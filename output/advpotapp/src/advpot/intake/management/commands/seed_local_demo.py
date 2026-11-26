"""Explicit, local-only synthetic fixture. Not an importer or authority bootstrap."""
import json
import uuid
from datetime import date
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from advpot.audit.services import record
from advpot.identity.models import User
from advpot.cases.models import Case, CaseGrant
from advpot.intake import services, workflow
from advpot.intake.models import BusinessAssignment, ContactGrant, Demand, DemandGrant


VERSION = 'advpot.local-demo.v1'


def key(entity, code):
    return uuid.uuid5(uuid.NAMESPACE_URL, f'urn:{VERSION}:{entity}:{code}')


class Command(BaseCommand):
    help = 'Carrega 6 contatos, 8 demandas e 3 envelopes fictícios para a conta teste, somente localmente.'

    @transaction.atomic
    def handle(self, *args, **options):
        database = settings.DATABASES['default']
        local_database = database['ENGINE'] == 'django.db.backends.sqlite3' or database.get('HOST') in {'127.0.0.1', 'localhost'}
        if not settings.DEBUG or not local_database:
            raise CommandError('Carga permitida apenas em desenvolvimento local; nenhuma alteração executada.')
        actor = User.objects.select_for_update().filter(username='teste', is_active=True, role='operator', is_staff=False, is_superuser=False).first()
        if not actor:
            raise CommandError('A conta teste deve existir, estar ativa e não possuir privilégios administrativos. A senha não é criada nem alterada por esta carga.')
        source = Path(__file__).resolve().parents[2] / 'data' / 'local_demo_v1.json'
        fixture = json.loads(source.read_text(encoding='utf-8'))
        if fixture.get('schema') != VERSION or fixture.get('synthetic') is not True:
            raise CommandError('Pacote demonstrativo inválido.')
        reception, new_actor = User.objects.get_or_create(username='demo.recepcao', defaults={'first_name': 'Recepção fictícia', 'role': 'operator'})
        if new_actor:
            reception.set_unusable_password()
            reception.save(update_fields=['password'])
        if not reception.is_active or reception.role != 'operator' or reception.is_staff or reception.is_superuser or reception.has_usable_password():
            raise CommandError('Conta auxiliar incompatível; carga cancelada sem alterações.')
        for account, departments in [(actor, ['secretariat', 'commercial']), (reception, ['secretariat'])]:
            for department in departments:
                _, created = BusinessAssignment.objects.get_or_create(user=account, department=department)
                if created:
                    record(actor=actor, action=f'demo.department.{department}', target=account.pk)
        contacts = {}
        for item in fixture['contacts']:
            contact = services.create_contact(actor=actor, operation_key=key('contact', item['code']), data={
                'kind': item['kind'], 'name': item['name'], 'email': '', 'phone': '',
                'channel_absence_reason': 'Dado sintético local. Nenhum canal real de contato.',
            })
            contacts[item['code']] = contact
        added = 0
        for item in fixture['demands']:
            operation_key = key('demand', item['code'])
            existing = Demand.objects.filter(creation_key=operation_key).first()
            if existing:
                # Preserve interactive edits and decisions on a replay.
                continue
            contact = contacts[item['contact']]
            owner = reception if item['state'] == 'pending' else actor
            if owner == reception:
                ContactGrant.objects.get_or_create(user=reception, contact=contact, action='view')
            demand = services.create_demand(actor=owner, operation_key=operation_key, data={
                'contact': contact, 'title': '[FICTÍCIO] ' + item['title'],
                'need': f"Cenário sintético {item['code']}. Exercitar atendimento e permissões; não representa cliente ou serviço real.",
                'origin': 'Demonstração local v1', 'area': item['area'],
                'next_step': 'Revisar cenário fictício com a equipe de testes', 'next_step_on': date.fromisoformat(item['on']),
            })
            for action in ['view', 'edit_intake', 'manage_opportunity', 'send_handoff', 'receive_handoff', 'view_history']:
                DemandGrant.objects.get_or_create(user=actor, demand=demand, action=action)
            record(actor=actor, action='demo.record_access', target=demand.pk)
            if item['state'] != 'triage':
                handoff = workflow.send_to_commercial(actor=owner, demand_id=demand.pk, target_id=actor.pk, expected_version=demand.version, operation_key=key('send', item['code']))
                demand.refresh_from_db()
                if item['state'] != 'pending':
                    workflow.accept_handoff(actor=actor, handoff_id=handoff.pk, expected_version=demand.version, operation_key=key('accept', item['code']))
                    demand.refresh_from_db()
                    workflow.update_demand(actor=actor, demand_id=demand.pk, expected_version=demand.version, operation_key=key('edit', item['code']), data={
                        'solution': 'Solução fictícia para revisão de escopo, sem execução ou orientação jurídica real.',
                        'proposal': 'Resumo fictício de escopo. Sem contrato, valor, cobrança ou liberação financeira.',
                    })
                    demand.refresh_from_db()
                    stages = {'diagnosis': [], 'proposal': ['proposal'], 'formalization': ['proposal', 'formalization'], 'lost': ['lost'], 'cancelled': ['cancelled']}[item['state']]
                    for stage in stages:
                        workflow.move_commercial_stage(actor=actor, demand_id=demand.pk, stage=stage, reason='Encerramento fictício para teste.' if stage in {'lost', 'cancelled'} else '', expected_version=demand.version, operation_key=key(f'move-{stage}', item['code']))
                        demand.refresh_from_db()
            added += 1
        for item in fixture['cases']:
            case, created = Case.objects.get_or_create(pk=key('case', item['code']), defaults={'title': '[FICTÍCIO] ' + item['title'], 'responsible': actor})
            for action in ['view', 'export']:
                CaseGrant.objects.get_or_create(user=actor, case=case, action=action)
            if created:
                record(actor=actor, action='demo.case.create', target=case.pk)
        self.stdout.write(self.style.SUCCESS(f'{VERSION}: 6 contatos, 8 demandas e 3 casos demonstrativos. {added} demandas novas; reexecução preserva alterações. Sem autoridade, senha, integração ou envio externo criado.'))
