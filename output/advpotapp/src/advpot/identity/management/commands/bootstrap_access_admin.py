from getpass import getpass
import sys
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from advpot.audit.services import record
from advpot.identity.models import IdentitySetupLock, User


class Command(BaseCommand):
    help = 'Cria o primeiro administrador interno, sem superusuário; exige terminal interativo.'

    def handle(self, *args, **options):
        if not sys.stdin.isatty():
            raise CommandError('Este procedimento exige um terminal interativo; senha não aceita por entrada redirecionada.')
        username = input('Nome de usuário: ').strip()
        password = getpass('Senha (não exibida): ')
        if password != getpass('Confirme a senha: '):
            raise CommandError('As senhas não conferem.')
        account = User(username=username, role=User.Role.ACCESS_ADMIN, is_staff=False, is_superuser=False)
        try:
            account.full_clean(exclude=['password'])
            validate_password(password, account)
        except ValidationError as error:
            raise CommandError('; '.join(error.messages)) from error
        with transaction.atomic():
            IdentitySetupLock.objects.get_or_create(pk=1)
            IdentitySetupLock.objects.select_for_update().get(pk=1)
            if User.objects.filter(role=User.Role.ACCESS_ADMIN, is_active=True).exists():
                raise CommandError('Já existe administrador ativo. Use a administração interna.')
            account.set_password(password)
            account.save()
            record(actor=None, action='identity.bootstrap', target=account.pk)
        self.stdout.write(self.style.SUCCESS('Administrador interno criado, sem acesso implícito a casos.'))
