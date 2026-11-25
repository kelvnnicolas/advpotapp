import uuid
from django.core.exceptions import ValidationError
from django.http import Http404
from advpot.intake import services, workflow
from advpot.intake.exceptions import WorkflowConflict
from advpot.intake.models import Demand, DemandEvent, DemandGrant, CommercialHandoff
from advpot.identity.services import update_internal_user
from .test_intake import IntakeFixture


class CommercialWorkflowTests(IntakeFixture):
    def setUp(self):
        super().setUp()
        self.item = self.demand()

    def prepare_target(self):
        for action in ['view', 'receive_handoff', 'manage_opportunity', 'view_history']:
            services.grant_demand_action(actor=self.authority, target=self.commercial, demand_id=self.item.pk, action=action, enabled=True)

    def send(self, key=None):
        self.item.refresh_from_db()
        return workflow.send_to_commercial(actor=self.secretary, demand_id=self.item.pk, target_id=self.commercial.pk, expected_version=self.item.version, operation_key=key or uuid.uuid4())

    def accept(self):
        self.prepare_target()
        handoff = self.send()
        self.item.refresh_from_db()
        workflow.accept_handoff(actor=self.commercial, handoff_id=handoff.pk, expected_version=self.item.version, operation_key=uuid.uuid4())
        self.item.refresh_from_db()
        return handoff

    def test_send_requires_active_commercial_with_explicit_scope(self):
        with self.assertRaises(ValidationError):
            self.send()
        self.assertEqual(CommercialHandoff.objects.count(), 0)
        self.prepare_target()
        self.send()
        self.item.refresh_from_db()
        self.assertEqual(self.item.responsible_id, self.secretary.pk)
        self.assertEqual(self.item.journey_stage, 'reception')

    def test_accept_transfers_once_and_stale_actor_cannot_overwrite(self):
        self.prepare_target()
        handoff = self.send()
        self.item.refresh_from_db()
        version = self.item.version
        key = uuid.uuid4()
        workflow.accept_handoff(actor=self.commercial, handoff_id=handoff.pk, expected_version=version, operation_key=key)
        workflow.accept_handoff(actor=self.commercial, handoff_id=handoff.pk, expected_version=version, operation_key=key)
        with self.assertRaises(WorkflowConflict):
            workflow.accept_handoff(actor=self.commercial, handoff_id=handoff.pk, expected_version=version, operation_key=uuid.uuid4())
        self.item.refresh_from_db()
        self.assertEqual(self.item.responsible_id, self.commercial.pk)
        self.assertEqual(self.item.journey_stage, 'commercial')
        self.assertEqual(self.item.commercial_stage, 'diagnosis')
        self.assertEqual(DemandEvent.objects.filter(action='handoff.accept', demand=self.item).count(), 1)

    def test_pending_handoff_cannot_be_duplicated_or_bypassed(self):
        self.prepare_target()
        handoff = self.send()
        self.assertEqual(self.send(key=handoff.operation_key).pk, handoff.pk)
        with self.assertRaises(WorkflowConflict):
            self.send()
        self.item.refresh_from_db()
        with self.assertRaises((WorkflowConflict, Http404, ValidationError)):
            workflow.move_commercial_stage(actor=self.secretary, demand_id=self.item.pk, stage='proposal', expected_version=self.item.version, operation_key=uuid.uuid4(), reason='')

    def test_return_requires_reason_and_keeps_origin_owner(self):
        self.prepare_target()
        handoff = self.send()
        self.item.refresh_from_db()
        with self.assertRaises(ValidationError):
            workflow.return_handoff(actor=self.commercial, handoff_id=handoff.pk, reason='', expected_version=self.item.version, operation_key=uuid.uuid4())
        workflow.return_handoff(actor=self.commercial, handoff_id=handoff.pk, reason='Necessidade incompleta', expected_version=self.item.version, operation_key=uuid.uuid4())
        self.item.refresh_from_db()
        self.assertEqual(self.item.responsible_id, self.secretary.pk)
        self.assertEqual(self.item.journey_stage, 'reception')
        self.assertEqual(self.send().state, 'pending')

    def test_edit_version_and_commercial_prerequisites(self):
        self.accept()
        with self.assertRaises(ValidationError):
            workflow.move_commercial_stage(actor=self.commercial, demand_id=self.item.pk, stage='proposal', expected_version=self.item.version, operation_key=uuid.uuid4(), reason='')
        workflow.update_demand(actor=self.commercial, demand_id=self.item.pk, expected_version=self.item.version, operation_key=uuid.uuid4(), data={'next_step': 'Apresentar solução', 'next_step_on': None, 'solution': 'Solução fictícia', 'proposal': ''})
        old_version = self.item.version
        self.item.refresh_from_db()
        with self.assertRaises(WorkflowConflict):
            workflow.update_demand(actor=self.commercial, demand_id=self.item.pk, expected_version=old_version, operation_key=uuid.uuid4(), data={'next_step': 'Sobrescrever', 'next_step_on': None, 'solution': '', 'proposal': ''})
        workflow.move_commercial_stage(actor=self.commercial, demand_id=self.item.pk, stage='proposal', expected_version=self.item.version, operation_key=uuid.uuid4(), reason='')
        self.item.refresh_from_db()
        with self.assertRaises(ValidationError):
            workflow.move_commercial_stage(actor=self.commercial, demand_id=self.item.pk, stage='formalization', expected_version=self.item.version, operation_key=uuid.uuid4(), reason='')
        with self.assertRaises(ValidationError):
            workflow.move_commercial_stage(actor=self.commercial, demand_id=self.item.pk, stage='contracted', expected_version=self.item.version, operation_key=uuid.uuid4(), reason='')

    def test_lost_requires_reason_and_is_terminal_without_case_or_contract(self):
        self.accept()
        with self.assertRaises(ValidationError):
            workflow.move_commercial_stage(actor=self.commercial, demand_id=self.item.pk, stage='lost', reason='', expected_version=self.item.version, operation_key=uuid.uuid4())
        workflow.move_commercial_stage(actor=self.commercial, demand_id=self.item.pk, stage='lost', reason='Não prosseguiu com atendimento', expected_version=self.item.version, operation_key=uuid.uuid4())
        self.item.refresh_from_db()
        self.assertEqual(self.item.status, 'lost')
        self.assertTrue(self.item.closing_reason)
        from advpot.cases.models import Case
        self.assertEqual(Case.objects.count(), 0)

    def test_disable_origin_recovers_without_waiting_for_replacement(self):
        self.prepare_target()
        handoff = self.send()
        update_internal_user(actor=self.technical, user_id=self.secretary.pk, changes={'first_name': '', 'last_name': '', 'role': 'operator', 'is_active': False})
        self.item.refresh_from_db()
        handoff.refresh_from_db()
        self.assertIsNone(self.item.responsible_id)
        self.assertIsNotNone(self.item.recovery_queue_id)
        self.assertTrue(handoff.blocked)
        self.assertTrue(DemandGrant.objects.filter(demand=self.item, user=self.authority, action='recover').exists())
        self.assertFalse(DemandGrant.objects.filter(demand=self.item, user=self.authority, action='view').exists())
        self.assertEqual(DemandEvent.objects.filter(action='demand.recovery', demand=self.item).count(), 1)

    def test_revoking_owner_action_recovers_and_planned_sector_removal_is_blocked(self):
        self.accept()
        with self.assertRaises(ValidationError):
            services.assign_department(actor=self.authority, target=self.commercial, department='commercial', enabled=False)
        services.grant_demand_action(actor=self.authority, target=self.commercial, demand_id=self.item.pk, action='manage_opportunity', enabled=False)
        self.item.refresh_from_db()
        self.assertIsNotNone(self.item.recovery_queue_id)
        for action in ['view', 'edit_intake', 'send_handoff']:
            services.grant_demand_action(actor=self.authority, target=self.secretary, demand_id=self.item.pk, action=action, enabled=True)
        with self.assertRaises(ValidationError):
            workflow.recover_demand(actor=self.authority, demand_id=self.item.pk, target_id=self.secretary.pk, expected_version=self.item.version, operation_key=uuid.uuid4())
        services.grant_demand_action(actor=self.authority, target=self.commercial, demand_id=self.item.pk, action='manage_opportunity', enabled=True)
        workflow.recover_demand(actor=self.authority, demand_id=self.item.pk, target_id=self.commercial.pk, expected_version=self.item.version, operation_key=uuid.uuid4())
        self.item.refresh_from_db()
        self.assertEqual(self.item.responsible_id, self.commercial.pk)
        self.assertIsNone(self.item.recovery_queue_id)
