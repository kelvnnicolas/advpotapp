from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError, transaction
from advpot.audit.services import record
from .models import User


def require_access_admin(actor, extra_ids=()):
    # Reload on commands: stale forms cannot retain revoked permissions.
    accounts = {user.pk: user for user in User.objects.filter(pk__in={actor.pk, *extra_ids}).order_by('pk').select_for_update()}
    actor = accounts[actor.pk]
    if not actor.can_manage_identity:
        raise PermissionDenied
    return actor


@transaction.atomic
def create_internal_user(*, actor, form):
    actor = require_access_admin(actor)
    account = form.save(commit=False)
    account.is_staff = account.is_superuser = False
    try:
        with transaction.atomic():
            account.save()
    except IntegrityError:
        if User.objects.filter(username=account.username).exists():
            raise ValidationError({'username': 'Este nome de usuário já está em uso.'}) from None
        raise
    record(actor=actor, action='identity.create', target=account.pk)
    return account


@transaction.atomic
def update_internal_user(*, actor, user_id, changes):
    actor = require_access_admin(actor, [user_id])
    account = User.objects.select_for_update().get(pk=user_id)
    if account.pk == actor.pk and (not changes['is_active'] or changes['role'] != User.Role.ACCESS_ADMIN):
        raise ValidationError('Você não pode desativar nem remover seu próprio perfil de administração.')
    old_active, old_role = account.is_active, account.role
    for field in ['first_name', 'last_name', 'role', 'is_active']:
        setattr(account, field, changes[field])
    if old_active != account.is_active or old_role != account.role:
        account.session_version += 1
    account.save(update_fields=['first_name', 'last_name', 'role', 'is_active', 'session_version'])
    if old_active and not account.is_active:
        from advpot.intake.workflow import recover_if_unable
        recover_if_unable(actor=actor, user=account)
    if old_active != account.is_active:
        action = 'identity.enable' if account.is_active else 'identity.disable'
        record(actor=actor, action=action, target=account.pk)
    if old_role != account.role:
        record(actor=actor, action=f'identity.role.{old_role}.{account.role}', target=account.pk)
    record(actor=actor, action='identity.update', target=account.pk)
    return account


@transaction.atomic
def revoke_sessions(*, actor, user_id):
    actor = require_access_admin(actor, [user_id])
    account = User.objects.select_for_update().get(pk=user_id)
    account.session_version += 1
    account.save(update_fields=['session_version'])
    record(actor=actor, action='identity.revoke_sessions', target=account.pk)
