"""Opt-in real browser journey, isolated in Django's temporary test database."""
import os
import unittest
from pathlib import Path
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.crypto import get_random_string


def save_review_snapshot(page, output_dir, name):
    import re
    css = (Path(__file__).resolve().parent.parent / 'src' / 'static' / 'app.css').read_text(encoding='utf-8')
    html = page.content()
    html = re.sub(r'<link[^>]+href="/static/app.css"[^>]*>', lambda _: f'<style>{css}</style>', html)
    html = re.sub(r'<script\b[^>]*>.*?</script>', '', html, flags=re.S)
    html = re.sub(r'<input[^>]+name="csrfmiddlewaretoken"[^>]*>', '', html)
    (output_dir / f'{name}.html').write_text(html, encoding='utf-8')


@unittest.skipUnless(os.environ.get('ADVPOT_BROWSER_TESTS') == '1', 'Ative ADVPOT_BROWSER_TESTS=1 para a jornada visual.')
class BrowserJourneyTests(StaticLiveServerTestCase):
    def test_partial_search_updates_total_without_storing_case_content(self):
        from playwright.sync_api import sync_playwright
        from advpot.cases.models import Case, CaseGrant
        password = get_random_string(32)
        account = get_user_model().objects.create_user(username='leitor.visual', password=password)
        for title in ['Registro fictício Alfa', 'Registro fictício Beta']:
            case = Case.objects.create(title=title, responsible=account)
            CaseGrant.objects.create(case=case, user=account, action='view')
        with sync_playwright() as runtime:
            browser = runtime.chromium.launch(channel='chrome', headless=True)
            page = browser.new_page()
            page.goto(self.live_server_url + '/entrar/')
            page.get_by_label('Usuário', exact=True).fill(account.username)
            page.get_by_label('Senha', exact=True).fill(password)
            page.get_by_role('button', name='Entrar no meu espaço').click()
            page.wait_for_url('**/meu-trabalho/')
            page.get_by_role('link', name='Casos autorizados', exact=True).click()
            page.get_by_label('Buscar pelo título').fill('Alfa')
            page.get_by_role('button', name='Buscar', exact=True).click()
            page.wait_for_url('**/casos/?q=Alfa')
            page.wait_for_function("!document.querySelector('#case-results').innerText.includes('Beta')")
            storage = page.evaluate('JSON.stringify(sessionStorage)')
            self.assertNotIn('Registro fictício', storage)
            self.assertEqual(page.locator('.result-count').inner_text(), '1 resultado')
            storage = page.evaluate('JSON.stringify(sessionStorage)')
            self.assertNotIn('Registro fictício', storage)
            browser.close()

    def test_identity_flow_and_responsive_pages(self):
        from playwright.sync_api import sync_playwright
        from advpot.audit.models import AuditEvent
        password = get_random_string(32)
        get_user_model().objects.create_user(username='revisao.m1', first_name='Revisão', last_name='Fictícia', password=password, role='access_admin')
        screenshot_dir = Path(__file__).resolve().parent.parent / '.stitch' / 'previews'
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        with sync_playwright() as runtime:
            browser = runtime.chromium.launch(channel='chrome', headless=True)
            page = browser.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1)
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(self.live_server_url + '/entrar/')
            page.screenshot(path=str(screenshot_dir / 'm1-login.png'), full_page=True)
            save_review_snapshot(page, screenshot_dir, 'm1-login')
            page.get_by_label('Usuário', exact=True).fill('revisao.m1')
            page.get_by_label('Senha', exact=True).fill(password)
            page.get_by_role('button', name='Entrar no meu espaço').click()
            page.wait_for_url('**/meu-trabalho/')
            self.assertTrue(page.get_by_role('heading', name='Bom trabalho, Revisão.').is_visible())
            page.screenshot(path=str(screenshot_dir / 'm1-meu-trabalho.png'), full_page=True)
            save_review_snapshot(page, screenshot_dir, 'm1-meu-trabalho')
            page.get_by_role('link', name='Casos autorizados', exact=True).click()
            self.assertTrue(page.get_by_role('heading', name='Nenhum caso compartilhado ainda').is_visible())
            page.screenshot(path=str(screenshot_dir / 'm1-casos.png'), full_page=True)
            page.get_by_role('link', name='Usuários e acessos', exact=True).click()
            page.screenshot(path=str(screenshot_dir / 'm1-usuarios.png'), full_page=True)
            save_review_snapshot(page, screenshot_dir, 'm1-usuarios')
            page.get_by_role('link', name='Adicionar usuário').click()
            page.get_by_label('Usuário', exact=True).fill('colega.ficticio')
            page.get_by_label('Primeiro nome', exact=True).fill('Colega')
            page.get_by_label('Senha', exact=True).fill(password)
            page.get_by_label('Confirmação de senha', exact=True).fill(password)
            page.get_by_role('button', name='Criar usuário').click()
            page.wait_for_url('**/administracao/usuarios/')
            self.assertTrue(page.get_by_text('colega.ficticio', exact=True).is_visible())
            page.set_viewport_size({'width': 390, 'height': 844})
            page.goto(self.live_server_url + '/meu-trabalho/')
            self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), 390)
            page.screenshot(path=str(screenshot_dir / 'm1-mobile.png'), full_page=True)
            page.get_by_role('button', name='Sair', exact=True).click()
            page.wait_for_url('**/entrar/')
            self.assertEqual(errors, [])
            browser.close()
        self.assertTrue(AuditEvent.objects.filter(action='session.logout').exists())
