# Business Frontend Implementation Plan

> **For agentic workers:** usar superpowers:executing-plans para execução nativa, task-by-task, com uma revisão independente final. O pedido já autoriza iniciar; não repetir confirmação de implementação do mesmo lote.

**Goal:** primeiro checkpoint Business navegável, responsivo e testado, preparando rotas/contratos antes de backend/banco.

**Architecture:** módulo business_frontend com views GET locais sem modelos; dados de prévia fixos, templates e JS local sem persistência. Separar apresentação de proposta de domínio e serviços futuros.

**Tech Stack:** Django 5.2/HTML/HTMX existente, CSS/JS locais; nenhuma dependência nova.

**Spec:** docs/superpowers/specs/2026-11-26-business-frontend.md; docs/product/BUSINESS_SAAS_EVALUATION.md.

## Global Constraints

- Frontend primeiro; não criar tabelas, cobrar, enviar convites ou conectar Workspace neste lote.
- Produção 404; área Business autenticada; todos os dados fictícios e banner de prévia.
- Sem preço, quantidade de vagas, frequência ou provedor definidos por inferência.
- Interações sem gravação e sem armazenar dados de formulários no navegador.
- Preservar M1, M2-A e a base fictícia local existentes.

## Review Focus

1. Usuário pode interpretar assinatura/Google como real ou interface como administração de dados existentes.
2. JS desativado/erro pode enviar formulário, expor conteúdo na URL ou persistir dados.
3. Entrada HTML, nomes/emails repetidos e papéis adulterados podem gerar XSS ou estado inválido.
4. Cenário desconhecido, acesso anônimo e DEBUG=False podem expor rotas fora do recorte.
5. CSS/navegação novos podem quebrar operação M1/M2 ou celular; links devem conservar contexto permitido.

## Task 1 — CP1: contrato e rotas

Arquivos: docs/data/BUSINESS_DOMAIN_MODEL.md; src/advpot/business_frontend/{__init__,contracts,views,urls,context_processors}.py; config/{settings,urls}.py; tests/test_business_frontend.py.
Interfaces: get_preview(scenario) com schema_version e campos fixos sem preço/vagas; rotas business:index/team/flows/subscription/integrations/settings e business:contract/return, GET/HEAD.
- [x] Testes RED de login, produção, métodos, cenário inválido, contrato sem preço fictício e ausência de efeitos em modelos reais.
- [x] Registrar proposta de domínio/alternativas/índices e implementar entrega local de HTML sem modelos.
- [x] Testes pertinentes GREEN e commit do checkpoint.

## Task 2 — CP2: interface/interações

Arquivos: templates/business/*; static/business.{css,js}; templates/base.html e identity/login.html; tests/test_business_browser.py.
Interfaces: páginas por rota, formulário data-preview-form com prevenção de submissão; aviso aria-live; atributos/IDs estáveis para testes. Componentes visuais consistentes com .stitch/DESIGN.md.
- [x] Testes RED de jornada Chrome e responsividade, convite duplicado, suspensão, fluxo, resumo da contratação e ausência de chamadas/escritas.
- [x] Implementar telas e estados/interações locais com DOM seguro, labels, foco e estados vazios.
- [x] Chrome desktop/celular, regressões M1/M2 e commit.

## Task 3 — CP3: validação e entrega

Arquivos: docs/testing/BUSINESS_FRONTEND_VERIFICATION.md, README, PROJECT_STATUS e escopo comercial.
- [x] Suíte PostgreSQL com navegador, check e migrations --check.
- [x] Revisão independente do conjunto, uma passagem de correções relevantes com RED→GREEN.
- [x] Servidor local atualizado, inspeção das telas e capturas fictícias; docs de limites/resultado e commit.

## Ledger

- BASE: fbab150. Novo branch codex/business-frontend, árvore limpa antes do início.
- Ruling: manter o checkout existente e isolar em branch, sem worktree adicional — preserva o servidor/venv e URL usados pelo usuário — custo: não permite dois desenvolvimentos simultâneos no mesmo diretório.
- Ruling: primeiro lote é frontend de prévia local e contrato de domínio; backend/banco seguem checkpoint posterior — respeita ordem explícita e decisões comerciais pendentes — custo: nenhuma ação Business é persistida ou cobrada nesta entrega.


- CP1: testes RED observados sem rotas/módulo; 7 testes GREEN após implementação. Contrato e modelagem candidatos registrados. Commit 8a6773e.
- CP2: jornada Chrome RED com campos sem interações; JS/CSS implementados, desktop/celular e caminho sem JavaScript verificados. Ajustados seletores de noscript/fieldset e expectativa de sessionStorage para metadado HTMX não conter dados de formulário. Commit d75236c; suíte 73/73 antes da revisão.
- CP3: revisão independente /root/review_business_frontend, somente leitura, pacote git diff -U10 fbab150..d75236c. Retorno de contratação corrigido; suíte final 74/74 PostgreSQL com seis testes de navegador e check/migrations --check aprovados; sem modelos ou migrações novos.
- Final: fixed contexto do retorno da contratação — test_checkout_return_links_preserve_the_origin_scenario RED→GREEN, jornada de ida/volta expired em Chrome e suíte 74/74. Asserção focal adicional inspeciona somente o painel de retorno, evitando correspondência com navegação lateral.
- Final: minor (deferred): sem JavaScript a busca e os botões de suspensão visual não funcionam mas ainda aparecem habilitados. Formulários de edição permanecem desabilitados; nenhuma gravação ou envio ocorre. Refinamento da experiência sem JS permanece pendente.
- Final: Ruling: aceite visual do ambiente pelo usuário não foi emitido pelo revisor — executor inspecionou desktop/celular e páginas locais, mas mantém estado de revisão — custo: homologação do usuário ainda é necessária antes de declarar disponibilidade operacional.
- Final: Ruling: revisor não executou PostgreSQL — evidência de 74 testes e check/migrations vem da execução real deste agente — custo: a revisão é estática e não oferece uma segunda execução independente da suíte.
- Operação local: servidor atualizado e /contratar/ HTTP 200. Nenhum dado Business persistido, provedor escolhido, cobrança ou conexão Google.
