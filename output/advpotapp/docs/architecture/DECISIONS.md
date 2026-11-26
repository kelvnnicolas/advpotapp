# Decisões de arquitetura recomendadas

24/11/2026. Atualização: monólito Django/HTML/HTMX/PostgreSQL autorizado pelo usuário para a fundação M1. As regras dos módulos seguintes continuam propostas; estas decisões não descrevem a arquitetura da ADVBOX. O registro ADR-008 delimita a execução.

## ADR-001 — aplicação modular de implantação única

Escolha recomendada: monólito modular. Módulos de identidade, contatos, atendimento, casos, trabalho, passagens, documentos, financeiro, integrações e auditoria compartilham transações, mantendo fronteiras de responsabilidade.

Motivo: uma equipe pequena, uma cliente e uma VPS não justificam a operação de vários serviços independentes. Trade-off: disciplina de módulos e testes será necessária para evitar dependência circular e regras espalhadas.

Alternativas: SPA React + API, útil se houver equipe independente ou múltiplos clientes de API; microsserviços, sem necessidade demonstrada. Reavaliar se a arquitetura impedir requisito comprovado, não por antecipação de crescimento.

## ADR-002 — Django, HTML/HTMX e PostgreSQL

Escolha recomendada: Django no servidor, templates HTML com HTMX para interações parciais e PostgreSQL. CSS com tokens e componentes próprios. Usar JavaScript pontual para o quadro, sempre com operação equivalente sem arraste.

