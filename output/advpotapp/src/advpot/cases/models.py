import uuid
from django.conf import settings
from django.db import models


class Case(models.Model):
    """Minimal M1 envelope, not the M2 legal workflow."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Título', max_length=180)
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', 'pk']


class CaseGrant(models.Model):
    class Action(models.TextChoices):
        VIEW = 'view', 'Visualizar'
        EXPORT = 'export', 'Exportar'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    case = models.ForeignKey(Case, on_delete=models.PROTECT, related_name='grants')
    action = models.CharField(max_length=12, choices=Action.choices)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'case', 'action'], name='unique_case_action_grant')]
