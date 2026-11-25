import hashlib
import json
import uuid
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from advpot.audit.services import record
from advpot.identity.models import IdentitySetupLock, User
from . import access
from .exceptions import WorkflowConflict
from .models import BusinessAuthority, BusinessAssignment, Contact, ContactGrant, ContactEvent, Demand, DemandGrant, DemandEvent, RecoveryQueue


def lock_actor(actor, extra_ids=()):
    if not actor.is_authenticated:
        raise PermissionDenied
    locked = {user.pk: user for user in User.objects.filter(pk__in={actor.pk, *extra_ids}).order_by('pk').select_for_update()}
    account = locked.get(actor.pk)
    if not account:
        raise PermissionDenied
    if not account.is_active:
        raise PermissionDenied
    return account


def fingerprint(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, default=str, ensure_ascii=False).encode()).hexdigest()


def validate_key(value):
    try:
        return uuid.UUID(str(value))
    except (ValueError, TypeError, AttributeError):
        raise ValidationError('Operação inválida. Reabra o formulário.') from None


def require_authority(actor, extra_ids=()):
    actor = lock_actor(actor, extra_ids)
    if not access.is_authority(actor):
        raise PermissionDenied
    return actor


def event(*, actor, demand, action, previous='', new='', reason='', changes=None):
    DemandEvent.objects.create(demand=demand, actor=actor, action=action, previous_value=str(previous), new_value=str(new), reason=reason, changes=changes or {}, version=demand.version)
    record(actor=actor, action=action, target=demand.pk)


@transaction.atomic
def initialize_business_authority(*, operator, target, approval_reference):
    operator = lock_actor(operator, [target.pk])
    if not operator.can_manage_identity:
        raise PermissionDenied
    reference = approval_reference.strip()
    if not reference or len(reference) > 250:
        raise ValidationError('Informe a referência da autorização da gestão, com até 250 caracteres.')
    target = User.objects.select_for_update().get(pk=target.pk)
    if not target.is_active:
        raise ValidationError('A pessoa indicada deve ter conta ativa.')
    IdentitySetupLock.objects.get_or_create(pk=1)
    IdentitySetupLock.objects.select_for_update().get(pk=1)
    if BusinessAuthority.objects.exists():
        raise ValidationError('A autoridade inicial já foi configurada.')
    authority = BusinessAuthority.objects.create(pk=1, user=target, configured_by=operator, approval_reference=reference)
    RecoveryQueue.objects.get_or_create(pk=1)
    record(actor=operator, action='business.bootstrap', target=target.pk)
    return authority


@transaction.atomic
def assign_department(*, actor, target, department, enabled):
    actor = require_authority(actor, [target.pk])
    target = User.objects.select_for_update().get(pk=target.pk)
    if department not in BusinessAssignment.Department.values or not target.is_active:
        raise ValidationError('Setor ou usuário inválido.')
    if enabled:
        BusinessAssignment.objects.get_or_create(user=target, department=department)
    else:
        from .workflow import require_no_owned_work
        require_no_owned_work(target, department=department)
        BusinessAssignment.objects.filter(user=target, department=department).delete()
    record(actor=actor, action=f'business.department.{"grant" if enabled else "revoke"}.{department}', target=target.pk)


@transaction.atomic
def grant_contact_action(*, actor, target, contact_id, action, enabled):
    actor = require_authority(actor, [target.pk])
    target = User.objects.select_for_update().get(pk=target.pk)
    contact = get_object_or_404(Contact, pk=contact_id)
    if action not in ContactGrant.Action.values or not target.is_active:
        raise ValidationError('Ação ou usuário inválido.')
    if enabled:
        ContactGrant.objects.get_or_create(user=target, contact=contact, action=action)
    else:
        ContactGrant.objects.filter(user=target, contact=contact, action=action).delete()
    record(actor=actor, action=f'contact.access.{"grant" if enabled else "revoke"}.{action}', target=contact.pk)


