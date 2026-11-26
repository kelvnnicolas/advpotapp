# Guia de direção para agentes de software

Consolidado em 26/11/2026. Use este arquivo para transformar as decisões de negócio em um recorte implementável. Ele complementa AGENTS.md; não substitui o pedido atual nem autoriza construir o roadmap inteiro.

## Leitura mínima, em ordem

1. [AGENTS.md da aplicação](../../AGENTS.md) e instruções do repositório pai.
2. [Posicionamento do negócio](../business/BUSINESS_POSITIONING.md).
3. [Objetivo do produto](../product/PRODUCT_OBJECTIVE.md).
4. [Status atual](../../PROJECT_STATUS.md) e evidências do lote correspondente.
5. Spec/plano do checkpoint autorizado, [decisões de arquitetura](../architecture/DECISIONS.md), [contrato de dados](../data/DATA_CONTRACT.md) e [questões em aberto](../decisions/OPEN_QUESTIONS.md).

## Decisões estabelecidas que não precisam ser redescobertas

- Delfino é a primeira validação; Advpot deverá poder atender outros advogados/escritórios.
- Prioridade comercial: assinatura por escritório com colaboradores incluídos, sem trial. Não presumir preço, vagas, frequência ou provedor.
- Workspace é colaboração; Advpot é a fonte principal da operação jurídica. Identidade Google, consentimento de API e participação no escritório são controles distintos.
- Demanda atravessa setores com responsabilidade preservada até aceite. Entrega, compromisso e prazo fatal são distintos.
- Implementação existente usa Django/HTML/HTMX/PostgreSQL. Não trocar stack ou criar um segundo frontend por preferência do agente.
- O pedido mais recente de construção priorizou frontend, validado por checkpoints, com backend/banco posteriormente. O frontend Business é prévia, sem domínio persistido.

## Como decidir o que construir

Antes de editar, registrar de forma curta:

| Pergunta | Saída esperada |
| --- | --- |
| Qual usuário e problema? | Persona e dificuldade concreta da operação |
| Em qual fluxo e checkpoint? | Entrada, ação, saída e vínculos com registros existentes |
| Qual autorização existe? | Pedido/decisão do usuário e fronteiras do lote |
| Quais regras e limites? | Permissões, responsabilidade, estados, versão e exceções |
| O que depende de decisão? | Diferenciar bloqueio real de decisão rotineira reversível |
| Como comprovar? | Aceite observável e verificações proporcionais, incluindo negação/falha quando pertinente |

Avançar nas decisões rotineiras dentro do escopo já autorizado e registrar escolhas. Não repetir pedidos de aprovação da mesma entrega. Quando faltar decisão material de provedor, preço, isolamento ou efeito externo, preparar a opção concreta e continuar o trabalho independente que não dependa dela. Ausência de resposta não é aprovação de cobrança, envio, importação ou publicação de dados.

## Regras de implementação

1. Reutilizar módulos, tokens e padrões existentes. Separar apresentação, consultas autorizadas e comandos de negócio; não criar estruturas vazias para fingir módulos concluídos.
2. Para Business, registrar estratégia de isolamento e migração antes de schema. Escopar concessões, consultas, histórico, exportações, credenciais e jobs. Não adaptar somente a tela de login ou adicionar um campo pago como solução de SaaS.
3. Validar identidade/participação/assinatura/permissão no servidor quando essas capacidades forem implementadas. Nunca confiar em cenário de prévia, papel, preço, valor pago ou business_id recebido do navegador como autorização.
4. Preservar transações, idempotência, versão e trilha de mudanças nos comandos pertinentes. Separar cobrança SaaS do financeiro jurídico. Proteger segredos e evitar sua cópia em exemplos, fixtures, commits, capturas ou logs.
5. Integrações externas ficam desligadas em testes locais por padrão; efeitos reais exigem escopo e autorização explícitos. Não usar a conta Google pessoal do operador como conta institucional do cliente.
6. Usar dados fictícios identificados, sem canais reais ou documentos deliberadamente inválidos nos cenários positivos. Não carregar Aurora ou dados reais por semelhança com uma fixture existente.
7. Testar os fluxos alterados e seus limites; não confundir testes locais antigos com verificação do novo código. Em documentação isolada, verificar links, coerência e escopo sem afirmar execução funcional que não ocorreu.

## Critérios para rejeitar um caminho

Rever uma proposta se ela mistura escritórios, esconde falta de responsável, envia cobrança/convite por efeito de demonstração, transforma administrador técnico em leitor universal, duplica a demanda entre setores, converte entrega em prazo fatal ou promete integração/capacidade que só existe visualmente.

Evitar módulos isolados sem vínculo com uma jornada, personalização ilimitada, indicadores sem origem, reescrita de tecnologia sem motivo comprovado e otimização de banco sem consultas/medição correspondentes.

## Como fechar um checkpoint

- Registrar o que foi implementado e o que continua proposta ou prévia.
- Apresentar evidências das verificações executadas e limites restantes, inclusive pendências relevantes.
- Atualizar PROJECT_STATUS.md, plano/spec e documentação de operação; atualizar escopo comercial se mudar capacidade, responsabilidade, custo ou prazo.
- Manter arquivos, links, branch e histórico coerentes. Quando atualizar a cópia no Desktop, preservar dossiê/versões anteriores e verificar hashes; não copiar sessões ou credenciais.
- Não declarar disponível antes de verificação, aceite no ambiente destinado ao uso e publicação acordada. A implementação de um lote não autoriza o próximo automaticamente só por constar no roadmap.

Para retomar hoje, verificar o checkpoint backend/banco Business no [contrato proposto](../data/BUSINESS_DOMAIN_MODEL.md), preservar M1/M2-A e não tratar a [prévia frontend](../testing/BUSINESS_FRONTEND_VERIFICATION.md) como gestão multiempresa real.
