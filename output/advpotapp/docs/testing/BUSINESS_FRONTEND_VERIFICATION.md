# Business — checkpoints de frontend

26/11/2026. Autorizado pelo usuário: iniciar estrutura/implementação por checkpoints, frontend primeiro e backend/banco posteriormente. Escopo deste lote: apresentação e interações demonstrativas locais, com contrato/modelagem propostos. Sem SaaS operacional ou aceite de produção.

## CP1 — contrato e rotas

Modelo de apresentação advpot.business.frontend.v1 e oito rotas nomeadas: /business/, /business/equipe/, /business/fluxos/, /business/assinatura/, /business/integracoes/, /business/configuracoes/, /contratar/ e /contratar/retorno/. Área Business exige sessão; contratação demonstrativa é pública apenas no desenvolvimento local. DEBUG=False retorna 404; POST/PUT/DELETE autenticados retornam 405. Cenários permitidos: active, pending, expired, cancelled; desconhecidos não viram assinatura ativa por fallback.

Sete testes de rotas/contrato observaram RED antes da implementação e passaram após. Proposta de domínio com entidades, vínculos, índices candidatos, alternativas de isolamento e migração em [BUSINESS_DOMAIN_MODEL.md](../data/BUSINESS_DOMAIN_MODEL.md). Nenhuma tabela/modelo Business criada; os singletons atuais não são apresentados como solução multiempresa.

## CP2 — interface e interações

Navegação Business própria, escritório Horizonte explicitamente fictício e retorno à operação local. Equipe pesquisável, preparação/duplicidade de convite, papel validado e suspensão visual; configuração de nome/responsável do fluxo sem alterar as seis etapas; configurações institucionais na tela; cenários de assinatura; integrações Google sempre desconectadas; resumo de contratação e retorno aguardando confirmação. Sem preço, vagas, frequência ou provedor inventados.

JavaScript local sem fetch/XHR, persistência, SDK ou serviço externo. Entrada de usuário renderizada como texto; payload HTML não cria elementos/eventos. Formulários não possuem botões submit e permanecem desabilitados sem JavaScript; o aviso noscript informa a limitação. Com JavaScript, handlers de bloqueio de submissão são registrados antes da habilitação dos campos. Interações são perdidas ao navegar/recarregar.

Jornada real Chrome passou após observar RED dos campos inicialmente sem interações. Verificados desktop 1440 px e celular 390 px; todas as oito rotas sem rolagem horizontal da página, tabela com rolagem própria, teclado e feedback aria-live. Sem JavaScript, controles continuam desabilitados e links funcionam. Capturas fictícias: [resumo](../../.stitch/previews/business-overview.png), [equipe](../../.stitch/previews/business-team.png), [celular](../../.stitch/previews/business-mobile.png), [contratação com payload de teste exibido como texto](../../.stitch/previews/business-contract.png).

## CP3 — verificação do conjunto

`ADVPOT_BROWSER_TESTS=1`, `manage.py test tests --settings=config.test_postgres --verbosity 1 --noinput`: **74 testes aprovados, zero ignorados**, incluindo seis testes de navegador, concorrência PostgreSQL e regressões M1/M2-A. `makemigrations --check --dry-run`: nenhuma mudança. Django check: sem problemas identificados.

Nos testes de navegação/interação Business, contagens de User, Contact, Demand, Case, AuditEvent, BusinessAuthority, DemandGrant e BusinessAssignment permaneceram iguais após o login. Nenhuma requisição de escrita ou externa durante as ações demonstrativas. Nenhum dado de formulário em localStorage/sessionStorage; HTMX conserva apenas sua referência de caminho de navegação, sem conteúdo dos campos. Não há sessão própria de contratação ou cookie de pagamento.

Revisão independente estática sobre fbab150..d75236c concluída. Achado relevante: retorno da contratação perdia cenário de origem. Reproduzido com teste RED e corrigido nos links; teste de regressão e jornada Chrome preservam expired no caminho de ida/volta. Suíte final 74/74; assert adicional restrito ao painel de retorno passou em execução focal. Pendência menor adiada: sem JavaScript, busca e botões de suspensão da equipe permanecem visualmente habilitados mas sem interação; os formulários de edição continuam protegidos. O revisor não executou PostgreSQL nem deu aceite visual; esses resultados são verificação técnica do executor, não homologação do usuário. As capturas M1/M2-A regeneradas pela suíte foram restauradas para preservar referências históricas.

## Limites e checkpoint seguinte

Este frontend não autentica via Google, não cria escritório/membro, não envia convite, não grava FlowVersion, não aplica entitlement e não inicia checkout. O cenário de assinatura é apenas apresentação; não deve ser utilizado para autorizar serviços futuros. A operação M1/M2-A e a base fictícia persistente permanecem separadas desta prévia.

Próximo checkpoint proposto: Business/Membership/isolamento e migração do primeiro escritório; serviços e comandos escopados; só depois assinatura/checkout e integração Google com decisões registradas e testes próprios. Preço, vagas, periodicidade, provedor e estratégia física de isolamento continuam pendentes. Nenhuma API pública nova, infraestrutura, custo comercial ou disponibilidade SaaS aprovado por esta entrega.


Servidor local atualizado; /contratar/ respondeu HTTP 200 com banner de prévia e valor a definir. Nenhuma migração ou gravação Business aplicada. Os links da área Business ficam disponíveis após login existente no ambiente local.
