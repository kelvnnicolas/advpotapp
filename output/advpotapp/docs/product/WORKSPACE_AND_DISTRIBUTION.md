# Advpot colaborativo, Google Workspace e distribuição comercial

26/11/2026. Direção confirmada pelo usuário: colaboradores devem usar suas próprias contas Workspace para integrar e trabalhar em conjunto no Advpot; o produto deve poder ser oferecido a outros advogados e escritórios como instalação licenciada ou SaaS. Delfino permanece a primeira validação. Esta confirmação altera a direção de produto, mas não autoriza tratar SSO, integrações ou isolamento multiempresa como implementados.

## 1. Resultado esperado

Advpot organiza clientes, demandas, casos, responsáveis, passagens e histórico; Workspace oferece identidade e colaboração documental/agenda. O escritório trabalha sobre os mesmos registros autorizados, sem planilhas paralelas como fonte jurídica principal ou senha Google compartilhada. As funções ainda não implementadas de tarefas, prazos e documentos conservam seus lotes próprios.

Exemplo futuro: a recepção registra demanda; o Comercial a aceita; o advogado autorizado consulta o contexto e abre o documento institucional vinculado. Uma colega com acesso ao mesmo caso revisa esse documento no Google Docs. Um compromisso escolhido é publicado na agenda institucional autorizada. Autoria e estado da integração ficam rastreáveis no Advpot. Documentos colaborativos são editados no Google; a aplicação atual não oferece coedição em tempo real dos seus próprios formulários.

## 2. Três controles separados

| Camada | Pergunta respondida | Regra de produto |
| --- | --- | --- |
| Entrada com Google | Quem está entrando? | Login individual proposto via OpenID Connect; não importa arquivos nem concede acesso a casos |
| Conexão Drive/Calendar | Quais operações Google foram autorizadas? | OAuth por capacidades necessárias; consentimento e políticas do Workspace podem limitar ou bloquear a conexão |
| Participação no escritório | O que essa pessoa pode fazer no Advpot? | Convite/admissão pelo escritório, participação ativa, setor e ação por registro; conexão Google não vira administração do escritório |

