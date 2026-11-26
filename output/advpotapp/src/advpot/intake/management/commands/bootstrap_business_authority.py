import sys
from getpass import getpass
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.management.base import BaseCommand, CommandError
from advpot.identity.models import User
from advpot.intake.services import initialize_business_authority


class Command(BaseCommand):
    help = 'Designa a primeira autoridade de negócio por indicação expressa da gestão; sem leitura automática.'

    def handle(self, *args, **options):
        if not sys.stdin.isatty():
            raise CommandError('Use um terminal interativo.')
        username = input('Administrador técnico executor: ').strip()
        operator = User.objects.filter(username=username, is_active=True).first()
        password = getpass('Senha do executor (não exibida): ')
        if not operator or not operator.check_password(password) or not operator.can_manage_identity:
            raise CommandError('Não foi possível autorizar o procedimento.')
        target = User.objects.filter(username=input('Usuário indicado pela gestão: ').strip(), is_active=True).first()
        if not target:
            raise CommandError('A pessoa indicada precisa de conta interna ativa.')
        reference = input('Referência da autorização expressa: ').strip()
        try:
            initialize_business_authority(operator=operator, target=target, approval_reference=reference)
        except (ValidationError, PermissionDenied) as error:
            raise CommandError('; '.join(error.messages) if isinstance(error, ValidationError) else 'Acesso negado.') from error
        self.stdout.write(self.style.SUCCESS('Autoridade inicial registrada, sem leitura automática de demandas ou casos.'))
