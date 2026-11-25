# Contrato conceitual dos dados

Contrato conceitual do Advpot, não contrato de importação da ADVBOX. Atualização M1: existem modelos e migrações para User, LoginBucket, IdentitySetupLock, AuditEvent e envelope Case/CaseGrant em src/advpot. As demais entidades abaixo permanecem propostas. Não há fixtures Aurora carregadas nem importador definitivo.

## Entidades propostas

| Entidade | Campos/conceitos centrais | Relações e restrições |
| --- | --- | --- |
| OfficeSettings | Nome institucional, fuso e parâmetros | Uma instalação; não é tenant SaaS |
| User / AccessGrant | Identidade, ativo, papéis e concessões por caso | Desativação revoga sessão e impede nova atribuição |
| Contact | Pessoa/organização, nome, canais, origem e identificação opcional | Documento preenchido validado; duplicidade exige revisão |
| Intake / Opportunity | Contato, área, responsável, etapa e próximo passo | Comercial, sem recebimento implícito |
| Engagement | Condições, referência documental e situação da contratação | Liga oportunidade a caso; não pressupõe assinatura digital |
| Case / CaseParty | Área, natureza, estado, responsável; partes por papel | Processo judicial não obrigatório; múltiplas partes possíveis |
| JudicialProcess | Número, órgão e referência, quando aplicáveis | Vinculado a caso; identificadores fictícios não passam como reais |
| Task | Título, responsável, estado, delivery_date, contexto e prioridade | Pode ser interna, de atendimento ou de caso |
| LegalDeadline | Data, origem, confirmação, responsável e estado | Separado de delivery_date; nunca inferido da fixture |
| Appointment | Início/fim com fuso e contexto | Publicação externa opt-in e sem convidados no primeiro marco |
| Handoff | Demanda, trilha, origem/destino, fila/responsável, checklist, estado e versão | Uma passagem ativa por demanda/trilha, conforme proposta a validar; histórico preservado |
| OperationalRelease | Contratação/caso, decisão, motivo e autor | Liberação manual autorizada, sem quitação automática |
| ChecklistItem / DocumentReference | Exigência, conferência, referência de arquivo e metadados | Não presume conteúdo local nem permissão Google |
| Installment / Receipt | Vencimento, valor, moeda, recebimentos e correções | Marco financeiro; previsto não é recebido |
| AuditEvent | Autor, instante, ação, referência e alterações relevantes | Acesso restrito; sem credenciais e conteúdo desnecessário |
| ExternalOperation | Provedor, ação, chave, estado, tentativas e erro sanitizado | Outbox gravada junto à mudança de domínio |
| SourceMapping | Fonte, versão, entidade, source_id e target_id | Unicidade por fonte/versão/entidade/id; reexecução sem duplicar |

Todos os comandos de negócio precisam de autoria e invariantes no servidor. Definir tamanho, obrigatoriedade, nulabilidade, índices e constraints na especificação do lote antes de gerar migrations.

## Uso da base sintética

Fonte: pacote original no diretório pai `data/synthetic/advbox-synthetic-test-data`. O perfil existente informa 39 registros, incluindo escritório, e 64 referências válidas. Essas são verificações históricas locais do dossiê, não uma carga desta entrega.

Base representa **Aurora Advocacia Experimental**, seis usuários fictícios, seis contatos, dois leads, quatro processos, seis tarefas, três publicações, cinco transações, quatro metadados de documentos e duas comunicações de rascunho/template. Não reflete volume ou pessoas da Delfino.

Originais permanecem imutáveis. Cinco registros complementares em `data/synthetic/proposals/v1` continuam propostas separadas; avaliação em memória não foi aceite humano nem autorização de carga.

## De/para candidato para o Advpot

| Fonte sintética | Destino/conceito proposto | Cuidado obrigatório |
| --- | --- | --- |
| office | Ambiente demonstrativo separado | Não substituir pelos dados reais da Delfino |
| users.role / active | Papel descritivo / ativo | Papel textual não concede automaticamente permissão |
| customers | Contact | Preservar source_id; não usar CPF/CNPJ inválido em cenário positivo |
| leads.stage | Etapa comercial da Opportunity | Não confundir com fase jurídica do caso |
| lawsuits | Case + JudicialProcess quando válido/aplicável | Natureza consultiva permite caso sem número/tribunal; campos falsos ficam negativos |
| lawsuits.phase | Rótulo legado no staging | Sem tradução automática para fase/etapa oficial ou etapa própria |
| tasks.due_date | Task.delivery_date | U01 já confirmada: entrega/compromisso; jamais LegalDeadline |
| tasks sem lawsuit_id | Atividade interna ou atendimento, após revisar contexto | Não fabricar processo para satisfazer contrato da ADVBOX |
| tasks.status | Estado próprio revisado por tabela explícita | Conservar bloqueio/revisão; não mapear tudo para pendente |
| transactions.amount/status/paid_at | Estágio de estudo financeiro | Unidade/moeda a confirmar; não converter estado em comando de recebimento |
| documents | DocumentReference demonstrativo | Quatro arquivos originais não existem no pacote; não gerar link funcional fictício |
| publications | Futuro aviso demonstrativo, fora do núcleo | Não afirmar origem judicial nem gerar prazo oficial |
| communications | Templates/rascunhos isolados, fora do envio | Nenhum destinatário externo ou disparo |

Os contratos ADVBOX pendentes continuam pendentes para aquele destino. O modelo próprio não precisa inventar IDs de catálogo ADVBOX nem cumprir suas rotas para funcionar. Em contrapartida, um novo contrato do Advpot também precisa de revisão e testes antes da carga.

## Processo futuro de preparação

1. Aprovar o contrato do lote e o recorte de cenários.
2. Criar cópia derivada versionada, com manifesto de transformações e vínculo para cada fonte.
3. Separar casos positivos sem documento opcional de casos negativos com documento deliberadamente inválido. Não afrouxar validações globais.
4. Fixar data de referência 24/11/2026 nos testes históricos; novos testes usam relógio controlado.
5. Fazer dry-run com rejeições explícitas; não descartar campo sem rastreio nem concatenar tudo em observações.
6. Obter revisão prevista pelo pacote antes da primeira inserção em ambiente de teste.
7. Só então carregar lote autorizado, comparar contagens, relações e resultados; registrar versão e evidência.

Não gerar importador ou payload final nesta etapa. Importação real da cliente possui outro inventário, autorização e reconciliação. Metadados de documentos não bastam para migrar arquivos.

## Controles a conservar

Na data congelada, base original tem zero tarefas pendentes vencidas, uma pendente no dia e quatro futuras. A tarefa concluída com entrega anterior não comprova conclusão atrasada porque não há completed_at.

Totais financeiros nominais do relatório: recebíveis 7900.00, pagáveis 480.00, recebíveis sem pagamento 3700.00. Não são saldo bancário, economia ou indicadores reais. Se houver fixture financeira futura, declarar moeda/unidade e preservar esses controles na camada de origem antes de qualquer transformação.