O Google distingue identidade persistente (`sub`) de e-mail, que pode mudar; restrições de domínio exigem validação no servidor. Domínio é um sinal de admissão, não identificador suficiente do escritório no SaaS. [OpenID Connect oficial](https://developers.google.com/identity/openid-connect/openid-connect).

Um usuário autenticado não entra automaticamente em todo escritório com o mesmo domínio. Participar de mais de um escritório, caso oferecido, exige admissão explícita em cada um e seleção de contexto; tokens, papéis e ações nunca atravessam esse contexto implicitamente. Associar conta Google a conta Advpot existente exige comprovar ambas as identidades, sem vínculo automático apenas por e-mail recebido.

## 3. Experiência futura do usuário e da equipe

1. O responsável provisiona o escritório e suas configurações; convida/admite colaboradores por fluxo próprio do Advpot. Esse convite ainda não existe e nenhum envio externo é autorizado por este documento.
2. O colaborador entra com sua identidade Google e recebe somente os acessos aprovados para o escritório. Login Google é evolução; hoje a autenticação é local.
3. Ao usar uma capacidade Google pela primeira vez, conecta a conta e autoriza os escopos pertinentes. Não precisa entregar sua senha Google ao Advpot. O administrador Workspace pode exigir liberação do aplicativo. [Controle administrativo Google](https://knowledge.workspace.google.com/admin/apps/control-which-apps-access-google-workspace-data).
4. O escritório define pasta/drive e agenda institucionais. O Advpot vincula os objetos aos registros jurídicos; não importa toda a conta ou concede compartilhamento amplo automaticamente.
5. Colaboradores acessam os mesmos registros conforme a matriz interna. Para abrir/editar conteúdo no Google, também precisam das permissões daquele serviço. Uma divergência de acesso deve resultar em aviso e revisão autorizada, não em ampliação silenciosa de permissões.
6. Alterações no Advpot conservam autoria, versão e histórico. Operações externas ganham estados pendente/concluída/falhou e retomada autorizada; indisponibilidade Google não impede salvar a operação jurídica local.
7. No desligamento, remover a participação no escritório, invalidar suas sessões e bloquear o uso local de seus tokens imediatamente. Revogar a autorização Google pelo fluxo pertinente e revisar membros/grupos e compartilhamentos Google é trabalho adicional; retirar acesso no Advpot não apaga uma permissão concedida diretamente no Drive.

## 4. Documentos, agenda e propriedade

Recomendação: recursos institucionais, não arquivos presos à conta pessoal de um colaborador. Drives compartilhados têm organização e propriedade coletivas próprias; disponibilidade e política devem ser conferidas na conta do cliente. Isso sustenta continuidade quando alguém deixa a equipe, sem substituir permissões por item. [Drives compartilhados](https://developers.google.com/workspace/drive/api/guides/about-shareddrives).

O conteúdo permanece no Drive; o Advpot conserva vínculo, metadados e controle jurídico. Calendar recebe compromissos explicitamente escolhidos; próxima ação, entrega e prazo fatal permanecem distintos. Google Docs/Sheets/Slides podem ser vinculados como arquivos, mas automações ou edição programática específica têm escopo próprio. Gmail, WhatsApp, IA e importação de todo o Workspace não entram por consequência desta direção.

Licenças Workspace e acesso Advpot são contratações distintas, salvo composição expressamente definida na oferta. Conectar uma conta não inclui licenças Google nem dispensa políticas do administrador.

## 5. Duas modalidades comerciais

Atualização desta avaliação em 26/11/2026: o usuário escolheu priorizar assinatura por escritório com colaboradores incluídos. [Conta Business, checkout e liberação de acesso](BUSINESS_SAAS_EVALUATION.md). Instalação licenciada continua alternativa futura; número de vagas, frequência, preço, provedor e isolamento ainda precisam ser definidos.

| Modalidade | Entrega a definir | Responsabilidade a fechar | Limite atual |
| --- | --- | --- | --- |
| Instalação licenciada por escritório (“cópia do sistema”) | Mesma versão do produto, instalação/configuração independente, marca e fluxos nos limites contratados | Operador da VPS, banco, backup, atualização, domínio, projeto OAuth, suporte e direito de acesso ao código | Licença de uso não define sozinha cessão de código, exclusividade ou customização ilimitada |
| SaaS gerenciado | Serviço hospedado pelo fornecedor, com ambiente lógico/operacional de cada escritório e gestão de adesão/assinatura | Operação, isolamento, suporte, atualização, cotas, recuperação, exportação e encerramento | Mecanismo multiempresa, cobrança e provisionamento ainda não implementados |

As duas ofertas podem compartilhar o mesmo produto e versões. Recomenda-se configuração por escritório em vez de manter um fork permanente por cliente; isso é recomendação técnica, não escolha comercial já aprovada. SaaS não exige necessariamente banco compartilhado: instâncias/bancos separados e armazenamento compartilhado com isolamento são alternativas a avaliar. Nenhuma foi escolhida para esta expansão.

Autenticação Google para clientes de organizações diferentes requer desenho de aplicativo externo, escopos e eventual verificação segundo a categoria de acesso; a configuração interna de uma única organização não pode ser simplesmente reaproveitada como habilitação geral de SaaS. Definir quem controla o projeto OAuth nas instalações licenciadas. [Consentimento e categorias de escopos Google](https://developers.google.com/workspace/guides/configure-oauth-consent).

## 6. Fronteira obrigatória antes do SaaS

- Organização/escritório com identificador próprio e participação de usuários explícita; eliminar autoridade e filas globais de negócio. Os singletons atuais pertencem a uma instalação e não são seguros como gestão multiempresa compartilhada.
- Isolar registros, contatos, referências, concessões, histórico, buscas/contagens, exportações, sessões/contexto, credenciais, jobs e armazenamento por escritório. Uma migração deve associar os dados atuais ao primeiro escritório, sem misturá-los a novas contas.
- Revisar unicidades, locks e chaves de repetição por fronteira de organização; testar troca de contexto, tarefas assíncronas e acesso por ID de outro escritório, inclusive administrador do serviço.
- Credenciais de integração vinculadas ao escritório, identidade autorizada e escopos; armazenamento protegido, rotação/revogação e auditoria sem segredos. Não compartilhar um refresh token entre clientes ou adotar delegação ampla por inferência.
- Separar suporte da operação jurídica: administração do serviço não concede leitura dos casos; eventual acesso assistido exige autorização, prazo e trilha própria.
- Definir exportação, retenção, cancelamento, restauração por escritório, cotas e suporte. Preço e cobrança dependem de escopo próprio e custo total apurado.

## 7. Situação e sequência de validação

Implementado para revisão local: fundação M1, recorte operacional M2-A e base fictícia autorizada, com permissões por registro na instalação única. Não há SSO Google, conexão Drive/Calendar, múltiplos escritórios isolados, provisionamento, planos ou cobrança SaaS.

Sequência proposta: fechar documento de identidade/colaboração e modalidade de primeira comercialização; manter recorte operacional M2; implementar identidade Google e isolamento na ordem exigida pelo próximo piloto; executar Drive/Calendar com ambiente institucional de homologação; testar dois escritórios sintéticos sem vazamento; só depois homologar implantação comercial. Isolamento precisa preceder qualquer convivência real entre escritórios no mesmo ambiente, e os dados fictícios não vão para produção.

O próximo plano técnico deve comparar alternativas, dependências, impacto de migração/custo e aceites antes de alterar schema ou autenticação. A prioridade de avaliação agora é assinatura Business por escritório. Permanecem pendentes responsáveis/contas reais, plano/vagas/preço/frequência, gestão de infraestrutura/OAuth, provedor de pagamento e condições da oferta. Não bloqueiam o detalhamento solicitado, mas impedem declarar a plataforma já pronta para comercialização.
