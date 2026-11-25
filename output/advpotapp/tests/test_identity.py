from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class SessionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='operador.teste', password='test-password-only-8462')

    def test_anonymous_cannot_open_internal_pages(self):
        for route in ['/meu-trabalho/', '/casos/', '/administracao/usuarios/', '/historico/']:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith('/entrar/'))

    def test_login_and_logout_require_csrf_and_logout_is_not_get(self):
        browser = Client(enforce_csrf_checks=True)
        self.assertEqual(browser.post('/entrar/', {'username': self.user.username, 'password': 'test-password-only-8462'}).status_code, 403)
        page = browser.get('/entrar/')
        self.assertEqual(page.status_code, 200)
        token = browser.cookies['csrftoken'].value
        response = browser.post('/entrar/', {'username': self.user.username, 'password': 'test-password-only-8462', 'csrfmiddlewaretoken': token})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(browser.get('/sair/').status_code, 405)
        self.assertEqual(browser.post('/sair/').status_code, 403)

    def test_login_ignores_external_next_url(self):
        response = self.client.post('/entrar/?next=https://outside.invalid', {'username': self.user.username, 'password': 'test-password-only-8462'})
        self.assertRedirects(response, '/meu-trabalho/')

    def test_repeated_failure_limits_even_a_correct_password(self):
        for _ in range(5):
            self.client.post('/entrar/', {'username': self.user.username, 'password': 'incorrect'})
        response = self.client.post('/entrar/', {'username': self.user.username, 'password': 'test-password-only-8462'})
        self.assertEqual(response.status_code, 429)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_unknown_and_inactive_account_have_same_public_error(self):
        self.user.is_active = False
        self.user.save()
        unknown = self.client.post('/entrar/', {'username': 'does-not-exist', 'password': 'incorrect'})
        inactive = self.client.post('/entrar/', {'username': self.user.username, 'password': 'incorrect'})
        self.assertEqual(unknown.status_code, inactive.status_code)
        self.assertEqual(unknown.context['form'].non_field_errors(), inactive.context['form'].non_field_errors())

    def test_operator_cannot_manage_identity_or_read_audit(self):
        self.client.force_login(self.user)
        for route in ['/administracao/usuarios/', '/historico/']:
            self.assertEqual(self.client.get(route).status_code, 403)

    def test_whitespace_variants_do_not_bypass_account_limit_across_ips(self):
        for attempt in range(5):
            self.client.post('/entrar/', {'username': self.user.username, 'password': 'wrong'}, REMOTE_ADDR=f'192.0.2.{attempt}')
        response = self.client.post('/entrar/', {'username': ' ' * 200 + self.user.username, 'password': 'test-password-only-8462'}, REMOTE_ADDR='192.0.2.99')
        self.assertEqual(response.status_code, 429)

    def test_blocked_ip_cannot_keep_creating_name_buckets(self):
        from advpot.identity.models import LoginBucket
        for attempt in range(20):
            self.client.post('/entrar/', {'username': f'unknown.{attempt}', 'password': 'wrong'})
        before = LoginBucket.objects.count()
        for attempt in range(20, 25):
            response = self.client.post('/entrar/', {'username': f'unknown.{attempt}', 'password': 'wrong'})
            self.assertEqual(response.status_code, 429)
        self.assertEqual(LoginBucket.objects.count(), before)

    def test_expired_session_during_partial_request_redirects_entire_page(self):
        self.client.force_login(self.user)
        session = self.client.session
        session['identity_version'] = 0
        session.save()
        response = self.client.get('/casos/', HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.headers.get('HX-Redirect', '').startswith('/entrar/'))
