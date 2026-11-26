# Orientações do Advpotapp

## Escopo e fontes

Antes de propor ou criar software, ler [posicionamento de negócio](docs/business/BUSINESS_POSITIONING.md), [objetivo do produto](docs/product/PRODUCT_OBJECTIVE.md), [guia para agentes](docs/project/AGENT_PRODUCT_BRIEF.md) e PROJECT_STATUS.md. Essas referências consolidam a direção sem autorizar novos lotes por inferência.

Esta pasta reúne o desenho de uma aplicação independente para uso interno da Delfino. Ler README, docs/specs/ADVPOTAPP_DESIGN.md, docs/context/CLIENT_DOSSIER.md, docs/data/DATA_CONTRACT.md e docs/decisions/OPEN_QUESTIONS.md antes de planejar implementações.

M1/M2-A e frontend Business foram implementados após autorizações do usuário; backend/banco Business, isolamento, cobrança e Google seguem pendentes. Não tratar recomendações técnicas ou regras propostas como aprovação automática para construir todos os módulos, provisionar serviços ou migrar dados. A restrição documental do dossiê pai continua valendo para a investigação da ADVBOX. Novas autorizações do usuário definem o escopo das futuras etapas.

## Produto

- Delfino é a primeira validação. Direção comercial confirmada: produto para outros escritórios, priorizando assinatura Business por escritório com colaboradores incluídos, sem trial. Cadastro público, cobrança e isolamento não estão implementados nem autorizados por mera referência nesta instrução.
- Preservar a separação entre atendimento, oportunidade, contratação, caso, processo judicial, tarefa, prazo fatal e compromisso.
- Modelar passagens entre secretaria, comercial, financeiro e operação com responsável, checklist, pendência e histórico.
- Não exigir quitação integral para iniciar todo caso. Liberação financeira é uma decisão manual autorizada na primeira versão.
- Não transformar tasks.due_date das fixtures em prazo fatal ou início de tarefa.
- Não copiar fase/etapa, permissões, fórmulas ou schema da ADVBOX como regra da Delfino.
- Não prometer que o sistema, integrações ou requisitos de segurança estão prontos sem verificação correspondente.

## Implementação futura

Stack existente Django/HTML/HTMX/PostgreSQL autorizada para a fundação e registrada em docs/architecture/DECISIONS.md. Mudança de stack exige atualização da decisão e do roteiro. Trabalhar por lotes e manter produto, aceite e comercial coerentes; não tratar mecanismo de autenticação Google, provedor financeiro ou estratégia de isolamento como escolhidos por esse registro.

Validar permissões no servidor, por ação e registro; controles visuais não bastam. Sessões, CSRF, segredos, auditoria e revogação são requisitos da fundação. Grupos Django não implementam sozinhos autorização por caso.

Integrações externas devem usar adaptadores, outbox e idempotência. Desligadas por padrão em desenvolvimento/teste. Não enviar e-mail, WhatsApp, convite, cobrança, protocolo ou dados reais por efeito de uma fixture.

## Dados

Preservar o pacote sintético e o dossiê no diretório pai. Não adaptar originais silenciosamente. Não carregar as propostas v1, criar importador definitivo ou inserir dados sem a revisão e autorização correspondentes. Preparar novo mapeamento para o contrato próprio do Advpot; pendências de importação ADVBOX não são evidência de impossibilidade de modelar o produto independente.

Usar identificadores externos versionados para rastreabilidade. Dados demonstrativos com documentos inválidos devem ir para fixtures negativas ou casos positivos sem identificador opcional; não desativar a validação de produção para acomodá-los. O escritório fictício Aurora nunca será renomeado para parecer a base real da Delfino.

## Conclusão de cada lote

Registrar mudanças, verificação, limites e estágio em PROJECT_STATUS.md. Testar os comportamentos relevantes, incluindo negação de acesso e falhas de integração quando alterados. Não declarar disponibilidade por existir uma tela, migração ou teste unitário isolado.
