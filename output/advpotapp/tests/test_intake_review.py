import uuid
from django.core.exceptions import ValidationError
from advpot.intake import access, services, workflow
from advpot.intake.models import CommercialHandoff, DemandGrant
from .test_intake import IntakeFixture


class ReviewRegressionTests(IntakeFixture):
    def disable(self, account):
        from advpot.identity.services import update_internal_user
        update_internal_user(actor=self.technical, user_id=account.pk, changes={'first_name': '', 'last_name': '', 'role': account.role, 'is_active': False})

    def prepared(self):
        item = self.demand()
        for action in ['view', 'receive_handoff', 'manage_opportunity']:
            services.grant_demand_action(actor=self.authority, target=self.commercial, demand_id=item.pk, action=action, enabled=True)
        handoff = workflow.send_to_commercial(actor=self.secretary, demand_id=item.pk, target_id=self.commercial.pk, expected_version=item.version, operation_key=uuid.uuid4())
        return item, handoff

    def test_recovery_authorizes_before_rendering_users_and_filters_eligible_targets(self):
        item, handoff = self.prepared()
        self.disable(self.secretary)
        self.client.force_login(self.technical)
        response = self.client.post(f'/gestao/recuperacao/{item.pk}/', {})
        self.assertEqual(response.status_code, 403)
        self.assertNotContains(response, self.commercial.username, status_code=403)
        services.assign_department(actor=self.authority, target=self.other, department='secretariat', enabled=True)
        for action in ['view', 'edit_intake']:
            services.grant_demand_action(actor=self.authority, target=self.other, demand_id=item.pk, action=action, enabled=True)
        self.client.force_login(self.authority)
        response = self.client.get('/gestao/recuperacao/')
        candidates = response.context['items'][0]['form'].fields['target'].queryset
        self.assertEqual(list(candidates), [self.other])

    def test_secretariat_cannot_write_commercial_fields_in_service_or_form(self):
        item = self.demand()
        with self.assertRaises(ValidationError):
            workflow.update_demand(actor=self.secretary, demand_id=item.pk, expected_version=item.version, operation_key=uuid.uuid4(), data={'solution': 'Proposta indevida', 'proposal': 'Resumo indevido'})
        self.client.force_login(self.secretary)
        response = self.client.get(f'/atendimentos/{item.pk}/editar/')
        self.assertNotContains(response, 'name="solution"')
        self.assertNotContains(response, 'name="proposal"')
        item.refresh_from_db()
        self.assertEqual((item.solution, item.proposal, item.version), ('', '', 1))

    def test_management_sector_alone_does_not_gain_recovery_grants(self):
        item = self.demand()
        services.assign_department(actor=self.authority, target=self.other, department='management', enabled=True)
        self.disable(self.secretary)
        self.assertFalse(DemandGrant.objects.filter(user=self.other, demand=item, action='recover').exists())
        self.client.force_login(self.other)
        response = self.client.get('/gestao/recuperacao/')
        self.assertEqual(response.context['page_obj'].paginator.count, 0)

    def test_commercial_creator_can_correct_own_intake_without_commercial_stage_skip(self):
        item = self.demand(actor=self.commercial)
        self.assertTrue(access.visible_demands(self.commercial, 'edit_intake').filter(pk=item.pk).exists())
        workflow.update_demand(actor=self.commercial, demand_id=item.pk, expected_version=1, operation_key=uuid.uuid4(), data={'need': 'Necessidade corrigida'})
        item.refresh_from_db()
        self.assertEqual((item.need, item.journey_stage), ('Necessidade corrigida', 'reception'))
        with self.assertRaises(ValidationError):
            services.assign_department(actor=self.authority, target=self.commercial, department='commercial', enabled=False)

    def test_recovery_cancels_blocked_handoff_so_replacement_can_edit(self):
        item, handoff = self.prepared()
        self.disable(self.secretary)
        services.assign_department(actor=self.authority, target=self.other, department='secretariat', enabled=True)
        for action in ['view', 'edit_intake']:
            services.grant_demand_action(actor=self.authority, target=self.other, demand_id=item.pk, action=action, enabled=True)
        item.refresh_from_db()
        workflow.recover_demand(actor=self.authority, demand_id=item.pk, target_id=self.other.pk, expected_version=item.version, operation_key=uuid.uuid4())
        handoff.refresh_from_db()
        self.assertEqual(handoff.state, CommercialHandoff.State.CANCELLED)
        item.refresh_from_db()
        workflow.update_demand(actor=self.other, demand_id=item.pk, expected_version=item.version, operation_key=uuid.uuid4(), data={'next_step': 'Retomar triagem'})
        item.refresh_from_db()
        self.assertEqual(item.next_step, 'Retomar triagem')

    def test_delegated_access_can_be_managed_on_the_authorized_demand_only(self):
        item = self.demand()
        services.grant_demand_action(actor=self.authority, target=self.secretary, demand_id=item.pk, action='manage_access', enabled=True)
        self.client.force_login(self.secretary)
        response = self.client.get(f'/atendimentos/{item.pk}/acessos/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('recover', dict(response.context['form'].fields['action'].choices))
        self.assertNotIn('manage_opportunity', dict(response.context['form'].fields['action'].choices))
        response = self.client.post(f'/atendimentos/{item.pk}/acessos/', {'kind': 'demand', 'record_id': item.pk, 'target': self.commercial.pk, 'action': 'view', 'enabled': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(access.visible_demands(self.commercial).filter(pk=item.pk).exists())
        response = self.client.post(f'/atendimentos/{item.pk}/acessos/', {'kind': 'demand', 'record_id': item.pk, 'target': self.commercial.pk, 'action': 'recover', 'enabled': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(DemandGrant.objects.filter(user=self.commercial, demand=item, action='recover').exists())
        other = self.demand(actor=self.commercial)
        self.assertEqual(self.client.get(f'/atendimentos/{other.pk}/acessos/').status_code, 404)
