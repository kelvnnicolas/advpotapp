import uuid
import unicodedata
import hashlib
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def normalized_name(value):
    value = unicodedata.normalize('NFKD', value.strip().casefold())
    return ' '.join(''.join(c for c in value if not unicodedata.combining(c)).split())


def name_fingerprint(value):
    return hashlib.sha256(normalized_name(value).encode()).hexdigest()


class BusinessAuthority(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    approval_reference = models.CharField(max_length=250)
    configured_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.CheckConstraint(condition=models.Q(id=1), name='business_authority_singleton')]


class BusinessAssignment(models.Model):
    class Department(models.TextChoices):
        SECRETARIAT = 'secretariat', 'Secretaria'
        COMMERCIAL = 'commercial', 'Comercial'
        FINANCE = 'finance', 'Financeiro'
        OPERATIONAL = 'operational', 'Operacional'
        MANAGEMENT = 'management', 'Gestão'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    department = models.CharField(max_length=20, choices=Department.choices)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'department'], name='unique_business_department')]


class RecoveryQueue(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    name = models.CharField(max_length=100, default='Gestão — recuperar responsabilidade')


class Contact(models.Model):
    class Kind(models.TextChoices):
        PERSON = 'person', 'Pessoa'
        ORGANIZATION = 'organization', 'Organização'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kind = models.CharField('Tipo', max_length=15, choices=Kind.choices)
    name = models.CharField('Nome', max_length=150)
    name_key = models.CharField(max_length=64, editable=False, db_index=True)
    email = models.EmailField('E-mail', blank=True)
    phone = models.CharField('Telefone', max_length=40, blank=True)
    channel_absence_reason = models.CharField('Motivo da ausência de contato', max_length=300, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    version = models.PositiveIntegerField(default=1)
    creation_key = models.UUIDField(unique=True, editable=False)
    creation_hash = models.CharField(max_length=64, editable=False)

    class Meta:
        ordering = ['name', 'pk']

    def clean(self):
        self.name = self.name.strip()
        self.name_key = name_fingerprint(self.name)
        if not self.name:
            raise ValidationError({'name': 'Informe o nome.'})
        if not (self.email.strip() or self.phone.strip() or self.channel_absence_reason.strip()):
            raise ValidationError({'channel_absence_reason': 'Informe um canal de contato ou justifique sua ausência.'})


class ContactGrant(models.Model):
    class Action(models.TextChoices):
        VIEW = 'view', 'Consultar cadastro'
        EDIT = 'edit', 'Editar cadastro'
        VIEW_HISTORY = 'view_history', 'Consultar histórico cadastral'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT)
    action = models.CharField(max_length=24, choices=Action.choices)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'contact', 'action'], name='unique_contact_action')]


