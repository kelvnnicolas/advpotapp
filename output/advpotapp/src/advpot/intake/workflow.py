from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from advpot.identity.models import User
from . import access
from .exceptions import WorkflowConflict
from .models import BusinessAssignment, BusinessAuthority, CommandReceipt, CommercialHandoff, Demand, DemandGrant, RecoveryQueue
from .services import event, fingerprint, lock_actor, validate_key


def _begin(*, actor, demand_id, action, permission, expected_version, operation_key, payload, extra_users=(), recovery=False):
    actor = lock_actor(actor, extra_users)
    if recovery:
        if not access.is_authority(actor) and not ('management' in access.departments(actor) and DemandGrant.objects.filter(user=actor, demand_id=demand_id, action='recover').exists()):
            raise PermissionDenied
        demand = get_object_or_404(Demand.objects.select_for_update(), pk=demand_id)
    else:
        demand = get_object_or_404(access.visible_demands(actor, permission).select_for_update(), pk=demand_id)
    key = validate_key(operation_key)
    digest = fingerprint(payload)
    receipt = CommandReceipt.objects.filter(key=key).first()
    if receipt:
        if receipt.actor_id != actor.pk or receipt.demand_id != demand.pk or receipt.action != action or receipt.request_hash != digest:
            raise WorkflowConflict('Esta operação já foi usada com outros dados.')
        return actor, demand, key, digest, True
    if demand.version != expected_version:
        raise WorkflowConflict('Este registro foi atualizado. Recarregue para continuar.')
    return actor, demand, key, digest, False


def _finish(*, actor, demand, key, digest, action, previous='', new='', reason='', changes=None):
    demand.version += 1
    demand.full_clean()
    demand.save()
    event(actor=actor, demand=demand, action=action, previous=previous, new=new, reason=reason, changes=changes)
    CommandReceipt.objects.create(key=key, demand=demand, actor=actor, action=action, request_hash=digest, result_version=demand.version)


def _owned_open(actor, demand):
    if demand.status != 'open':
        raise ValidationError('Este atendimento já foi finalizado.')
    if demand.responsible_id != actor.pk or demand.recovery_queue_id:
        raise PermissionDenied('A ação exige o responsável atual.')


def _no_pending(demand):
    if CommercialHandoff.objects.filter(demand=demand, state='pending').exists():
        raise WorkflowConflict('Existe uma passagem aguardando recebimento. Cancele o pedido antes de alterar a demanda.')


def _can_execute(user, demand, *, reception=False):
    required = 'edit_intake' if reception else 'manage_opportunity'
    return user.is_active and access.visible_demands(user, required).filter(pk=demand.pk).exists()


@transaction.atomic
def update_demand(*, actor, demand_id, expected_version, operation_key, data):
    # Determine action from the authorized record, never from the client's role hint.
    initial = get_object_or_404(access.visible_demands(actor), pk=demand_id)
    permission = 'edit_intake' if initial.journey_stage == 'reception' else 'manage_opportunity'
    actor, demand, key, digest, replay = _begin(actor=actor, demand_id=demand_id, action='demand.update', permission=permission, expected_version=expected_version, operation_key=operation_key, payload=data)
    if replay:
        return demand
    _owned_open(actor, demand)
    _no_pending(demand)
    allowed = ['next_step', 'next_step_on']
    if demand.journey_stage == 'reception':
        if {'solution', 'proposal'} & data.keys():
            raise ValidationError('Solução e proposta são registradas pelo Comercial após o aceite.')
        allowed += ['title', 'need', 'origin', 'area']
    else:
        allowed += ['solution', 'proposal']
    changes = {}
    for field in allowed:
        if field in data:
            before, after = getattr(demand, field), data[field]
            if before != after:
                changes[field] = {'before': str(before) if before is not None else None, 'after': str(after) if after is not None else None}
                setattr(demand, field, after)
    _finish(actor=actor, demand=demand, key=key, digest=digest, action='demand.update', changes=changes)
    return demand