O [Django documenta autenticação, grupos e permissões](https://docs.djangoproject.com/en/5.2/topics/auth/). Isso reduz a necessidade de construir mecanismos básicos do zero, mas autorização por registro/caso exige implementação própria e testes. A referência 5.2 foi consultada para arquitetura; não fixa a versão da futura aplicação.

Selecionar versões mantidas e compatíveis no início do lote de fundação, registrar dependências e travá-las. Não instalar automaticamente “latest” sem verificar suporte e compatibilidade. Django Admin será ferramenta administrativa restrita, não interface final de operação.

## ADR-003 — sessões e acesso interno

Escolha proposta: login interno sem cadastro público; sessão em cookie seguro, proteção CSRF, limitação de tentativas e revogação de sessões no desligamento. MFA para contas privilegiadas antes de produção, com mecanismo mantido selecionado na fundação. SSO Google pode ser adicionado após validar domínio e escopo; conectar Calendar não significa autenticar o usuário da aplicação.

Recuperação de acesso por procedimento administrativo auditado no piloto; envio de e-mail somente após configurar remetente e fluxo real autorizado. Sem senha compartilhada ou usuário administrador de demonstração em produção.

## ADR-004 — dinheiro, datas e concorrência

Moeda explícita e Decimal no banco/domínio; nunca float para cálculos financeiros. Datas civis de entrega e prazo usam tipo date. Compromissos/eventos e auditoria usam timestamps inequívocos, com apresentação em fuso acordado.

Comandos de aceitar passagem, liberar operação e registrar recebimento devem ser transacionais. Identificador de operação e controle de versão evitam efeitos repetidos e sobrescrita concorrente. Exclusões de entidades relacionadas exigem política explícita; não usar cascade para apagar histórico financeiro/jurídico por conveniência.

## ADR-005 — integrações assíncronas

Outbox no PostgreSQL e worker do mesmo projeto, como processo separado da aplicação web. Não introduzir broker externo no começo sem necessidade medida. A reivindicação de jobs precisa ser atômica; prever expiração, tentativas, backoff, falha final e repetição manual autorizada.

Adaptadores Drive/Calendar substituídos por simuladores locais nos testes. Idempotência depende de cada operação e da API, não somente de uma flag local. Testar a janela em que o provedor conclui a ação, mas a resposta é perdida.

Referências oficiais consultadas: [criação de eventos Calendar](https://developers.google.com/calendar/api/guides/create-events) e [drives compartilhados](https://developers.google.com/drive/api/guides/about-shareddrives). Confirmar escopos, plano, permissões, notificações e limites na implementação; não presumir integração já validada.

## ADR-006 — infraestrutura e documentos

VPS Linux com contêineres para proxy, aplicação, banco e worker. Não depende de Vercel, Supabase ou serviço de IA. A compra/provisão de recursos não faz parte desta estruturação.

Arquivos do cliente permanecem no Drive quando essa modalidade for aprovada. O Advpot armazena referências e controle operacional. Antes da integração, usar referências manuais institucionais sem alegar verificação automática de acesso ou cópia de conteúdo. Caso seja necessário upload próprio, projetar armazenamento privado, limites, inspeção e recuperação antes de habilitar.

## ADR-007 — implantação exclusiva, sem SaaS presumido

Primeira instalação exclusiva da Delfino, conforme confirmação do usuário. Configuração institucional separada do código. Não introduzir seleção de tenant, assinatura comercial ou isolamento multiempresa fictício. Uma futura expansão terá revisão própria de dados, identidade, autorização e operação; a modularidade não torna a aplicação automaticamente multiempresa.

## ADR-008 — execução autorizada da fundação M1

Nota de evolução em 26/11/2026: a restrição de ADR-007 descreve a primeira implementação, não o limite comercial definitivo. O usuário confirmou produto para outros profissionais/escritórios por instalação licenciada ou SaaS. Identidade Google, isolamento e operação exigem novo plano; alternativas em [Workspace e distribuição](../product/WORKSPACE_AND_DISTRIBUTION.md). Direção aprovada, mecanismo técnico e implementação multiempresa ainda não escolhidos/autorizados por esta nota.

Data: 24/11/2026. Responsável pela autorização: usuário do projeto, pelo pedido de iniciar após a recomendação explícita de M1. Implementação no workspace atual, preservando documentos e ativos anteriores; nenhum destino Desktop foi criado.

Decisão: executar somente identidade, auditoria, envelope mínimo de caso e interface reutilizável. Alternativas consideradas no desenho: frontend/API separados e SaaS multiempresa; monólito escolhido pela operação interna e menor número de componentes. Python 3.13.18, Django 5.2.19 LTS, psycopg 3.3.9, HTMX 2.0.8 local; dependências transitivas em requirements.txt. Compatibilidade Python 3.13 verificada na [documentação oficial Django 5.2](https://docs.djangoproject.com/en/5.2/faq/install/). PostgreSQL local verificado como 17.12. O Python 3.15 global foi preservado.

Perfis técnicos M1: profissional sem privilégios implícitos; administrador de acessos pode gerir contas, sem leitura de casos; auditor pode consultar eventos sem conteúdo jurídico. Por caso, view e export são concessões separadas, cumulativas para exportação. Ser responsável ou superusuário Django não concede leitura automaticamente. Esses perfis não aprovam a matriz por setor do M2.

Sessões Django com versão por conta; desativação, mudança de perfil e revogação invalidam sessões anteriores na requisição seguinte. Bootstrap interativo sem senha padrão, serializado no banco e auditado. Limitação por identificador e IP usa contadores persistidos e normalização coerente. Não confiar em cabeçalhos de proxy até definir a topologia. Proteção CSRF para mutações; logout e exportação por POST. Histórico HTMX privado desabilitado; sessão expirada em fragmento provoca navegação integral ao login.

Não foram necessários broker, microsserviços, APIs externas, provedor de autenticação, upload documental ou recursos pagos. Custo recorrente novo contratado: nenhum. Não há preço ou cronograma comercial aprovado por esta implementação. Impactos: dependências Python/PostgreSQL exigem manutenção e atualização; conta do banco local tem capacidade de criar o banco temporário de testes e não deve ser reutilizada em produção.

Limites: MFA mantido, recuperação auditada de conta, política completa de casos, exportação integral, TLS/proxy, backup externo/restauração e infraestrutura ficam pendentes antes do uso real. Auditoria não é um armazenamento imutável contra acesso administrativo direto ao banco. Não há aplicação publicada em produção. Revisar esta decisão quando mudar stack, modelo de identidade, escopo, custo ou responsabilidade de operação.
