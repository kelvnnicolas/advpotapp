from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        OPERATOR = 'operator', 'Profissional'
        ACCESS_ADMIN = 'access_admin', 'Administrador de acessos'
        AUDITOR = 'auditor', 'Auditor'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.OPERATOR)
    session_version = models.PositiveIntegerField(default=1, editable=False)

    @property
    def can_manage_identity(self):
        return self.is_active and self.role == self.Role.ACCESS_ADMIN

    @property
    def can_read_audit(self):
        return self.is_active and self.role == self.Role.AUDITOR


class LoginBucket(models.Model):
    # Keyed digests, never raw usernames, IP addresses or credentials.
    key = models.CharField(max_length=64, unique=True)
    attempts = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(default=timezone.now)


class IdentitySetupLock(models.Model):
    """Single durable row to serialize first-administrator bootstrap."""
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)

    class Meta:
        constraints = [models.CheckConstraint(condition=models.Q(id=1), name='identity_setup_singleton')]
