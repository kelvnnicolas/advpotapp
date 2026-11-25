from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class AuditEvent(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT)
    action = models.CharField(max_length=64)
    target = models.CharField(max_length=100, blank=True)
    occurred_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-occurred_at', '-pk']

    def save(self, *args, **kwargs):
        if not self._state.adding:
            raise ValidationError('O histórico não pode ser editado.')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError('O histórico não pode ser excluído.')
