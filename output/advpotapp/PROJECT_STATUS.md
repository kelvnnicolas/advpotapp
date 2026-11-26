# Status — Advpotapp

## Direção colaborativa e comercial — 26/11/2026

Usuário confirmou intenção de cada colaborador usar sua conta Workspace no Advpot e de oferecer o produto a outros advogados/escritórios como instalação licenciada ou SaaS. Delfino permanece a primeira validação; exclusividade da instalação inicial não é exclusividade comercial do produto.

Entregue [detalhamento Workspace e distribuição](docs/product/WORKSPACE_AND_DISTRIBUTION.md): identidade versus consentimento versus participação no escritório, permissões Google/Advpot, recursos institucionais, desligamento, modelos de oferta e fronteiras de isolamento. Fontes oficiais Google verificadas. Atualizados posicionamento, escopo e nota de arquitetura. A direção vem do usuário; as opções técnicas, mecanismos de colaboração e sequência são propostas para o próximo plano.

Somente documentação nesta etapa. Sem alteração de dados, schema, autenticação, integrações, papéis reais, hospedagem ou cobrança. Os testes anteriores validam a instalação local, não SSO/SaaS. Isolamento multiempresa, conexão Google e operação comercial permanecem não implementados; nenhum preço/prazo ou modalidade prioritária foi aprovado.

## Base fictícia e preparação Workspace — 26/11/2026

Usuário autorizou alimentar a aplicação com dados sintéticos e verificar a preparação para dados reais/Workspace. Criado pacote próprio advpot.local-demo.v1: 6 contatos, 8 demandas e 3 envelopes de caso identificados como fictícios. Carga transacional local executada; repetição criou zero demandas novas. Conta teste manteve senha e perfil Profissional, recebeu Secretaria/Comercial e concessões somente aos registros demonstrativos. Auxiliar demo.recepcao sem senha utilizável representa uma origem de passagem. Não foi criada autoridade/administração de negócio nem carregada a base Aurora.

Verificação: 63 testes PostgreSQL aprovados, incluindo navegador; check e migrações sem pendências. [Uso e limites da base](docs/data/LOCAL_DEMO_V1.md). Sem dados reais, arquivos, processos judiciais, documentos, eventos ou operações financeiras simulados como capacidades prontas.

[Preparação Workspace](docs/integrations/GOOGLE_WORKSPACE_READINESS.md) confronta o código com a arquitetura e documentação oficial Google: relações, UUIDs, permissões e transações existentes; faltam OAuth, tokens protegidos, DocumentReference/Appointment, SourceMapping, outbox/worker, adaptadores e testes de reconciliação/falhas. Integração operacional e importação real **não estão prontas**. Drive/Calendar permanecem M3; nenhuma conexão externa ativada, novo serviço, custo ou prazo comercial assumido.

## M2-A — construção autorizada — 25/11/2026

Usuário aprovou desenho e continuidade. Implementado clientes/contatos, demandas vinculadas, pipeline comercial, primeira passagem Secretaria → Comercial com aceite, setor e concessões por registro/ação, histórico e recuperação após revogação. Contratação e financeiro permanecem nos próximos lotes.

Estágio: **em desenvolvimento, verificação técnica local**. PostgreSQL: 60 testes aprovados, três jornadas de navegador e concorrência real. Django check e migrações sem pendências. [Evidências e limites](docs/testing/M2A_VERIFICATION.md). Revisão independente concluída e seis achados relevantes corrigidos com regressões; uma pendência menor de opções de etapa registrada. Sem homologação ou produção. Capturas locais M2-A; nenhuma nova tela publicada no Stitch nesta etapa. Nenhum dado real, carga Aurora, integração ou VPS. Nenhum preço, prazo comercial ou disponibilidade operacional aprovado.

As seções seguintes preservam o registro histórico anterior à implementação do M2-A.

## M2 — desenho baseado no fluxograma da cliente — 25/11/2026

Pedido atual: utilizar a imagem já fornecida pela cliente para criar regras do M2, fluxo e pipelines. A fonte de processo foi definida pelo usuário; não é necessário repetir diagnóstico para redescobrir as seis etapas.

Entregue: evidência transcrita e cópia da fotografia com hash igual ao original; desenho M2 com sequência recepção → comercial → financeiro inicial → organização/distribuição → execução → financeiro final; visões conectadas de atendimento, preparação, execução e acompanhamento financeiro; critérios de passagem, matriz proposta por setor/registro/ação e 30 cenários de aceite. Revisão independente apontou quatro lacunas, tratadas no desenho: inicialização de acesso de negócio, encerramento sem obrigações abertas, recuperação de responsabilidade após revogação e ausência de retrocesso livre. Arquivos relacionados no README e em docs/superpowers/specs/2026-11-25-m2-workflow-design.md.

