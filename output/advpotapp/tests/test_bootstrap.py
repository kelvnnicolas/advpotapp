from concurrent.futures import ThreadPoolExecutor
from io import StringIO
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.core.management import call_command, CommandError
from django.db import connection, connections
from django.test import TransactionTestCase
from django.test.testcases import skipUnlessDBFeature


class BootstrapTests(TransactionTestCase):
    def test_noninteractive_bootstrap_is_rejected_without_creating_account(self):
        with patch('sys.stdin.isatty', return_value=False):
            with self.assertRaises(CommandError):
                call_command('bootstrap_access_admin', stdout=StringIO())
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_concurrent_bootstrap_only_creates_one_initial_administrator(self):
        if connection.vendor != 'postgresql':
            self.skipTest('Serialização verificada no PostgreSQL de destino.')
        import threading
        barrier = threading.Barrier(2)

        def username(_):
            barrier.wait(timeout=10)
            return f'bootstrap-{threading.current_thread().name}'

        def run():
            try:
                call_command('bootstrap_access_admin', stdout=StringIO())
                return 'created'
            except CommandError:
                return 'rejected'
            finally:
                connections.close_all()

        with patch('sys.stdin.isatty', return_value=True), patch('builtins.input', side_effect=username), patch('advpot.identity.management.commands.bootstrap_access_admin.getpass', return_value='test-bootstrap-password-9371'):
            with ThreadPoolExecutor(max_workers=2) as pool:
                results = list(pool.map(lambda _: run(), range(2)))
        self.assertEqual(sorted(results), ['created', 'rejected'])
        self.assertEqual(get_user_model().objects.filter(role='access_admin').count(), 1)
