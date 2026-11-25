# Advpotapp — aplicação interna Delfino

**Gestão jurídica conectada. Tecnologia sob medida. Liberdade para evoluir.**

Aplicação interna, atualizada em 24/11/2026. Construção M1 no workspace atual, em `output/advpotapp`. O caminho Desktop citado na estruturação anterior permanece uma referência histórica; não foi criado ou alterado.

**M1 implementado para revisão técnica local:** login interno, limitação persistida de tentativas, administração de contas, revogação de sessões, política por caso/ação, auditoria, interface em português e exportação mínima autorizada. PostgreSQL local criado e migrações aplicadas. Nenhuma carga Aurora ou dado real, integração externa ou implantação em VPS.

Abrir [http://127.0.0.1:8765/entrar/](http://127.0.0.1:8765/entrar/) com o servidor local em execução. Não existe conta/senha padrão; criar o primeiro administrador por terminal conforme [guia local](docs/operations/LOCAL_DEVELOPMENT.md). O guia também contém instalação e testes. [Evidências do M1](docs/testing/M1_VERIFICATION.md).

Protótipos: [Advpotapp — Delfino no Stitch](https://stitch.withgoogle.com/projects/10692539038282260634). São referências visuais para revisão, não comprovam disponibilidade de módulos futuros.

## Decisões e limites

- **Confirmado pelo usuário:** começar por uma aplicação interna exclusiva da Delfino. Atendimento a outros escritórios é evolução posterior.
- **Diretriz de produto:** implantação inicial em VPS, Google Workspace como colaboração e Advpot como fonte dos fluxos jurídicos.
- **Arquitetura autorizada para M1:** monólito modular em Django, páginas HTML com HTMX e PostgreSQL. Dependências fixadas; decisões e limites em docs/architecture/DECISIONS.md. Sem microsserviços ou SaaS multiempresa.
- **Regra do domínio já confirmada:** entrega/compromisso de tarefa é diferente de prazo fatal.
- **Material da empresa:** o fluxo fotografado do escritório orienta as passagens entre setores; o site público orienta áreas e contexto institucional.

## Ordem de leitura

1. [Contexto da cliente e conciliação das fontes](docs/context/CLIENT_DOSSIER.md).
2. [Estratégia do produto](docs/product/PRODUCT_STRATEGY.md).
3. [Desenho da aplicação](docs/specs/ADVPOTAPP_DESIGN.md).
4. [Decisões de arquitetura recomendadas](docs/architecture/DECISIONS.md).
5. [Contrato dos dados e uso das fixtures](docs/data/DATA_CONTRACT.md).
6. [Roteiro de construção](docs/delivery/BUILD_ROADMAP.md).
7. [Critérios de aceite](docs/testing/ACCEPTANCE.md) e [operação em VPS](docs/operations/VPS_RUNBOOK.md).
8. [Questões a validar](docs/decisions/OPEN_QUESTIONS.md).

A [organização prevista do código](docs/architecture/PROJECT_LAYOUT.md) detalha diretórios, responsabilidades e rotas próprias para orientar a execução futura.

Os documentos anteriores de produto, implantação e comercial foram incorporados como referência. Onde detalham sugestões anteriores, prevalece para esta proposta o desenho específico do Advpotapp: em especial a passagem pelo financeiro antes da operação, sem pressupor pagamento integral obrigatório.

## Referências complementares

- [Blueprint anterior](docs/product/PRODUCT_BLUEPRINT.md).
- [Processo de implantação](docs/project/PROJECT_PLAYBOOK.md).
- [Estratégia comercial](docs/commercial/COMMERCIAL_STRATEGY.md).
- [Modelo de proposta](docs/commercial/PROPOSAL_TEMPLATE.md).
- [Escopo comercial da aplicação](docs/commercial/ADVPOTAPP_SCOPE.md).
- [Fontes e rastreabilidade](docs/context/SOURCE_REGISTER.md).
- [Status desta entrega](PROJECT_STATUS.md).

## Sequência após a fundação M1

A fundação M1 foi construída após autorização do usuário. M2 permanece proposto: contato → triagem → proposta/contratação → liberação financeira manual → documentos → distribuição ao jurídico → tarefa → histórico operacional. Validar matriz por setor, transições e exceções antes de implementar esse lote.

Drive/Calendar e financeiro gerencial completo têm marcos próprios. Sua ausência no primeiro lote exige convivência explícita com as ferramentas atuais; esse lote não é uma substituição integral da ADVBOX.