@transaction.atomic
def move_commercial_stage(*, actor, demand_id, stage, reason, expected_version, operation_key):
    actor, demand, key, digest, replay = _begin(actor=actor, demand_id=demand_id, action='commercial.move', permission='manage_opportunity', expected_version=expected_version, operation_key=operation_key, payload={'stage': stage, 'reason': reason})
    if replay:
        return demand
    _owned_open(actor, demand)
    _no_pending(demand)
    if demand.journey_stage != 'commercial':
        raise ValidationError('O Comercial precisa aceitar a passagem antes de conduzir o atendimento.')
    previous = demand.commercial_stage
    if stage in {'lost', 'cancelled'}:
        reason = reason.strip()
        if not reason or len(reason) > 500:
            raise ValidationError('Informe um motivo com até 500 caracteres.')
        demand.status, demand.closing_reason = stage, reason
    else:
        allowed = {'diagnosis': 'proposal', 'proposal': 'formalization'}
        if allowed.get(previous) != stage:
            raise ValidationError('A passagem solicitada não está habilitada neste lote.')
        if stage == 'proposal' and not demand.solution.strip():
            raise ValidationError('Registre a solução antes de apresentar a proposta.')
        if stage == 'formalization' and not demand.proposal.strip():
            raise ValidationError('Registre o resumo da proposta antes de preparar a formalização.')
        demand.commercial_stage = stage
    _finish(actor=actor, demand=demand, key=key, digest=digest, action='commercial.move', previous=previous, new=stage, reason=reason)
    return demand


@transaction.atomic
def send_to_commercial(*, actor, demand_id, target_id, expected_version, operation_key):
    actor, demand, key, digest, replay = _begin(actor=actor, demand_id=demand_id, action='handoff.send', permission='send_handoff', expected_version=expected_version, operation_key=operation_key, payload={'target': target_id}, extra_users=[target_id])
    if replay:
        return CommercialHandoff.objects.get(operation_key=key)
    _owned_open(actor, demand)
    _no_pending(demand)
    if demand.journey_stage != 'reception':
        raise ValidationError('Só está habilitada a passagem da recepção ao Comercial.')
    target = User.objects.filter(pk=target_id, is_active=True).first()
    required = {'view', 'receive_handoff', 'manage_opportunity'}
    granted = set(DemandGrant.objects.filter(demand=demand, user_id=target_id).values_list('action', flat=True))
    if not target or 'commercial' not in access.departments(target) or not required.issubset(granted):
        raise ValidationError('O destinatário precisa de setor Comercial e concessões de leitura, recebimento e condução desta demanda.')
    handoff = CommercialHandoff.objects.create(demand=demand, target=target, sent_by=actor, operation_key=key, operation_hash=digest)
    _finish(actor=actor, demand=demand, key=key, digest=digest, action='handoff.send', new=target.pk)
    return handoff


def _received_command(*, actor, handoff_id, expected_version, operation_key, action, reason=''):
    initial = get_object_or_404(CommercialHandoff, pk=handoff_id, target=actor)
    actor, demand, key, digest, replay = _begin(actor=actor, demand_id=initial.demand_id, action=action, permission='receive_handoff', expected_version=expected_version, operation_key=operation_key, payload={'handoff': str(handoff_id), 'reason': reason})
    handoff = CommercialHandoff.objects.select_for_update().get(pk=handoff_id)
    if replay:
        return demand
    if 'commercial' not in access.departments(actor) or handoff.state != 'pending' or handoff.blocked or demand.recovery_queue_id:
        raise WorkflowConflict('Esta passagem não está disponível para recebimento.')
    if not _can_execute(actor, demand):
        raise ValidationError('A concessão comercial necessária foi revogada.')
    if action == 'handoff.accept':
        previous = demand.responsible_id
        demand.responsible = actor
        demand.journey_stage = 'commercial'
        demand.commercial_stage = 'diagnosis'
        handoff.state = 'accepted'
    else:
        reason = reason.strip()
        if not reason or len(reason) > 500:
            raise ValidationError('Informe o motivo da devolução com até 500 caracteres.')
        previous = 'pending'
        handoff.state, handoff.reason = 'returned', reason
    handoff.decided_at = timezone.now()
    handoff.save(update_fields=['state', 'reason', 'decided_at'])
    _finish(actor=actor, demand=demand, key=key, digest=digest, action=action, previous=previous, new=actor.pk if action == 'handoff.accept' else 'returned', reason=reason)
    return demand


@transaction.atomic
def accept_handoff(**kwargs):
    return _received_command(**kwargs, action='handoff.accept')


@transaction.atomic
def return_handoff(**kwargs):
    return _received_command(**kwargs, action='handoff.return')


