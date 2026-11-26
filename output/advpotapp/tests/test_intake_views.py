import uuid
from django.test import Client
from advpot.intake import services
from advpot.intake.models import Contact, Demand
from .test_intake import IntakeFixture


class IntakeViewTests(IntakeFixture):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.secretary)

    def test_login_and_technical_admin_cannot_access_business_management(self):
        self.client.logout()
        for route in ['/clientes/', '/atendimentos/', '/passagens/', '/gestao/acessos-negocio/']:
            self.assertEqual(self.client.get(route).status_code, 302)
        self.client.force_login(self.technical)
        self.assertEqual(self.client.get('/gestao/acessos-negocio/').status_code, 403)
        self.assertEqual(self.client.post('/clientes/novo/', {}).status_code, 403)

    def test_contact_and_demand_create_forms_persist_and_reuse_contact(self):
        response = self.client.post('/clientes/novo/', {'kind': 'person', 'name': 'Pessoa fictícia da tela', 'email': '', 'phone': '', 'channel_absence_reason': 'Contato presencial', 'operation_key': uuid.uuid4()})
        self.assertEqual(response.status_code, 302)
        contact = Contact.objects.get(name='Pessoa fictícia da tela')
        response = self.client.post('/atendimentos/novo/', {'contact': contact.pk, 'title': 'Atendimento fictício da tela', 'need': 'Entender a demanda', 'origin': 'Presencial', 'area': '', 'next_step': 'Triagem', 'next_step_on': '', 'operation_key': uuid.uuid4()})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Demand.objects.get().contact_id, contact.pk)

    def test_invalid_demand_preserves_form_and_cannot_select_hidden_contact(self):
        visible = self.contact()
        hidden = self.contact(actor=self.commercial, name='Cadastro fictício reservado')
        response = self.client.get('/atendimentos/novo/')
        self.assertContains(response, visible.name)
        self.assertNotContains(response, hidden.name)
        response = self.client.post('/atendimentos/novo/', {'contact': hidden.pk, 'title': 'Texto preservado', 'need': '', 'origin': 'Presencial', 'next_step': 'Triagem', 'operation_key': uuid.uuid4()})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Texto preservado')
        self.assertEqual(Demand.objects.count(), 0)

    def test_lists_board_and_search_hide_other_scope_and_serialize_same_total(self):
        mine = self.demand()
        other = self.demand(actor=self.commercial)
        for route in ['/atendimentos/', '/atendimentos/?view=board', '/atendimentos/?q=reservado']:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, str(other.pk))
        listing = self.client.get('/atendimentos/')
        self.assertEqual(listing.context['page_obj'].paginator.count, 1)
        self.assertContains(listing, str(mine.pk))
        self.assertEqual(self.client.get(f'/atendimentos/{other.pk}/').status_code, 404)
        self.assertEqual(self.client.get(f'/clientes/{other.contact_id}/').status_code, 404)

    def test_duplicate_confirmation_applies_only_to_visible_contacts(self):
        self.contact(name='Pessoa Exemplo')
        data = {'kind': 'person', 'name': 'pessoa exemplo', 'channel_absence_reason': 'Presencial', 'operation_key': uuid.uuid4()}
        first = self.client.post('/clientes/novo/', data)
        self.assertEqual(first.status_code, 200)
        self.assertEqual(Contact.objects.count(), 1)
        approved = self.client.post('/clientes/novo/', {**data, 'duplicate_ack': 'on'})
        self.assertEqual(approved.status_code, 302)
        self.assertEqual(Contact.objects.count(), 2)

    def test_contact_edit_is_scoped_versioned_and_audited(self):
        contact = self.contact()
        response = self.client.post(f'/clientes/{contact.pk}/editar/', {'kind': 'person', 'name': 'Nome fictício corrigido', 'email': '', 'phone': '', 'channel_absence_reason': 'Presencial', 'expected_version': 1, 'duplicate_ack': 'on'})
        self.assertEqual(response.status_code, 302)
        contact.refresh_from_db()
        self.assertEqual(contact.name, 'Nome fictício corrigido')
        self.assertEqual(contact.version, 2)
        stale = self.client.post(f'/clientes/{contact.pk}/editar/', {'kind': 'person', 'name': 'Sobrescrever antigo', 'channel_absence_reason': 'Presencial', 'expected_version': 1, 'duplicate_ack': 'on'})
        self.assertEqual(stale.status_code, 409)
        from advpot.intake.models import ContactEvent
        self.assertEqual(ContactEvent.objects.filter(contact=contact, action='contact.update').count(), 1)

    def test_mutations_require_csrf_and_unknown_action_does_not_change_stage(self):
        demand = self.demand()
        browser = Client(enforce_csrf_checks=True)
        browser.force_login(self.secretary)
        self.assertEqual(browser.post('/atendimentos/novo/', {}).status_code, 403)
        self.assertEqual(browser.post(f'/atendimentos/{demand.pk}/editar/', {}).status_code, 403)
        self.assertEqual(self.client.get(f'/atendimentos/{demand.pk}/etapa/').status_code, 405)

    def test_authority_can_assign_business_scope_without_receiving_content(self):
        demand = self.demand()
        self.client.force_login(self.authority)
        response = self.client.post('/gestao/acessos-negocio/', {'kind': 'department', 'target': self.other.pk, 'department': 'commercial', 'enabled': 'on'})
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/gestao/acessos-negocio/', {'kind': 'demand', 'target': self.other.pk, 'record_id': demand.pk, 'action': 'view', 'enabled': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get(f'/atendimentos/{demand.pk}/').status_code, 404)
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(f'/atendimentos/{demand.pk}/').status_code, 200)
