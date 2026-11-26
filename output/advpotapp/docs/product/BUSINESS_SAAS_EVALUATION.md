# Avaliação — conta Business, checkout e acesso por assinatura

26/11/2026. Direção proposta pelo usuário: conta Business administra colaboradores e fluxos; contratação com checkout; login libera uso conforme pagamento; sem teste gratuito. Na avaliação, o usuário escolheu priorizar **assinatura por escritório, com colaboradores incluídos**. A periodicidade, preço, quantidade incluída, provedor e política de atraso ainda não foram definidos. Este documento avalia o caminho; não é autorização de implementação financeira nem declaração de prontidão comercial.

## 1. Parecer e recorte recomendado

É um caminho coerente para um SaaS gerenciado por escritório. Recomenda-se um plano Business inicial e checkout hospedado por provedor, sem trial ou cartão tratado diretamente pelo Advpot. Contratação e administração ficam com o responsável Business; cada colaborador mantém login individual e não precisa comprar uma assinatura pessoal para participar.

O número de colaboradores incluídos precisa ser explícito antes da venda; não se presume uso ilimitado. Um advogado individual pode iniciar com apenas seu próprio usuário. A oferta de instalação licenciada permanece alternativa futura; a prioridade desta avaliação é a assinatura hospedada por escritório.

“Sem teste de produto” é interpretado como sem período gratuito para o cliente. Homologação técnica, testes de cobrança em sandbox e isolamento entre escritórios continuam necessários antes de cobrar clientes reais. Nenhuma transação ou conexão de provedor foi criada.

## 2. Caminho de contratação e entrada

1. Usuário se identifica na entrada única; quem já tem escritório ativo segue para o trabalho. Login Google é evolução planejada, ainda não implementada.
2. Quem contrata informa os dados mínimos do escritório e se torna o responsável Business. O registro começa pendente, sem acesso operacional ou dados jurídicos reais.
3. O servidor cria uma sessão de checkout vinculada àquele escritório e ao plano/preço cadastrado no servidor. O navegador não define valor, produto ou escritório a ativar.
4. O provedor confirma o pagamento pelo canal servidor-servidor. O Advpot valida assinatura do evento, ambiente, cliente/assinatura e vínculo ao Business, processa sem duplicar e registra validade do acesso.
5. Após confirmação, o responsável entra, configura a equipe e recursos institucionais. Retorno do checkout pode mostrar “aguardando confirmação” enquanto o processamento ocorre.
6. Colaboradores admitidos entram pela mesma rota e usam o escritório conforme assinatura, participação e permissões. Um colaborador sem autoridade de cobrança não vê dados de faturamento nem compra outro plano para resolver a inadimplência do escritório.

O checkout não obriga criar uma landing page, free trial, marketplace ou vários planos. Uma entrada com “Entrar” e “Contratar” pode ser suficiente para a primeira oferta; ainda requer fluxos técnicos de retorno, faturamento e webhook, mesmo que não apareçam como páginas de produto.

## 3. Regra de acesso

Autorizar uma operação exige identidade ativa, participação ativa no escritório selecionado, assinatura com direito de uso vigente e permissão para a ação/registro. A verificação acontece no servidor também nas requisições posteriores ao login. Alterar a URL, conservar uma sessão aberta ou obter um ID de outro escritório não pode contornar a regra.

Persistir o estado da assinatura e a validade confirmada localmente, atualizados por eventos e reconciliação. Não chamar o provedor a cada login/requisição nem guardar apenas `pagou=True`: renovações, vencimento, cancelamento e pagamento pendente têm efeitos diferentes. Workspace e assinatura Advpot são vínculos distintos; desativar o SaaS não deve apagar arquivos Google ou cobranças de honorários dos clientes do escritório.

| Situação proposta | Comportamento recomendado |
| --- | --- |
| Contratação pendente ou primeiro pagamento recusado | Sem acesso operacional; responsável pode concluir/regularizar a contratação |
| Pagamento confirmado e período vigente | Operação e colaboração liberadas dentro do plano e das permissões |
| Renovação falhou, mas período já pago ainda não terminou | Preservar o acesso desse período; orientar o responsável a regularizar |
| Validade paga encerrada sem renovação confirmada | Suspender operações do produto; manter entrada para regularização e rotas de saída autorizadas |
| Cancelamento programado para o fim do período pago | Manter uso até a data de validade confirmada, se essa política for adotada |
| Reembolso, contestação ou cancelamento imediato | Aplicar política explicitamente definida antes da venda; não inferir exclusão de dados ou efeitos a partir de um único evento |

Tolerância de atraso, período de retenção, exportação durante suspensão e efeitos de reembolso precisam entrar na política comercial e no aceite. A proposta é não apagar dados automaticamente por falha de pagamento. Suspensão de acesso não conclui tarefas, altera prazos ou apaga histórico jurídico.

## 4. Administração Business e fluxos

O responsável Business administra somente seu escritório: membros, papéis, vagas do plano, situação da assinatura e configurações autorizadas. Administração de faturamento não concede por si leitura de casos restritos; separar gestão do escritório de acesso jurídico. Não transformar o papel técnico global access_admin atual em dono de todos os clientes SaaS.