Estágio: **desenho proposto para revisão**. A imagem fundamenta responsabilidades e entregas; aceite/devolução, concessões, critérios de liberação e exceções são decisões adicionais propostas pelo agente. Nenhum código, migração, carga, tela operacional M2 ou integração foi criado nesta etapa. Os testes do M1 registrados abaixo não validam as propostas do M2.

Dependências para codificação: revisão explícita do desenho e das regras adicionais, seguida de plano de implementação. Homologação exige responsáveis do escritório e cenários executados no ambiente acordado. Financeiro M2 é conferência/liberação e acompanhamento manual; parcelas/recebimentos detalhados continuam no M4. Sem novo preço, prazo, serviço contratado ou disponibilidade operacional declarada.

## Atualização de construção M1 — 24/11/2026

Usuário autorizou “inicie e após atualize prototipagem do projeto no stitch”, após apresentação do recorte M1 e da arquitetura Django/HTMX/PostgreSQL. Esse aceite autoriza a construção da fundação, não a disponibilidade operacional nem todos os módulos.

Estágio: **em desenvolvimento, com verificação técnica local concluída para o recorte descrito**. Aguardando revisão e homologação do responsável; sem aceite da Delfino e sem produção. Base executável em src/, configuração local em scripts/ e deploy/, 28 testes aprovados no PostgreSQL incluindo dois cenários de navegador e concorrência da inicialização. Ver docs/testing/M1_VERIFICATION.md.

Entregue no recorte: sessão interna com CSRF e limite de tentativas, contas/perfis técnicos, desativação e revogação, auditoria restrita, envelope mínimo de caso com leitura/exportação explícitas e busca/paginação autorizadas. Interface portuguesa responsiva e HTMX servido localmente.

Sem carga de dados da cliente ou Aurora. Banco local criado vazio; contas e casos dos testes ficam em banco temporário descartado. Integrações desligadas por ausência de adaptadores/configuração. Nenhuma VPS provisionada, comunicação enviada ou migração executada.

M2–M6 continuam propostos. Pendências antes do piloto/produção: perfis departamentais e acesso operacional por caso, recuperação de conta, MFA privilegiado, HTTPS/proxy/static, monitoramento, backup externo/restauração e aceite. Exportação M1 é do envelope mínimo, não exportação integral do produto.

Prototipagem atualizada no projeto Stitch 10692539038282260634, preservando o sistema Ateliê Jurídico e as referências anteriores; detalhes e IDs em .stitch/metadata.json. Protótipos são material de revisão.

## Registro histórico — estruturação anterior à implementação

Data: 24/11/2026 · America/Sao_Paulo.

## Estruturação

Pedido atendido nesta etapa: reunir posicionamento comercial, dossiê, dados sintéticos, fluxo do escritório e informações públicas da Delfino para preparar a criação da aplicação no diretório solicitado.

Confirmado pelo usuário: primeira versão interna e exclusiva da Delfino. VPS e Workspace derivam do posicionamento anterior. Stack, regras detalhadas, matriz de acesso e marcos são recomendações para revisão.

Foram consultados os documentos do workspace anterior, AGENTS/README/status do dossiê, arquitetura, regras, UX, roadmap, revisões de dados, pacote sintético e cenários complementares; também a fotografia do fluxo e o texto dos 12 slides da proposta preliminar local. O site institucional foi lido no navegador após uma verificação inicial do próprio site.

## Situação técnica

Aplicação executável: não criada. Dependências: não instaladas. Banco: não criado. Dados: nenhuma carga. Serviços externos: nenhum provisionamento, autenticação de conta, envio ou integração ativada. Originais: preservados.

## Conciliações importantes

- VPS substitui a arquitetura de servidor local da apresentação antiga; os preços e prazos daquela apresentação não foram reaproveitados como oferta atual.
- Financeiro aparece no primeiro fluxo como conferência e liberação manual. Parcelas/recebimentos e encerramento dependem de marco específico antes de uma substituição integral do sistema atual.
- U01 sobre entrega/compromisso foi mantida; não foi confundida com prazo fatal.
- Dados de teste pertencem a um escritório fictício, não à Delfino.

## Próxima etapa

Revisar o desenho, fechar as decisões que bloqueiam o lote inicial e autorizar sua implementação. As perguntas de operação, financeiro, Workspace e migração estão classificadas em docs/decisions/OPEN_QUESTIONS.md. Construção e produção possuem critérios distintos.

As verificações documentais desta entrega ficam registradas em docs/testing/DELIVERY_CHECK.md. Nenhum resultado de pesquisa ou auditoria local foi apresentado como teste funcional do Advpotapp.
