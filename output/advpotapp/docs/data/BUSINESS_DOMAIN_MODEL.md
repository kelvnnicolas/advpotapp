# Business — contrato de apresentação e proposta de domínio

26/11/2026. Checkpoint frontend autorizado; proposta para backend/banco posterior. Não há novos modelos ou migrações neste lote. Stack existente mantida; nenhuma escolha de provedor, preço, vagas ou intervalo de cobrança por inferência.

## Contrato consumido pelo frontend

`advpot.business.frontend.v1`: is_preview=true; business (id opaco demonstrativo, nome, slug de exibição, fuso); membership (role/status); plan (code, amount_minor, currency, interval, seats_included nulos enquanto não decididos); subscription (access_state, paid_through demonstrativo); members fictícios; flow com seis etapas fixas; workspace.status=disconnected. Objetos retornados por get_preview(scenario) independentes para evitar estado global mutável.

Exibir campos comerciais nulos como “A definir”, sem zero monetário, periodicidade ou vagas inventados. Estados active/pending/expired/cancelled são cenários visuais. Nenhum campo deste contrato é prova de pagamento ou de participação real; dados do navegador nunca autorizam o backend futuro.

## Rotas e comandos

| Rota frontend GET/HEAD | Conteúdo | Futuro comando, ainda ausente |
| --- | --- | --- |
| /business/ | Resumo e próximos passos | Seleção de contexto Business validada por Membership |
| /business/equipe/ | Lista, busca, preparação de convite, suspensão visual | Convite/alteração de membro, versão, cota e autoria |
| /business/fluxos/ | Etapas obrigatórias e configuração de nome/responsável | Salvar FlowVersion e aplicar explicitamente a novas demandas |
| /business/assinatura/ | Estado e política de acesso | Regularizar/gerir assinatura pelo responsável autorizado |
| /business/integracoes/ | Estado desconectado e escopos propostos | OAuth e conexão vinculada ao escritório/usuário |
| /business/configuracoes/ | Nome/fuso/canal institucional demonstrativos | Atualizar Business por owner/admin com versão e histórico |
| /contratar/ | Plano sem valores e resumo de contratação | Criar CheckoutAttempt a partir de preço definido no servidor |
| /contratar/retorno/ | Aguardando confirmação, sem ativação | Consultar estado vinculado ao contexto autenticado; webhook confirma |

No futuro, contexto de escritório deve vir de participação autenticada e validada pelo servidor, via seleção/contexto ou identificador explícito; parâmetro de URL ou slug não é autorização. O formato final de rotas com identificador e o mecanismo de isolamento serão decididos no checkpoint de backend. Os POST da prévia retornam 405.

## Entidades propostas para backend

| Entidade | Relações/invariantes propostas | Índices e unicidade candidatos |
| --- | --- | --- |
| Business | UUID, nome, estado, fuso, versão; fronteira de escritório | PK UUID; slug não autentica nem identifica participação |
| Membership | Business + User + papel/status; pelo menos um owner ativo | unique(business,user); índice (business,status,role); mudança de owner serializada |
| PlanVersion | Código/versão, vagas, moeda, valor em unidade mínima, intervalo | unique(code,version); valores imutáveis por versão; preço privado do servidor |
| Subscription | Business, PlanVersion, provedor/conta externa, validade confirmada, estado/versão | unique(provider,provider_account,subscription_id); índice (business,access_state,paid_through) |
| CheckoutAttempt | Business, responsável, plano, chave de operação, referência externa/estado | chave idempotente por Business/ação; sessão externa única por provedor/conta |
| BillingEvent | Provedor/conta, id externo, ambiente, instante/estado de processamento | unique(provider,provider_account,event_id,livemode); índice (processing_state,next_attempt_at) |
| FlowDefinition / FlowVersion | Business, código, versão, etapas e responsáveis; demandas preservam versão aplicada | unique(business,code,version); referências a membros do mesmo Business |
| WorkspaceConnection | Business, identidade Google, escopos, estado, referência de segredo protegido | índice (business,user,provider,status); tokens fora de logs/contrato de frontend |

Não duplicar User por escritório: identidade pode participar de mais de um Business quando essa capacidade for aprovada. Papéis operacionais/comerciais devem estar na Membership/concessão daquele escritório; User.role técnico global atual não vira administração de todos os Business. BusinessAuthority e RecoveryQueue atuais precisam perder caráter global ou ser substituídos por estrutura escopada.

Sem escolher shared database, schemas ou banco/instância por escritório neste lote. Alternativas: isolamento físico aumenta operação por cliente; compartilhado exige filtro/constraints e revisão integral de todos os acessos. Ambas precisam proteger jobs, auditoria, busca, contagem, exportação e integrações. Constraints de relação entre tabelas não se resolvem com CHECK que consulta outra tabela: definir chaves/serviços e mecanismos suportados no desenho físico.

## Migração e otimização a validar

Vincular explicitamente os registros existentes ao primeiro Business, com plano de retorno e sem converter fixture em dado real. Contatos, demandas, casos, grants e eventos precisam de fronteira coerente, impedindo referência cruzada entre escritórios. A migração exige revisão e testes em cópia de homologação antes de dados reais.

Projetar índices pelas consultas reais de lista e entitlement, paginação limitada e dados mínimos por tela; confirmar planos de execução antes de otimizar por hipótese. Separar dados de cartão do domínio Advpot e não guardar PAN/CVV. Valores futuros inteiros em unidade mínima/Decimal com moeda explícita; timestamps de validade em UTC e exibição no fuso do escritório. Backfill, índices, constraints e alterações obrigatórias entram em migrações incrementais, nunca em carga silenciosa ao iniciar o servidor.

## Aceites posteriores indispensáveis

Dois Business sintéticos sem acesso cruzado por ID, lista, grants, worker ou exportação; alteração simultânea de owner/cota; evento financeiro repetido/fora de ordem; expiração com sessão aberta; checkout sem retorno; acesso do suporte sem privilégio jurídico implícito; falha/revogação Google. Entitlement é validado em cada ação com estado confiável do servidor, nunca pelo cenário desta prévia.
