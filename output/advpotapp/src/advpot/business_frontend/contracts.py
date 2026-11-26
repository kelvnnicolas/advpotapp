"""Presentation fixtures only. Never use these values to authorize access."""
from copy import deepcopy

SCENARIOS = {
    'active': {'label': 'Ativa', 'description': 'Exemplo de período confirmado e vigente.', 'paid_through': '26/12/2026', 'tone': 'positive'},
    'pending': {'label': 'Aguardando pagamento', 'description': 'O escritório aguarda a confirmação do provedor.', 'paid_through': None, 'tone': 'warning'},
    'expired': {'label': 'Período encerrado', 'description': 'A validade terminou. O responsável deverá regularizar a assinatura.', 'paid_through': '25/11/2026', 'tone': 'warning'},
    'cancelled': {'label': 'Cancelada', 'description': 'Exemplo de assinatura encerrada, sem direito de uso vigente.', 'paid_through': None, 'tone': 'neutral'},
}

FIXTURE = {
    'schema_version': 'advpot.business.frontend.v1', 'is_preview': True,
    'business': {'id': 'demo-horizonte', 'name': 'Horizonte Advocacia', 'slug': 'horizonte-demo', 'timezone': 'America/Sao_Paulo'},
    'membership': {'role': 'owner', 'status': 'active'},
    'plan': {'code': 'business', 'name': 'Business', 'amount_minor': None, 'currency': None, 'interval': None, 'seats_included': None},
    'workspace': {'status': 'disconnected'},
    'members': [
        {'id': 'demo-owner', 'name': 'Ana Horizonte', 'email': 'ana@horizonte.invalid', 'role': 'Responsável Business', 'status': 'Ativo', 'owner': True},
        {'id': 'demo-member-1', 'name': 'Bruno Horizonte', 'email': 'bruno@horizonte.invalid', 'role': 'Profissional', 'status': 'Ativo', 'owner': False},
        {'id': 'demo-member-2', 'name': 'Carla Horizonte', 'email': 'carla@horizonte.invalid', 'role': 'Apoio', 'status': 'Ativo', 'owner': False},
    ],
    'flow': {'name': 'Atendimento do escritório', 'version': 1, 'owner': 'Ana Horizonte', 'stages': [
        ('01', 'Recepção', 'Secretaria', 'Identificar a necessidade e organizar a entrada.'),
        ('02', 'Atendimento comercial', 'Comercial', 'Entender a demanda e preparar a contratação.'),
        ('03', 'Conferência inicial', 'Financeiro', 'Conferir condições e registrar a decisão de liberação.'),
        ('04', 'Organização e distribuição', 'Secretaria', 'Conferir documentos e indicar responsável jurídico.'),
        ('05', 'Execução do serviço', 'Operacional', 'Conduzir o trabalho e registrar pendências.'),
        ('06', 'Acompanhamento final', 'Financeiro', 'Conferir pendências e apoiar o fechamento.'),
    ]},
}


def get_preview(scenario='active'):
    if scenario not in SCENARIOS:
        raise ValueError('Cenário de prévia inválido.')
    data = deepcopy(FIXTURE)
    data['subscription'] = {**SCENARIOS[scenario], 'access_state': scenario}
    return data
