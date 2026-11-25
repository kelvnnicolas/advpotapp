from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from advpot.identity.models import LoginBucket


class Command(BaseCommand):
    help = 'Remove contadores de login sem atividade na última janela de 24 horas.'

    def handle(self, *args, **options):
        count, _ = LoginBucket.objects.filter(started_at__lt=timezone.now() - timedelta(hours=24)).delete()
        self.stdout.write(f'{count} contadores expirados removidos.')
