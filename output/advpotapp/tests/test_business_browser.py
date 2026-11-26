import os
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db import connections
from django.test import override_settings
from django.utils.crypto import get_random_string
from advpot.identity.models import User


@unittest.skipUnless(os.environ.get('ADVPOT_BROWSER_TESTS') == '1', 'Ative ADVPOT_BROWSER_TESTS para Chrome real.')
@override_settings(DEBUG=True)
class BusinessBrowserTests(StaticLiveServerTestCase):
    def setUp(self):
        self.password = get_random_string(32)
        self.account = User.objects.create_user(username='business.visual', password=self.password)
        self.output = Path(__file__).resolve().parent.parent / '.stitch' / 'previews'

    def login(self, page):
        page.goto(self.live_server_url + '/entrar/')
        page.get_by_label('Usuário', exact=True).fill(self.account.username)
        page.get_by_label('Senha', exact=True).fill(self.password)
        page.get_by_role('button', name='Entrar no meu espaço').click()
        page.wait_for_url('**/meu-trabalho/')

    def test_business_journey_is_interactive_responsive_and_has_no_domain_writes(self):
        from playwright.sync_api import sync_playwright, expect
        from advpot.audit.models import AuditEvent
        from advpot.intake.models import Contact, Demand, BusinessAuthority, DemandGrant, BusinessAssignment
        from advpot.cases.models import Case
        def counts():
            try:
                return tuple(model.objects.count() for model in [User, Contact, Demand, Case, AuditEvent, BusinessAuthority, DemandGrant, BusinessAssignment])
            finally:
                connections.close_all()
        with ThreadPoolExecutor(max_workers=1) as worker, sync_playwright() as runtime:
            browser = runtime.chromium.launch(channel='chrome', headless=True)
            page = browser.new_page(viewport={'width': 1440, 'height': 1000})
            errors, writes, external = [], [], []
            page.on('pageerror', lambda error: errors.append(str(error)))
            self.login(page)
            baseline = worker.submit(counts).result()
            page.on('request', lambda req: writes.append(req.url) if req.method not in {'GET', 'HEAD'} else None)
            page.on('request', lambda req: external.append(req.url) if not req.url.startswith(self.live_server_url) else None)
            page.get_by_role('link', name='Business · prévia', exact=True).click()
            expect(page.get_by_role('heading', name='Visão do escritório', exact=True)).to_be_visible()
            page.screenshot(path=str(self.output / 'business-overview.png'), full_page=True)
            page.get_by_role('link', name='Equipe', exact=True).click()
            self.assertTrue(page.get_by_label('Nome fictício', exact=True).is_enabled())
            page.get_by_label('Buscar pessoa ou e-mail fictício').fill('inexistente')
            expect(page.locator('[data-team-empty]')).to_be_visible()
            page.get_by_label('Buscar pessoa ou e-mail fictício').fill('')
            page.screenshot(path=str(self.output / 'business-team.png'), full_page=True)
            page.get_by_label('Nome fictício', exact=True).fill('Dora Horizonte')
            page.get_by_label('E-mail fictício', exact=True).fill('dora@horizonte.invalid')
            page.get_by_role('button', name='Preparar convite na prévia').press('Enter')
            expect(page.locator('[data-member-row]')).to_have_count(4)
            expect(page.locator('[data-form-feedback]')).to_contain_text('Nenhum e-mail foi enviado')
            page.get_by_label('Nome fictício', exact=True).fill('Dora repetida')
            page.get_by_label('E-mail fictício', exact=True).fill('DORA@HORIZONTE.INVALID')
            page.get_by_role('button', name='Preparar convite na prévia').click()
            expect(page.locator('[data-form-feedback]')).to_contain_text('já existe')
            expect(page.locator('[data-member-row]')).to_have_count(4)
            page.get_by_label('E-mail fictício', exact=True).fill('papel@horizonte.invalid')
            page.locator('#invite-role').evaluate("select => { const option = new Option('Adulterado', 'owner'); select.add(option); select.value = 'owner'; }")
            page.get_by_role('button', name='Preparar convite na prévia').click()
            expect(page.locator('[data-form-feedback]')).to_contain_text('papel válido')
            expect(page.locator('[data-member-row]')).to_have_count(4)
            row = page.locator('[data-member-row]').filter(has_text='Bruno Horizonte')
            row.get_by_role('button', name='Simular suspensão').click()
            expect(row.locator('[data-member-status]')).to_have_text('Suspenso na prévia')
            page.get_by_role('link', name='Fluxos', exact=True).click()
            page.get_by_label('Nome do fluxo', exact=True).fill('Atendimento da equipe fictícia')
            page.get_by_role('button', name='Aplicar na prévia').click()
            expect(page.locator('[data-flow-title]')).to_have_text('Atendimento da equipe fictícia')
            expect(page.locator('[data-flow-version]')).to_have_text('Prévia v2')
            expect(page.locator('.business-flow li')).to_have_count(6)
            page.get_by_role('link', name='Configurações', exact=True).click()
            page.get_by_label('Nome demonstrativo do escritório').fill('Horizonte · revisão fictícia')
            page.get_by_role('button', name='Revisar configuração').click()
            expect(page.locator('[data-settings-name]')).to_have_text('Horizonte · revisão fictícia')
            page.get_by_role('link', name='Assinatura', exact=True).click()
            page.get_by_label('Cenário de assinatura', exact=True).select_option('expired')
            page.get_by_role('button', name='Visualizar', exact=True).click()
            expect(page.locator('.business-status').filter(has_text='Período encerrado')).to_be_visible()
            page.get_by_role('link', name='Ver retorno de contratação').click()
            page.get_by_role('link', name='Ver assinatura demonstrativa').click()
            self.assertIn('scenario=expired', page.url)
            expect(page.locator('.business-status').filter(has_text='Período encerrado')).to_be_visible()
            page.get_by_role('link', name='Integrações', exact=True).click()
            self.assertIn('scenario=expired', page.url)
            expect(page.locator('.business-status')).to_have_count(3)
            page.set_viewport_size({'width': 390, 'height': 844})
            for route in ['/business/', '/business/equipe/', '/business/fluxos/', '/business/assinatura/', '/business/integracoes/', '/business/configuracoes/']:
                page.goto(self.live_server_url + route)
                self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), 390, route)
            page.goto(self.live_server_url + '/business/')
            page.screenshot(path=str(self.output / 'business-mobile.png'), full_page=True)
            self.assertEqual(page.evaluate('JSON.stringify(localStorage)'), '{}')
            storage = page.evaluate('Object.fromEntries(Object.entries(sessionStorage))')
            self.assertEqual(set(storage) - {'htmx-current-path-for-history'}, set())
            self.assertNotIn('dora@horizonte.invalid', str(storage))
            self.assertEqual(worker.submit(counts).result(), baseline)
            self.assertEqual((errors, writes, external), ([], [], []))
            browser.close()

    def test_contract_summary_and_untrusted_text_never_confirm_payment(self):
        from playwright.sync_api import sync_playwright, expect
        with sync_playwright() as runtime:
            browser = runtime.chromium.launch(channel='chrome', headless=True)
            page = browser.new_page(viewport={'width': 1440, 'height': 1000})
            dialogs = []
            page.on('dialog', lambda dialog: (dialogs.append(dialog.message), dialog.dismiss()))
            page.goto(self.live_server_url + '/contratar/')
            self.assertTrue(page.get_by_label('Nome fictício do escritório').is_enabled())
            page.get_by_label('Nome fictício do escritório').fill('Horizonte · escritório fictício')
            page.get_by_label('Responsável fictício', exact=True).fill('<img src=x onerror=alert(1)>')
            page.get_by_label('Entendo que esta é uma prévia').check()
            page.get_by_role('button', name='Ver resumo da contratação').click()
            expect(page.locator('[data-contract-summary]')).to_be_visible()
            expect(page.locator('[data-contract-owner]')).to_have_text('<img src=x onerror=alert(1)>')
            self.assertEqual(page.locator('[data-contract-owner] img').count(), 0)
            self.assertEqual(dialogs, [])
            page.screenshot(path=str(self.output / 'business-contract.png'), full_page=True)
            page.get_by_role('link', name='Visualizar retorno pendente').click()
            expect(page.get_by_role('heading', name='Aguardando confirmação', exact=True)).to_be_visible()
            self.assertNotIn('onerror', page.url)
            page.set_viewport_size({'width': 390, 'height': 844})
            for route in ['/contratar/', '/contratar/retorno/']:
                page.goto(self.live_server_url + route)
                self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), 390)
            browser.close()

    def test_without_javascript_preview_inputs_stay_disabled_and_navigation_works(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as runtime:
            browser = runtime.chromium.launch(channel='chrome', headless=True)
            page = browser.new_page(java_script_enabled=False)
            self.login(page)
            for route in ['/business/equipe/', '/business/fluxos/', '/business/configuracoes/', '/contratar/']:
                page.goto(self.live_server_url + route)
                self.assertIsNotNone(page.locator('[data-preview-form] fieldset').get_attribute('disabled'))
                self.assertTrue(page.locator('[data-preview-form] input').first.is_disabled())
                self.assertTrue(page.locator('noscript .notice').is_visible(), route)
            browser.close()