@transaction.atomic
def cancel_handoff(*, actor, demand_id, expected_version, operation_key, reason):
    actor, demand, key, digest, replay = _begin(actor=actor, demand_id=demand_id, action='handoff.cancel', permission='send_handoff', expected_version=expected_version, operation_key=operation_key, payload={'reason': reason})
    if replay:
        return demand
    _owned_open(actor, demand)
    if not reason.strip() or len(reason) > 500:
        raise ValidationError('Informe o motivo do cancelamento.')
    handoff = get_object_or_404(CommercialHandoff.objects.select_for_update(), demand=demand, state='pending')
    handoff.state, handoff.reason, handoff.decided_at = 'cancelled', reason.strip(), timezone.now()
    handoff.save(update_fields=['state', 'reason', 'decided_at'])
    _finish(actor=actor, demand=demand, key=key, digest=digest, action='handoff.cancel', new='cancelled', reason=reason.strip())
    return demand


def require_no_owned_work(user, *, department):
    stage = {'secretariat': 'reception', 'commercial': 'commercial'}.get(department)
    if stage and Demand.objects.filter(responsible=user, status='open', journey_stage=stage).exists():
        raise ValidationError('Reassocie as demandas abertas antes de retirar o setor.')
    if department == 'commercial' and CommercialHandoff.objects.filter(target=user, state='pending').exists():
        raise ValidationError('Há passagens aguardando esse destinatário. Reorganize-as antes de retirar o setor.')
    if department == 'commercial' and 'secretariat' not in access.departments(user) and Demand.objects.filter(responsible=user, created_by=user, status='open', journey_stage='reception').exists():
        raise ValidationError('Reassocie suas demandas de entrada antes de retirar o setor.')


def recover_if_unable(*, actor, user, demands=None):
    queryset = Demand.objects.filter(responsible=user, status='open').order_by('pk')
    if demands is not None:
        queryset = queryset.filter(pk__in=[d.pk for d in demands])
    for demand in queryset.select_for_update():
        if _can_execute(user, demand, reception=demand.journey_stage == 'reception'):
            continue
        previous = demand.responsible_id
        queue, _ = RecoveryQueue.objects.get_or_create(pk=1)
        demand.responsible, demand.recovery_queue = None, queue
        demand.version += 1
        demand.save(update_fields=['responsible', 'recovery_queue', 'version'])
        # A department alone never designates a recovery manager. Existing
        # per-demand recovery grants remain; only the initial authority is added.
        recipients = set(BusinessAuthority.objects.filter(user__is_active=True).values_list('user_id', flat=True))
        for recipient in recipients:
            DemandGrant.objects.get_or_create(user_id=recipient, demand=demand, action='recover')
        CommercialHandoff.objects.filter(demand=demand, state='pending').update(blocked=True)
        event(actor=actor, demand=demand, action='demand.recovery', previous=previous, new='recovery_queue')
    # A target that lost access must not revive a pending acceptance upon reactivation.
    for pending in CommercialHandoff.objects.filter(target=user, state='pending', blocked=False).select_related('demand'):
        actions = set(DemandGrant.objects.filter(user=user, demand=pending.demand).values_list('action', flat=True))
        if not user.is_active or 'commercial' not in access.departments(user) or not {'view', 'receive_handoff', 'manage_opportunity'}.issubset(actions):
            CommercialHandoff.objects.filter(pk=pending.pk).update(blocked=True)


@transaction.atomic
def recover_demand(*, actor, demand_id, target_id, expected_version, operation_key):
    actor, demand, key, digest, replay = _begin(actor=actor, demand_id=demand_id, action='demand.reassign', permission='recover', expected_version=expected_version, operation_key=operation_key, payload={'target': target_id}, extra_users=[target_id], recovery=True)
    if replay:
        return demand
    if not demand.recovery_queue_id:
        raise ValidationError('Esta demanda não está na fila de recuperação.')
    target = get_object_or_404(User, pk=target_id)
    if not access.recovery_candidates(demand).filter(pk=target.pk).exists():
        raise ValidationError('O novo responsável precisa de setor, leitura e ação adequados à etapa.')
    demand.responsible, demand.recovery_queue = target, None
    for handoff in CommercialHandoff.objects.filter(demand=demand, state='pending').select_for_update():
        handoff.state = 'cancelled'
        handoff.blocked = True
        handoff.reason = 'Passagem encerrada na recuperação de responsabilidade; novo encaminhamento necessário.'
        handoff.decided_at = timezone.now()
        handoff.save(update_fields=['state', 'blocked', 'reason', 'decided_at'])
        event(actor=actor, demand=demand, action='handoff.recovery_cancel', previous='pending', new='cancelled', reason=handoff.reason)
    _finish(actor=actor, demand=demand, key=key, digest=digest, action='demand.reassign', previous='recovery_queue', new=target.pk)
    return demand
