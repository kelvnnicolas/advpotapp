from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from advpot.audit.models import AuditEvent
from advpot.cases.models import Case, CaseGrant

User = get_user_model()


class RecordAccessTests(TestCase):
    def setUp(self):
        self.viewer = User.objects.create_user(username='leitor.teste', password='test-password-only-8462')
        self.other = User.objects.create_user(username='outro.teste', password='test-password-only-8462')
        self.admin = User.objects.create_user(username='gestor.acessos', password='test-password-only-8462', role='access_admin')
        self.shared = Case.objects.create(title='Registro fictício compartilhado', responsible=self.viewer)
        self.hidden = Case.objects.create(title='Registro fictício reservado', responsible=self.other)
        CaseGrant.objects.create(user=self.viewer, case=self.shared, action='view')
        self.client.force_login(self.viewer)

    def test_list_search_and_counter_do_not_reveal_unshared_records(self):
        response = self.client.get('/casos/')
        self.assertContains(response, self.shared.title)
        self.assertNotContains(response, self.hidden.title)
        self.assertEqual(response.context['page_obj'].paginator.count, 1)
        search = self.client.get('/casos/', {'q': 'reservado'})
        self.assertEqual(search.context['page_obj'].paginator.count, 0)
        dashboard = self.client.get('/meu-trabalho/')
        self.assertEqual(dashboard.context['case_count'], 1)

    def test_detail_returns_same_response_for_missing_and_unshared(self):
        import uuid
        self.assertEqual(self.client.get(f'/casos/{self.hidden.pk}/').status_code, 404)
        self.assertEqual(self.client.get(f'/casos/{uuid.uuid4()}/').status_code, 404)

    def test_administrator_and_responsible_have_no_implicit_case_access(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get('/casos/').context['page_obj'].paginator.count, 0)
        self.assertEqual(self.client.get(f'/casos/{self.shared.pk}/').status_code, 404)
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(f'/casos/{self.hidden.pk}/').status_code, 404)

    def test_export_needs_read_and_export_grants_and_records_actor(self):
        url = f'/casos/{self.shared.pk}/exportar/'
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(self.client.post(url).status_code, 404)
        CaseGrant.objects.create(user=self.viewer, case=self.shared, action='export')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['case']['title'], self.shared.title)
        self.assertNotIn(self.hidden.title, response.content.decode())
        self.assertTrue(AuditEvent.objects.filter(actor=self.viewer, action='case.export', target=str(self.shared.pk)).exists())
        CaseGrant.objects.filter(user=self.viewer, case=self.shared, action='view').delete()
        self.assertEqual(self.client.post(url).status_code, 404)

    def test_export_requires_csrf(self):
        CaseGrant.objects.create(user=self.viewer, case=self.shared, action='export')
        browser = Client(enforce_csrf_checks=True)
        browser.force_login(self.viewer)
        self.assertEqual(browser.post(f'/casos/{self.shared.pk}/exportar/').status_code, 403)

    def test_auditor_can_read_events_without_case_content(self):
        auditor = User.objects.create_user(username='auditor.teste', role='auditor')
        self.client.force_login(auditor)
        response = self.client.get('/historico/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.hidden.title)
        self.assertEqual(self.client.get(f'/casos/{self.shared.pk}/').status_code, 404)