@transaction.atomic
def grant_demand_action(*, actor, target, demand_id, action, enabled):
    actor = lock_actor(actor, [target.pk])
    if not access.is_authority(actor) and not access.visible_demands(actor, 'manage_access').filter(pk=demand_id).exists():
        raise PermissionDenied
    target = User.objects.select_for_update().get(pk=target.pk)
    demand = get_object_or_404(Demand.objects.select_for_update(), pk=demand_id)
    if action not in DemandGrant.Action.values or not target.is_active:
        raise ValidationError('Ação ou usuário inválido.')
    # Delegates cannot delegate authority or grant actions they do not possess.
    if not access.is_authority(actor) and (action in {'manage_access', 'recover'} or not DemandGrant.objects.filter(user=actor, demand=demand, action=action).exists()):
        raise PermissionDenied
    if enabled:
        DemandGrant.objects.get_or_create(user=target, demand=demand, action=action)
    else:
        DemandGrant.objects.filter(user=target, demand=demand, action=action).delete()
        from .workflow import recover_if_unable
        recover_if_unable(actor=actor, user=target, demands=[demand])
    record(actor=actor, action=f'demand.access.{"grant" if enabled else "revoke"}.{action}', target=demand.pk)


def existing_operation(model, *, key, actor, digest):
    instance = model.objects.filter(creation_key=key).first()
    if instance and (instance.created_by_id != actor.pk or instance.creation_hash != digest):
        raise WorkflowConflict('Esta operação já foi usada com outros dados.')
    return instance


@transaction.atomic
def create_contact(*, actor, operation_key, data):
    actor = lock_actor(actor)
    if not access.can_create(actor):
        raise PermissionDenied
    key = validate_key(operation_key)
    fields = {field: data.get(field, '').strip() for field in ['kind', 'name', 'email', 'phone', 'channel_absence_reason']}
    digest = fingerprint(fields)
    existing = existing_operation(Contact, key=key, actor=actor, digest=digest)
    if existing:
        return get_object_or_404(access.visible_contacts(actor), pk=existing.pk)
    contact = Contact(**fields, created_by=actor, creation_key=key, creation_hash=digest)
    contact.full_clean()
    contact.save()
    ContactGrant.objects.bulk_create([ContactGrant(user=actor, contact=contact, action=action) for action in ['view', 'edit', 'view_history']])
    ContactEvent.objects.create(contact=contact, actor=actor, action='contact.create')
    record(actor=actor, action='contact.create', target=contact.pk)
    return contact


@transaction.atomic
def create_demand(*, actor, operation_key, data):
    actor = lock_actor(actor)
    if not access.can_create(actor):
        raise PermissionDenied
    key = validate_key(operation_key)
    contact = get_object_or_404(access.visible_contacts(actor), pk=data['contact'].pk)
    fields = {field: data.get(field, '').strip() for field in ['title', 'need', 'origin', 'area', 'next_step']}
    fields['next_step_on'] = data.get('next_step_on')
    digest = fingerprint({**fields, 'contact_id': str(contact.pk)})
    existing = existing_operation(Demand, key=key, actor=actor, digest=digest)
    if existing:
        return get_object_or_404(access.visible_demands(actor), pk=existing.pk)
    demand = Demand(**fields, contact=contact, responsible=actor, created_by=actor, creation_key=key, creation_hash=digest)
    demand.full_clean()
    demand.save()
    DemandGrant.objects.bulk_create([DemandGrant(user=actor, demand=demand, action=action) for action in ['view', 'edit_intake', 'send_handoff', 'view_history']])
    event(actor=actor, demand=demand, action='demand.create', new='reception')
    return demand


@transaction.atomic
def update_contact(*, actor, contact_id, expected_version, data):
    actor = lock_actor(actor)
    contact = get_object_or_404(access.visible_contacts(actor, 'edit').select_for_update(), pk=contact_id)
    if contact.version != expected_version:
        raise WorkflowConflict('Este cadastro foi atualizado. Recarregue para continuar.')
    changes = {}
    for field in ['kind', 'name', 'email', 'phone', 'channel_absence_reason']:
        before, after = getattr(contact, field), data[field].strip()
        if before != after:
            changes[field] = {'before': before, 'after': after}
            setattr(contact, field, after)
    contact.full_clean()
    contact.version += 1
    contact.save()
    ContactEvent.objects.create(contact=contact, actor=actor, action='contact.update', changes=changes)
    record(actor=actor, action='contact.update', target=contact.pk)
    return contact
