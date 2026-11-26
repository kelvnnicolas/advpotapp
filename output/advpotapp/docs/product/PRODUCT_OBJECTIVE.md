# Objetivo do produto — Advpot

Referência para decisões de software. Consolidada em 26/11/2026. O objetivo abaixo descreve o destino do produto; implementar somente o checkpoint autorizado e consultar o status antes de declarar uma capacidade pronta.

## 1. Objetivo principal

Permitir que um escritório jurídico acompanhe cada demanda da recepção ao encerramento, com cliente vinculado, responsável atual, próximo passo, documentos relacionados e histórico, enquanto seus colaboradores trabalham sobre os mesmos registros autorizados.

Na evolução SaaS Business, o escritório será a unidade de participação, configuração e assinatura. O acesso dependerá de identidade, participação ativa, direito de uso vigente e permissão para a ação/registro. Workspace será uma camada de colaboração com autorização separada.

## 2. Problemas que o produto deve resolver

- Demanda perde contexto ou responsável ao passar entre setores.
- Cadastros e informações são repetidos sem vínculo claro entre atendimento, cliente e caso.
- A equipe não consegue distinguir próxima ação, entrega de tarefa, compromisso e prazo fatal.
- Documento ou agenda ficam separados do contexto jurídico, ou associados a acesso inadequado.
- Gestão comercial/técnica é confundida com autorização para ler conteúdo jurídico restrito.
- Um produto replicado para novos escritórios mistura configurações, registros, usuários ou credenciais.

Não transformar essas necessidades em alegações de resultados quantitativos sem medição.

## 3. Fluxo de referência

Recepção/Secretaria → Comercial → Financeiro inicial → Organização/distribuição/Secretaria → Execução/Operacional → Financeiro final.

A fotografia da cliente é a fonte do fluxo inicial, detalhada em [DELFINO_FLOW_EVIDENCE.md](../context/DELFINO_FLOW_EVIDENCE.md). O recebimento deve ser explícito: a origem continua responsável até o aceite. Devoluções preservam motivo e histórico. Uma demanda não é duplicada para aparecer em quadros de setores diferentes.

Cada escritório poderá ter configuração autorizada, sem apagar responsabilidades ou mudar silenciosamente regras de demandas em andamento. A sequência, exceções e campos de outros escritórios precisam de revisão; não presumir que o fluxo Delfino é universal.

## 4. Conceitos que devem permanecer separados

| Conceito | Significado no produto |
| --- | --- |
| Contato/cliente | Pessoa ou organização; pode ter várias demandas |
| Demanda/atendimento | Necessidade em acompanhamento, com responsável e próximo passo |
| Oportunidade | Tratamento comercial da demanda; não significa contratação ou recebimento |
| Contratação | Condições formalizadas e versionadas no lote próprio |
| Caso | Contexto de execução jurídica; pode existir sem processo judicial |
| Processo judicial | Referência judicial quando aplicável; não é obrigatório para todo caso |
| Tarefa/entrega | Trabalho atribuído e compromisso de entrega |
| Prazo fatal | Data jurídica informada/confirmada com origem e responsabilidade próprias |
| Compromisso de agenda | Evento interno/publicável por autorização; não nasce automaticamente de um prazo |
| Assinatura Business | Direito de uso do Advpot pelo escritório; independente de honorários dos clientes |

## 5. Critérios observáveis de sucesso

| Resultado esperado | Evidência necessária |
| --- | --- |
| Continuidade da demanda | Localizar responsável, estado e próximo passo; passagem aceita/devolvida sem duplicação |
| Colaboração com controle | Dois colaboradores autorizados trabalham no mesmo contexto; quem não tem acesso não o encontra por lista, busca, contagem, URL ou exportação |
| Histórico confiável | Alterações relevantes preservam autoria, instante, versão e motivo quando exigido |
| Resiliência de integração | Falha/revogação Google fica visível e retomável, preservando o registro jurídico |
| Isolamento Business | Dois escritórios sintéticos não acessam dados, credenciais ou jobs um do outro |
| Direito de uso controlado | Pagamento/renovação confirmado pelo servidor altera validade; sessão aberta não contorna expiração |
| Saída e recuperação | Exportação e restauração documentadas e verificadas no escopo contratado |

Esses aceites pertencem aos respectivos lotes; não são todos cobertos pela suíte local existente. Metas de desempenho/adoção precisam de linha de base e definição com o usuário.

## 6. Limites e prioridade de construção

Primeiro comprovar a operação jurídica e as permissões no recorte acordado. Para o Business, a ordem solicitada é frontend com rotas/contrato, depois backend/banco e isolamento, depois cobrança e conexões reais conforme decisões e aceites próprios.

Estado consolidado em 26/11/2026: M1 e M2-A implementados para revisão local; frontend Business demonstrativo validado; modelo de domínio proposto. Backend/banco Business, multiempresa, assinatura real, checkout, SSO e Drive/Calendar ainda não implementados. A suíte registrada de 74 testes não comprova essas capacidades futuras. Confirmar sempre o [status atual](../../PROJECT_STATUS.md) e a [verificação Business](../testing/BUSINESS_FRONTEND_VERIFICATION.md).

Fora de escopo por inferência: captura de tribunais, contagem automática de prazo, operação bancária, envio de comunicação, importação real, acesso amplo ao Google, construtor ilimitado de automações ou IA obrigatória. Usar VPS como diretriz inicial e preservar stack aprovada; nova decisão técnica precisa registrar alternativas e impacto.

## 7. Aceite de uma entrega

Uma entrega deve identificar problema, usuário, fluxo, regras, limites, dependências, estágio e evidência. Incluir caminhos de falha, negação de acesso e comportamento com integração indisponível quando aplicável. Frontend de prévia não equivale a persistência; teste técnico não equivale a homologação; merge no GitHub não equivale a produção.

Consultar o [guia para agentes](../project/AGENT_PRODUCT_BRIEF.md), o [posicionamento](../business/BUSINESS_POSITIONING.md), o [modelo Business](../data/BUSINESS_DOMAIN_MODEL.md) e o [roteiro](../delivery/BUILD_ROADMAP.md) antes de transformar objetivo em implementação.
