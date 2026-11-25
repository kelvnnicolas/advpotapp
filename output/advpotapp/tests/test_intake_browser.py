import os
import re
import unittest
from concurrent.futures import ThreadPoolExecutor
from django.db import connections
from pathlib import Path
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.crypto import get_random_string
from advpot.identity.models import User
from advpot.intake import services
from advpot.intake.models import Contact, Demand, DemandEvent


@unittest.skipUnless(os.environ.get('ADVPOT_BROWSER_TESTS') == '1', 'Ative a jornada de navegador explicitamente.')
class IntakeBrowserJourney(StaticLiveServerTestCase):
    def test_secretariat_to_commercial_with_persistent_pipeline_and_mobile(self):
        from playwright.sync_api import sync_playwright
        from advpot.cases.models import Case
        password = get_random_string(32)
        technical = User.objects.create_user(username='tecnico.visual', role='access_admin')
        authority = User.objects.create_user(username='gestao.visual')
        secretary = User.objects.create_user(username='secretaria.visual', password=password)
        commercial = User.objects.create_user(username='comercial.visual', password=password)
        services.initialize_business_authority(operator=technical, target=authority, approval_reference='Teste fictício de navegador')
        for account, department in [(secretary, 'secretariat'), (commercial, 'commercial')]:
            services.assign_department(actor=authority, target=account, department=department, enabled=True)
        output = Path(__file__).resolve().parent.parent / '.stitch' / 'previews'
        with ThreadPoolExecutor(max_workers=1) as worker, sync_playwright() as runtime:
            def db(callback):
                def run():
                    try:
                        return callback()
                    finally:
                        connections.close_all()
                return worker.submit(run).result()
            browser = runtime.chromium.launch(channel='chrome', headless=True)
            page = browser.new_page(viewport={'width': 1440, 'height': 1000})
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))

            def login(account):
                page.goto(self.live_server_url + '/entrar/')
                page.get_by_label('Usuário', exact=True).fill(account.username)
                page.get_by_label('Senha', exact=True).fill(password)
                page.get_by_role('button', name='Entrar no meu espaço').click()
                page.wait_for_url('**/meu-trabalho/')

            login(secretary)
            page.goto(self.live_server_url + '/clientes/novo/')
            page.get_by_label('Tipo', exact=False).select_option('person')
            page.get_by_label('Nome', exact=False).fill('Pessoa fictícia da jornada')
            page.get_by_label('Motivo da ausência de contato').fill('Atendimento presencial fictício')
            page.get_by_role('button', name='Salvar', exact=True).click()
            page.wait_for_url(re.compile(r'/clientes/[0-9a-f-]{36}/$'))
            self.assertEqual(db(lambda: Contact.objects.count()), 1)
            page.get_by_role('link', name='Abrir atendimento', exact=True).click()
            page.get_by_label('Contato:', exact=True).select_option(str(db(lambda: Contact.objects.get().pk)))
            for label, value in [('Título', 'Demanda fictícia da jornada'), ('Necessidade', 'Avaliar documentação'), ('Origem', 'Presencial'), ('Próximo passo', 'Conversa com Comercial')]:
                page.get_by_label(label + ':' , exact=True).fill(value)
            page.get_by_role('button', name='Salvar', exact=True).click()
            page.wait_for_url(re.compile(r'/atendimentos/[0-9a-f-]{36}/$'))
            demand = db(lambda: Demand.objects.get())
            for action in ['view', 'receive_handoff', 'manage_opportunity', 'view_history']:
                db(lambda: services.grant_demand_action(actor=authority, target=commercial, demand_id=demand.pk, action=action, enabled=True))
            page.reload()
            page.get_by_label('Destinatário do Comercial').select_option(str(commercial.pk))
            page.get_by_role('button', name='Enviar passagem').click()
            page.wait_for_url('**/atendimentos/*/')
            self.assertTrue(page.get_by_role('heading', name='Passagem aguardando recebimento').is_visible())
            db(demand.refresh_from_db)
            self.assertEqual(demand.responsible_id, secretary.pk)
            page.get_by_role('button', name='Sair', exact=True).click()
            login(commercial)
            page.goto(self.live_server_url + '/passagens/')
            page.locator('select[name=decision]').select_option('accept')
            page.get_by_role('button', name='Registrar decisão').click()
            page.wait_for_url('**/passagens/')
            db(demand.refresh_from_db)
            self.assertEqual(demand.responsible_id, commercial.pk)
            page.goto(self.live_server_url + f'/atendimentos/{demand.pk}/')
            self.assertFalse(page.get_by_text('Pessoa fictícia da jornada', exact=True).count())
            page.get_by_role('link', name='Atualizar atendimento').click()
            page.get_by_label('Solução proposta', exact=False).fill('Revisão documental fictícia')
            page.get_by_label('Resumo da proposta', exact=False).fill('Escopo para revisão fictícia')
            page.get_by_role('button', name='Salvar', exact=True).click()
            page.wait_for_url('**/atendimentos/*/')
            page.get_by_label('Próxima situação').select_option('proposal')
            page.get_by_role('button', name='Registrar etapa').click()
            page.wait_for_url('**/atendimentos/*/')
            page.get_by_label('Próxima situação').select_option('formalization')
            page.get_by_role('button', name='Registrar etapa').click()
            page.wait_for_url('**/atendimentos/*/')
            db(demand.refresh_from_db)
            self.assertEqual(demand.commercial_stage, 'formalization')
            page.screenshot(path=str(output / 'm2a-atendimento.png'), full_page=True)
            page.goto(self.live_server_url + '/atendimentos/?view=board')
            self.assertTrue(page.get_by_role('link', name=demand.title, exact=True).is_visible())
            page.screenshot(path=str(output / 'm2a-pipeline.png'), full_page=True)
            page.set_viewport_size({'width': 390, 'height': 844})
            self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), 390)
            page.screenshot(path=str(output / 'm2a-mobile.png'), full_page=True)
            self.assertEqual(errors, [])
            self.assertEqual(db(lambda: Case.objects.count()), 0)
            self.assertEqual(db(lambda: DemandEvent.objects.filter(action='handoff.accept').count()), 1)
            db(connections.close_all)
            browser.close()