Para a primeira versão vendável, recomenda-se configurar responsáveis, setores e modelos de fluxo dentro das regras aprovadas, com histórico de mudanças. Construtor livre de automações/pipelines e alteração de pré-condições legais/financeiras ficam fora do recorte inicial; não prometer personalização ilimitada. Trocas de configuração precisam ser versionadas para não mudar silenciosamente demandas em andamento.

Convites são propostos, sem envio nesta avaliação. Definir contagem de vagas, reserva/expiração de convites e tratamento de redução de limite sem apagar membros ou reatribuir tarefas arbitrariamente. Conta Workspace de cada colaborador autentica e autoriza suas integrações; não é licença de acesso a qualquer Business.

## 5. O que falta na aplicação atual

| Componente | Situação atual | Trabalho antes de venda |
| --- | --- | --- |
| Business/Organization e Membership | Ausentes; contas e setores pertencem a uma instalação única | Fronteira de escritório, dono/administração, participação e contexto ativo |
| Isolamento | Concessões por registro locais; autoridade e recuperação com singleton global | Escopo em todos os dados, consultas, grants, histórico, jobs, credenciais e operações administrativas; migração do primeiro escritório |
| Plano e assinatura | Ausentes | Plano, vagas, identificadores do provedor, validade e estado de acesso |
| Checkout | Ausente | Sessão vinculada ao escritório, retomada sem duplicar, confirmação em ambiente correto |
| Eventos de cobrança | Ausentes | Webhook autenticado, idempotência, eventos fora de ordem, reconciliação e trilha sanitizada |
| Porta de acesso | Só autenticação/permissões atuais | Validar Business + assinatura em cada ação e manter rotas restritas de regularização/saída |
| Gestão de equipe/fluxos por escritório | Administração técnica global e fluxo M2-A | Interface restrita ao Business e configurações versionadas permitidas |
| Google Workspace | Planejado, sem SSO/adaptadores | Identidade e conexão por escritório/usuário, escopos e recursos institucionais homologados |
| Operação comercial | Ambiente local com base fictícia | HTTPS, recuperação privilegiada, backup/restauração, monitoramento, suporte e política de saída |

Adicionar uma checagem de pagamento ao login atual não resolve os componentes ausentes. O software ainda não é vendável como SaaS multiempresa só por ganhar checkout. Os 63 testes atuais validam o recorte local; não provam faturamento ou isolamento.

## 6. Alternativas de cobrança e isolamento

**Cobrança:** Stripe Billing/Checkout e Mercado Pago Assinaturas são candidatos a comparar. Stripe documenta ciclo de assinatura e confirmação por eventos; Mercado Pago oferece API de assinaturas e pagamentos recorrentes. Escolher após verificar disponibilidade para a conta vendedora, meios de pagamento realmente compatíveis com recorrência, custos, conciliação, suporte e exportação. Nenhum provedor foi escolhido, conectado ou instalado nesta avaliação; não há taxas ou preços aprovados.

**Isolamento:** comparar ambiente/banco por escritório com aplicação multiempresa compartilhada. O primeiro aumenta operação por cliente; o segundo exige revisão extensiva de toda autorização e de migrações. SaaS é modalidade de prestação e pode usar qualquer uma dessas estratégias. Registrar decisão e impacto antes do schema; nenhum segundo escritório real deve entrar no ambiente atual sem esse trabalho.

**Recomendação de implementação futura:** manter checkout hospedado e adaptador de faturamento separado das regras de direito de uso. Não desenvolver armazenamento de cartão nem misturar faturamento do Advpot com o módulo financeiro jurídico dos clientes.

## 7. Marcos e aceites propostos

1. Definir plano Business: vagas, frequência, preço, cancelamento, atraso, suporte e saída; selecionar provedor e estratégia de isolamento.
2. Implementar Business/Membership e migração da instalação inicial; provar que dois escritórios sintéticos não acessam dados, buscas, exportações ou tarefas assíncronas um do outro.
3. Implementar dono/equipe/configuração de fluxo e acesso por participação. Validar que o administrador de um escritório não administra o outro.
4. Integrar checkout e cobrança em sandbox; validar primeiro pagamento, renovação, recusa, cancelamento, retorno ausente, evento inválido/repetido/atrasado e reconciliação. Um evento antigo não pode reativar assinatura suspensa indevidamente.
5. Implementar a porta de acesso e regularização; testar expiração com sessão já aberta e colaborador removido, mantendo histórico e saída conforme a política escolhida.
6. Homologar Google Workspace e operação, delimitar capacidades já utilizáveis na oferta e só então habilitar cobrança real com autorização própria.

## Referências oficiais consultadas

Stripe informa que a liberação não deve depender apenas da página de retorno do checkout; confirmação assíncrona precisa de webhook. [Checkout e fulfillment](https://docs.stripe.com/checkout/fulfillment.md?ui=full-page).

Stripe documenta eventos de pagamento e assinatura para atualização do acesso ao serviço; no seu fluxo, pagamento da fatura e estado de assinatura devem ser avaliados juntos. [Webhooks de assinatura](https://docs.stripe.com/billing/subscriptions/webhooks).

Mercado Pago descreve assinaturas por API, periodicidade e cobrança recorrente; condições específicas do vendedor e meio escolhido devem ser conferidas no momento de integrar. [Assinaturas](https://www.mercadopago.com.br/developers/pt/docs/subscriptions/overview).
