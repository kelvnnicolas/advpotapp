from .models import AuditEvent


def record(*, actor, action, target=''):
    return AuditEvent.objects.create(actor=actor, action=action, target=str(target))
