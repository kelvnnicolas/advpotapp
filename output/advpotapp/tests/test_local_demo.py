from io import StringIO
from django.core.management import call_command, CommandError
from django.test import TestCase, override_settings
from advpot.identity.models import User
from advpot.intake.models import Contact, Demand, CommercialHandoff, BusinessAuthority
from advpot.cases.models import Case


@override_settings(DEBUG=True)
class LocalDemoTests(TestCase):
    def setUp(self):
        self.account = User.objects.create_user(username='teste', password='only-for-this-test')

    def seed(self):
        call_command('seed_local_demo', stdout=StringIO())

    def test_seed_is_replayable_preserves_login_and_exercises_real_workflow(self):
        password_hash = self.account.password
        self.seed()
        self.seed()
        self.assertEqual((Contact.objects.count(), Demand.objects.count(), Case.objects.count()), (6, 8, 3))
        self.account.refresh_from_db()
        self.assertEqual(self.account.password, password_hash)
        self.assertFalse(self.account.can_manage_identity)
        self.assertFalse(BusinessAuthority.objects.exists())
        self.assertTrue(all(item.title.startswith('[FICTÍCIO]') for item in Demand.objects.all()))
        self.assertEqual(Demand.objects.filter(status='lost').count(), 1)
        self.assertEqual(Demand.objects.filter(status='cancelled').count(), 1)
        pending = CommercialHandoff.objects.get(state='pending')
        self.assertEqual(pending.target_id, self.account.pk)
        self.client.force_login(self.account)
        for route in ['/clientes/', '/atendimentos/?status=all', '/casos/', '/passagens/']:
            self.assertEqual(self.client.get(route).status_code, 200)
        response = self.client.get('/atendimentos/?status=all')
        self.assertEqual(response.context['page_obj'].paginator.count, 8)

    @override_settings(DEBUG=False)
    def test_production_is_rejected_without_partial_load(self):
        with self.assertRaises(CommandError):
            self.seed()
        self.assertEqual((Contact.objects.count(), Demand.objects.count(), Case.objects.count()), (0, 0, 0))

    def test_missing_or_privileged_test_account_is_not_created_or_modified(self):
        self.account.role = 'access_admin'
        self.account.save()
        with self.assertRaises(CommandError):
            self.seed()
        self.account.delete()
        with self.assertRaises(CommandError):
            self.seed()
        self.assertEqual(Contact.objects.count(), 0)
