# Fundação M1 — Implementation Plan

> **For agentic workers:** execução nativa nesta sessão com superpowers:executing-plans. A instrução do usuário “inicie e após atualize prototipagem ... no stitch” autoriza a execução e a atualização visual subsequente.

**Goal:** disponibilizar uma fundação executável localmente para revisão, sem declarar produção ou aceite da Delfino.

**Architecture:** monólito modular Django, templates HTML e PostgreSQL. Autorização por ação/registro separada da administração de acessos. Integrações desligadas.

**Tech Stack:** Python 3.13; Django 5.2 LTS; psycopg 3; HTMX local apenas onde houver interação parcial real. Fixar patches após consulta aos metadados oficiais.

**Spec:** docs/specs/ADVPOTAPP_DESIGN.md, recorte M1 do docs/delivery/BUILD_ROADMAP.md.

## Global Constraints

- Aplicação interna exclusiva da Delfino; sem cadastro público.
- Sem dados reais, carga Aurora, migração, envios, Workspace ou provisão de infraestrutura.
- Entrega de tarefa é diferente de prazo fatal; M2 permanece proposto.
- Negar por padrão; administrar usuários não concede leitura de casos.
- Não expor segredos, senhas, tokens ou conteúdo jurídico no histórico.
- Ambiente local no diretório existente output/advpotapp. Destino histórico Desktop não será criado por inferência.

## Review Focus

1. URL de retorno externa não pode redirecionar login para outro domínio.
2. Desativar e reativar um usuário não pode ressuscitar sessão anterior.
3. Busca, paginação e totais não podem revelar registros sem concessão.
4. Mutações sem CSRF e administração sem permissão devem falhar no servidor.
5. Tentativas repetidas de login devem ser limitadas sem enumerar contas.

## Task 1 — ambiente e sessão interna

Arquivos: requirements.txt, src/manage.py, src/config/*, src/advpot/identity/*, tests/test_identity.py, deploy/*.
Interfaces: User com role e session_version; login/logout; comando administrativo auditado para criar conta, alterar perfil e revogar sessões.
- [x] Preparar Python suportado e dependências fixas; PostgreSQL configurado por ambiente.
- [x] Escrever e observar falha dos testes de sessão, CSRF, bloqueio de tentativas e revogação.
- [x] Implementar identidade, limitação persistida, auditoria mínima e administração interna.
- [x] Executar testes da identidade com banco real disponível.

## Task 2 — política por registro e interface

Arquivos: src/advpot/cases/*, src/advpot/audit/*, src/templates/*, src/static/*, tests/test_access.py.
Interfaces: Case mínimo (referência, título e responsável), CaseGrant(user, case, action); consultas autorizadas; nenhum fluxo M2 completo.
- [x] Escrever e observar falha de testes de isolamento, ação específica, lista/busca/total e trilha.
- [x] Implementar envelope mínimo de caso para exercitar a política, leitura/listagem e exportação autorizada, sem criar fluxos jurídicos adicionais.
- [x] Implementar interface portuguesa, estados vazios, filtros, paginação e tratamento de erros.
- [x] Verificar conjunto, migrations e configuração de implantação; registrar limites de MFA/produção.

## Task 3 — verificação e protótipo Stitch

Arquivos: docs/testing/M1_VERIFICATION.md, docs/architecture/DECISIONS.md, PROJECT_STATUS.md, README.md, .stitch/*.
- [x] Verificar login, páginas e acesso negado; revisar código ao final.
- [x] Localizar projeto Stitch existente; preservar telas anteriores e adicionar revisão M1 coerente com o produto.
- [x] Registrar IDs e links, revisão visual e status; protótipo não comprova função entregue.

## Registro de execução

- 24/11/2026: usuário autorizou M1 após recomendação explícita de stack e escopo. M2–M6 não autorizados por inferência.
- Ruling: repositório ainda sem commits, todos os documentos não rastreados; executar em lugar, preservando os arquivos existentes. Não há baseline para worktree; não criar commit de materiais alheios.
- Ruling: execução segue diretamente por autorização atual, sem nova rodada de aprovação do mesmo recorte.
- Ruling: Python 3.15 global não será usado como ambiente suportado. Preparar runtime local 3.13; Docker instalado, mas daemon indisponível no diagnóstico inicial.
- Task 1: complete — sessão, contas, throttle e bootstrap; falhas observadas antes das implementações/correções, suíte PostgreSQL final aprovada.
- Task 2: complete — autorização de lista/detalhe/exportação, interface, histórico e filtros; 28 testes aprovados, nenhum problema no check e nenhuma migração pendente.
- Final review: revisão estática independente executada; achados de cache HTMX, normalização/alocação do throttle e bootstrap concorrente corrigidos com regressões RED→GREEN.
- Final: Ruling: total de filtro, retorno ao login em fragmento, entrada não interativa de senha, colisão de username e logs com busca foram tratados como correções funcionais/confidencialidade do M1, não polimento opcional. Sem achado técnico menor conhecido deixado para trás nesta revisão; requisitos de piloto/produção explicitamente fora da disponibilidade atual.
- Task 3: complete — três telas M1 verificadas e colocadas no canvas Stitch, com HTML e screenshots reais, sem scripts/CSRF, preservando referências anteriores. A geração inicial foi substituída após revisão visual para eliminar garantias e funções não implementadas. Duas jornadas de navegador novamente aprovadas após extração.
- Ruling: não criar commit inicial incluindo documentos alheios nem alterar repositório externo. Todos os arquivos permanecem no workspace para revisão do usuário.
