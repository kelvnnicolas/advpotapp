import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from django.db import connection, connections
from django.test import TransactionTestCase
from advpot.intake import services, workflow
from advpot.intake.exceptions import WorkflowConflict
from advpot.intake.models import DemandEvent
from .test_intake import IntakeFixture


class ConcurrentAcceptanceTests(TransactionTestCase):
    contact = IntakeFixture.contact
    demand = IntakeFixture.demand

    def setUp(self):
        IntakeFixture.setUp(self)

    def test_postgres_two_simultaneous_acceptances_have_one_winner(self):
        if connection.vendor != 'postgresql':
            self.skipTest('Verificação de bloqueio exige PostgreSQL.')
        item = self.demand()
        for action in ['view', 'receive_handoff', 'manage_opportunity']:
            services.grant_demand_action(actor=self.authority, target=self.commercial, demand_id=item.pk, action=action, enabled=True)
        handoff = workflow.send_to_commercial(actor=self.secretary, demand_id=item.pk, target_id=self.commercial.pk, expected_version=1, operation_key=uuid.uuid4())
        item.refresh_from_db()
        barrier = threading.Barrier(2)

        def accept(_):
            try:
                barrier.wait(timeout=10)
                workflow.accept_handoff(actor=self.commercial, handoff_id=handoff.pk, expected_version=item.version, operation_key=uuid.uuid4())
                return 'accepted'
            except WorkflowConflict:
                return 'conflict'
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as executor:
            outcomes = list(executor.map(accept, range(2)))
        self.assertEqual(sorted(outcomes), ['accepted', 'conflict'])
        self.assertEqual(DemandEvent.objects.filter(demand=item, action='handoff.accept').count(), 1)