class Demand(models.Model):
    class Journey(models.TextChoices):
        RECEPTION = 'reception', 'Secretaria · Recepção'
        COMMERCIAL = 'commercial', 'Comercial · Atendimento'

    class Stage(models.TextChoices):
        TRIAGE = 'triage', 'Triagem'
        DIAGNOSIS = 'diagnosis', 'Diagnóstico'
        PROPOSAL = 'proposal', 'Proposta'
        FORMALIZATION = 'formalization', 'Preparar formalização'

    class Status(models.TextChoices):
        OPEN = 'open', 'Aberta'
        LOST = 'lost', 'Perdida'
        CANCELLED = 'cancelled', 'Cancelada'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT)
    title = models.CharField('Título', max_length=180)
    need = models.TextField('Necessidade', max_length=2000)
    origin = models.CharField('Origem', max_length=100)
    area = models.CharField('Área', max_length=100, blank=True)
    next_step = models.CharField('Próximo passo', max_length=250)
    next_step_on = models.DateField('Data do próximo passo', null=True, blank=True)
    solution = models.TextField('Solução proposta', max_length=1500, blank=True)
    proposal = models.TextField('Resumo da proposta', max_length=1500, blank=True)
    journey_stage = models.CharField(max_length=20, choices=Journey.choices, default=Journey.RECEPTION)
    commercial_stage = models.CharField(max_length=20, choices=Stage.choices, default=Stage.TRIAGE)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.OPEN)
    closing_reason = models.CharField(max_length=500, blank=True)
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name='+')
    recovery_queue = models.ForeignKey(RecoveryQueue, null=True, blank=True, on_delete=models.PROTECT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    version = models.PositiveIntegerField(default=1)
    creation_key = models.UUIDField(unique=True, editable=False)
    creation_hash = models.CharField(max_length=64, editable=False)

    class Meta:
        ordering = ['-created_at', 'pk']
        constraints = [models.CheckConstraint(condition=(models.Q(responsible__isnull=False, recovery_queue__isnull=True) | models.Q(responsible__isnull=True, recovery_queue__isnull=False)), name='demand_person_or_recovery_queue')]

    def clean(self):
        errors = {}
        for field in ['title', 'need', 'origin', 'next_step']:
            setattr(self, field, getattr(self, field).strip())
            if not getattr(self, field):
                errors[field] = 'Este campo é obrigatório.'
        if errors:
            raise ValidationError(errors)


class ContactEvent(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    action = models.CharField(max_length=50)
    changes = models.JSONField(default=dict, blank=True)
    occurred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-occurred_at', '-pk']


class DemandGrant(models.Model):
    class Action(models.TextChoices):
        VIEW = 'view', 'Consultar demanda'
        EDIT_INTAKE = 'edit_intake', 'Editar recepção'
        MANAGE_OPPORTUNITY = 'manage_opportunity', 'Conduzir atendimento comercial'
        VIEW_HISTORY = 'view_history', 'Consultar histórico'
        SEND_HANDOFF = 'send_handoff', 'Encaminhar ao Comercial'
        RECEIVE_HANDOFF = 'receive_handoff', 'Receber passagem'
        RECOVER = 'recover', 'Recuperar responsabilidade'
        MANAGE_ACCESS = 'manage_access', 'Delegar acesso da demanda'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    demand = models.ForeignKey(Demand, on_delete=models.PROTECT)
    action = models.CharField(max_length=30, choices=Action.choices)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'demand', 'action'], name='unique_demand_action')]


class DemandEvent(models.Model):
    demand = models.ForeignKey(Demand, on_delete=models.PROTECT)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    action = models.CharField(max_length=50)
    previous_value = models.CharField(max_length=80, blank=True)
    new_value = models.CharField(max_length=80, blank=True)
    reason = models.CharField(max_length=500, blank=True)
    version = models.PositiveIntegerField()
    changes = models.JSONField(default=dict, blank=True)
    occurred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-occurred_at', '-pk']


class CommercialHandoff(models.Model):
    class State(models.TextChoices):
        PENDING = 'pending', 'Aguardando recebimento'
        ACCEPTED = 'accepted', 'Aceita'
        RETURNED = 'returned', 'Devolvida'
        CANCELLED = 'cancelled', 'Cancelada'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    demand = models.ForeignKey(Demand, on_delete=models.PROTECT)
    target = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='+')
    sent_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='+')
    state = models.CharField(max_length=15, choices=State.choices, default=State.PENDING)
    blocked = models.BooleanField(default=False)
    reason = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(null=True)
    operation_key = models.UUIDField(unique=True)
    operation_hash = models.CharField(max_length=64)

    class Meta:
        ordering = ['created_at', 'pk']
        constraints = [models.UniqueConstraint(fields=['demand'], condition=models.Q(state='pending'), name='one_pending_commercial_handoff')]


class CommandReceipt(models.Model):
    key = models.UUIDField(primary_key=True)
    demand = models.ForeignKey(Demand, on_delete=models.PROTECT)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    action = models.CharField(max_length=50)
    request_hash = models.CharField(max_length=64)
    result_version = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
