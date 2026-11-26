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
- [ ] Testes RED de login, produção, métodos, cenário inválido, contrato sem preço fictício e ausência de efeitos em modelos reais.
- [ ] Registrar proposta de domínio/alternativas/índices e implementar entrega local de HTML sem modelos.
- [ ] Testes pertinentes GREEN e commit do checkpoint.

## Task 2 — CP2: interface/interações

Arquivos: templates/business/*; static/business.{css,js}; templates/base.html e identity/login.html; tests/test_business_browser.py.
Interfaces: páginas por rota, formulário data-preview-form com prevenção de submissão; aviso aria-live; atributos/IDs estáveis para testes. Componentes visuais consistentes com .stitch/DESIGN.md.
- [ ] Testes RED de jornada Chrome e responsividade, convite duplicado, suspensão, fluxo, resumo da contratação e ausência de chamadas/escritas.
- [ ] Implementar telas e estados/interações locais com DOM seguro, labels, foco e estados vazios.
- [ ] Chrome desktop/celular, regressões M1/M2 e commit.

## Task 3 — CP3: validação e entrega

Arquivos: docs/testing/BUSINESS_FRONTEND_VERIFICATION.md, README, PROJECT_STATUS e escopo comercial.
- [ ] Suíte PostgreSQL com navegador, check e migrations --check.
- [ ] Revisão independente do conjunto, uma passagem de correções relevantes com RED→GREEN.
- [ ] Servidor local atualizado, inspeção das telas e capturas fictícias; docs de limites/resultado e commit.

## Ledger

- BASE: fbab150. Novo branch codex/business-frontend, árvore limpa antes do início.
- Ruling: manter o checkout existente e isolar em branch, sem worktree adicional — preserva o servidor/venv e URL usados pelo usuário — custo: não permite dois desenvolvimentos simultâneos no mesmo diretório.
- Ruling: primeiro lote é frontend de prévia local e contrato de domínio; backend/banco seguem checkpoint posterior — respeita ordem explícita e decisões comerciais pendentes — custo: nenhuma ação Business é persistida ou cobrada nesta entrega.
