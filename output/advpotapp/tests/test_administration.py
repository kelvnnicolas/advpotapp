from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from advpot.audit.models import AuditEvent

User = get_user_model()


class AdministrationTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='administrador.teste', password='test-password-only-8462', role='access_admin')
        self.operator = User.objects.create_user(username='profissional.teste', password='test-password-only-8462')
        self.client.force_login(self.admin)

    def test_create_user_validates_password_and_does_not_set_superuser(self):
        data = {'username': 'novo.teste', 'first_name': 'Pessoa', 'last_name': 'Fictícia', 'role': 'operator', 'password1': '123', 'password2': '123'}
        response = self.client.post('/administracao/usuarios/novo/', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='novo.teste').exists())
        data.update(password1='new-test-password-6842', password2='new-test-password-6842', is_superuser='1', is_staff='1')
        response = self.client.post('/administracao/usuarios/novo/', data)
        self.assertEqual(response.status_code, 302)
        created = User.objects.get(username='novo.teste')
        self.assertFalse(created.is_superuser)
        self.assertFalse(created.is_staff)
        self.assertTrue(created.check_password('new-test-password-6842'))
        self.assertTrue(AuditEvent.objects.filter(action='identity.create', target=str(created.pk), actor=self.admin).exists())

    def test_disable_and_reactivate_never_restore_existing_session(self):
        browser = Client()
        browser.force_login(self.operator)
        original = browser.cookies['sessionid'].value
        url = f'/administracao/usuarios/{self.operator.pk}/'
        for active in [False, True]:
            data = {'first_name': '', 'last_name': '', 'role': 'operator'}
            if active:
                data['is_active'] = 'on'
            self.assertEqual(self.client.post(url, data).status_code, 302)
        browser.cookies['sessionid'] = original
        self.assertEqual(browser.get('/meu-trabalho/').status_code, 302)
        self.assertTrue(AuditEvent.objects.filter(action='identity.disable', actor=self.admin).exists())

    def test_revoke_all_sessions_and_change_role_invalidate_other_browser(self):
        browser = Client()
        browser.force_login(self.operator)
        url = f'/administracao/usuarios/{self.operator.pk}/revogar/'
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(self.client.post(url).status_code, 302)
        self.assertEqual(browser.get('/meu-trabalho/').status_code, 302)
        browser.force_login(self.operator)
        self.assertEqual(self.client.post(f'/administracao/usuarios/{self.operator.pk}/', {'first_name': '', 'last_name': '', 'role': 'auditor', 'is_active': 'on'}).status_code, 302)
        self.assertEqual(browser.get('/meu-trabalho/').status_code, 302)

    def test_operator_cannot_mutate_another_user(self):
        self.client.force_login(self.operator)
        for url in ['/administracao/usuarios/novo/', f'/administracao/usuarios/{self.admin.pk}/', f'/administracao/usuarios/{self.admin.pk}/revogar/']:
            self.assertEqual(self.client.post(url, {'role': 'access_admin', 'is_active': 'on'}).status_code, 403)
        self.operator.refresh_from_db()
        self.assertEqual(self.operator.role, 'operator')

    def test_administrator_cannot_disable_or_demote_own_account(self):
        response = self.client.post(f'/administracao/usuarios/{self.admin.pk}/', {'role': 'operator', 'first_name': '', 'last_name': ''})
        self.assertEqual(response.status_code, 200)
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)
        self.assertEqual(self.admin.role, 'access_admin')

    def test_user_management_requires_csrf(self):
        browser = Client(enforce_csrf_checks=True)
        browser.force_login(self.admin)
        self.assertEqual(browser.post(f'/administracao/usuarios/{self.operator.pk}/revogar/').status_code, 403)

    def test_audit_does_not_store_passwords(self):
        self.client.post('/administracao/usuarios/novo/', {'username': 'terceiro.teste', 'role': 'operator', 'password1': 'new-test-password-6842', 'password2': 'new-test-password-6842'})
        for event in AuditEvent.objects.all():
            self.assertNotIn('password', event.target)
            self.assertNotIn('6842', event.target)

    def test_two_validated_forms_cannot_crash_on_same_username(self):
        from django.core.exceptions import ValidationError
        from advpot.identity.forms import InternalUserCreationForm
        from advpot.identity.services import create_internal_user
        data = {'username': 'colisao.teste', 'role': 'operator', 'password1': 'collision-test-password-8172', 'password2': 'collision-test-password-8172'}
        first, second = InternalUserCreationForm(data), InternalUserCreationForm(data)
        self.assertTrue(first.is_valid())
        self.assertTrue(second.is_valid())
        create_internal_user(actor=self.admin, form=first)
        with self.assertRaises(ValidationError):
            create_internal_user(actor=self.admin, form=second)
        self.assertEqual(User.objects.filter(username='colisao.teste').count(), 1)
