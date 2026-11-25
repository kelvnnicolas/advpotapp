import uuid
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from django.test import TestCase
from advpot.intake.models import BusinessAuthority, BusinessAssignment, Contact, ContactGrant, Demand, DemandGrant, DemandEvent
from advpot.intake import access, services

User = get_user_model()


class IntakeFixture(TestCase):
    def setUp(self):
        self.technical = User.objects.create_user(username='tecnico.ficticio', role='access_admin')
        self.authority = User.objects.create_user(username='gestao.ficticia')
        self.secretary = User.objects.create_user(username='secretaria.ficticia')
        self.commercial = User.objects.create_user(username='comercial.ficticio')
        self.other = User.objects.create_user(username='outro.ficticio')
        services.initialize_business_authority(operator=self.technical, target=self.authority, approval_reference='Aprovação fictícia de teste')
        services.assign_department(actor=self.authority, target=self.secretary, department='secretariat', enabled=True)
        services.assign_department(actor=self.authority, target=self.commercial, department='commercial', enabled=True)

    def contact(self, actor=None, name='Pessoa fictícia Alfa'):
        return services.create_contact(actor=actor or self.secretary, operation_key=uuid.uuid4(), data={
            'kind': 'person', 'name': name, 'email': '', 'phone': '', 'channel_absence_reason': 'Contato presencial fictício',
        })

    def demand(self, actor=None, contact=None):
        return services.create_demand(actor=actor or self.secretary, operation_key=uuid.uuid4(), data={
            'contact': contact or self.contact(actor), 'title': 'Atendimento fictício', 'need': 'Avaliar necessidade informada',
            'origin': 'Presencial', 'area': '', 'next_step': 'Realizar triagem', 'next_step_on': None,
        })


class IntakeCreationTests(IntakeFixture):
    def test_technical_admin_and_authority_have_no_implicit_business_read(self):
        demand = self.demand()
        self.assertFalse(access.can_create(self.technical))
        self.assertEqual(access.visible_demands(self.technical).count(), 0)
        self.assertEqual(access.visible_demands(self.authority).count(), 0)
        with self.assertRaises(PermissionDenied):
            services.assign_department(actor=self.technical, target=self.technical, department='commercial', enabled=True)
        self.assertEqual(access.visible_contacts(self.other).count(), 0)

    def test_bootstrap_is_once_and_requires_explicit_approval_reference(self):
        with self.assertRaises(ValidationError):
            services.initialize_business_authority(operator=self.technical, target=self.other, approval_reference='')
        with self.assertRaises(ValidationError):
            services.initialize_business_authority(operator=self.technical, target=self.other, approval_reference='Outra aprovação fictícia')
        self.assertEqual(BusinessAuthority.objects.count(), 1)

    def test_contact_requires_name_and_channel_or_reason_in_domain(self):
        for data in [
            {'kind': 'person', 'name': '', 'email': '', 'phone': '', 'channel_absence_reason': 'Presencial'},
            {'kind': 'person', 'name': 'Pessoa fictícia', 'email': '', 'phone': '', 'channel_absence_reason': ''},
            {'kind': 'person', 'name': 'Pessoa fictícia', 'email': 'invalid', 'phone': '', 'channel_absence_reason': ''},
        ]:
            with self.subTest(data=data), self.assertRaises(ValidationError):
                services.create_contact(actor=self.secretary, operation_key=uuid.uuid4(), data=data)
        self.assertEqual(Contact.objects.count(), 0)

    def test_creator_gets_only_initial_contact_and_demand_scope(self):
        contact = self.contact()
        demand = self.demand(contact=contact)
        self.assertEqual(access.visible_contacts(self.secretary).count(), 1)
        self.assertEqual(access.visible_demands(self.secretary).count(), 1)
        self.assertEqual(set(DemandGrant.objects.filter(demand=demand).values_list('action', flat=True)), {'view', 'edit_intake', 'send_handoff', 'view_history'})
        self.assertEqual(demand.journey_stage, 'reception')
        self.assertEqual(demand.commercial_stage, 'triage')
        self.assertEqual(demand.responsible, self.secretary)
        self.assertTrue(DemandEvent.objects.filter(demand=demand, actor=self.secretary, action='demand.create').exists())
        from advpot.cases.models import Case
        self.assertEqual(Case.objects.count(), 0)

    def test_duplicate_warning_is_normalized_and_never_reveals_other_scope(self):
        contact = self.contact(name='  Pessoa   Fictícia Alfa  ')
        self.assertEqual(list(access.possible_duplicates(self.secretary, name='pessoa ficticia alfa')), [contact])
        self.assertEqual(list(access.possible_duplicates(self.commercial, name='pessoa ficticia alfa')), [])
        second = self.contact(name='Pessoa Fictícia Alfa')
        self.assertNotEqual(contact.pk, second.pk)

    def test_invisible_contact_cannot_be_reused_in_new_demand(self):
        contact = self.contact()
        with self.assertRaises(Http404):
            self.demand(actor=self.commercial, contact=contact)
        self.assertEqual(Demand.objects.count(), 0)

    def test_create_retries_do_not_duplicate_and_changed_payload_conflicts(self):
        contact = self.contact()
        key = uuid.uuid4()
        data = {'contact': contact, 'title': 'Demanda fictícia', 'need': 'Triagem', 'origin': 'Presencial', 'area': '', 'next_step': 'Diagnosticar', 'next_step_on': None}
        first = services.create_demand(actor=self.secretary, operation_key=key, data=data)
        again = services.create_demand(actor=self.secretary, operation_key=key, data=data)
        self.assertEqual(first.pk, again.pk)
        from advpot.intake.exceptions import WorkflowConflict
        with self.assertRaises(WorkflowConflict):
            services.create_demand(actor=self.secretary, operation_key=key, data={**data, 'title': 'Outro título'})
        self.assertEqual(Demand.objects.count(), 1)
        self.assertEqual(DemandEvent.objects.filter(action='demand.create').count(), 1)

    def test_scope_grant_does_not_grant_sector_or_other_contacts(self):
        demand = self.demand()
        services.grant_demand_action(actor=self.authority, target=self.other, demand_id=demand.pk, action='view', enabled=True)
        self.assertEqual(access.visible_demands(self.other).count(), 0)
        services.assign_department(actor=self.authority, target=self.other, department='commercial', enabled=True)
        self.assertEqual(access.visible_demands(self.other).count(), 1)
        self.assertEqual(access.visible_contacts(self.other).count(), 0)
