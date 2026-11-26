# Definição do produto

Versão 1 · Proposta funcional para validação. Nenhum recurso abaixo está comprovado como implementado nesta pasta.

Atualização de direção em 26/11/2026: colaboração com Workspace individual e distribuição do produto a outros escritórios por instalação licenciada ou SaaS. O blueprint passa a prever identidade, participação no escritório e integrações como controles separados. Isolamento entre escritórios é requisito anterior ao uso multiempresa; não capacidade existente. [Detalhamento](WORKSPACE_AND_DISTRIBUTION.md).

## Recorte recomendado

Primeiro comprovar o fluxo atendimento → cliente → caso/processo → tarefa/prazo → documento → acompanhamento. Organizar o trabalho em núcleo e lotes conectados, evitando contratar um sistema amplo sem critérios de conclusão.

| Lote proposto | Conteúdo | Limite |
| --- | --- | --- |
| Núcleo operacional | Acesso, perfis, clientes/contatos, CRM Kanban, casos/processos, tarefas, prazos informados, painel e histórico | Sem captura judicial ou cálculo automático de prazos |
| Conexão Workspace | Drive e Calendar, com direção e permissões definidas | Não equivale a Gmail, Docs, Sheets e Meet integrados |
| Gestão ampliada | Financeiro gerencial e relatórios específicos | Sem contabilidade, conciliação ou pagamentos bancários implícitos |
| Evolução | Gmail, automações e IA opcional | Levantamento e contratação próprios |

Os dois primeiros lotes compõem a oferta inicial recomendada, mas podem ter marcos e aceites separados. Não apresentar o núcleo isolado como uma integração Workspace já entregue.

## Papéis propostos

Administrador gerencia acessos e configuração; gestor acompanha a operação autorizada; profissional executa o trabalho atribuído; apoio atua nos cadastros e tarefas permitidos. Acesso financeiro é uma permissão específica. Validar uma matriz por recurso e ação: visualizar, criar, editar, concluir, exportar e administrar.

Aplicar restrições também em buscas, painéis, exportações e documentos. Desativar um usuário revoga acesso e exige reassociação das responsabilidades abertas.

## Regras e aceite por fluxo

| Fluxo | Regra proposta | Aceite demonstrável |
| --- | --- | --- |
| Atendimento | Oportunidade tem responsável, etapa, origem e próximo passo; registrar motivo de perda | Mover etapa registra autor/data; conversão reutiliza cadastro existente |
| Cliente | Separar pessoa/organização, contato e papel no caso; alertar possível duplicidade sem bloquear homônimos | Busca localiza cadastro; conversão não duplica por repetição da ação |
| Caso/processo | Caso pode existir antes de processo judicial; relacionar pessoas por papel e permitir múltiplos processos por caso | Abrir o caso apresenta vínculos, responsáveis e atividades autorizadas |
| Tarefa | Responsável obrigatório, estado e vencimento quando aplicável; conclusão e reabertura têm histórico | Alterações aparecem no histórico; arquivar caso alerta sobre tarefas abertas |
| Prazo | Data informada e validada pelo profissional; registrar origem, responsável e confirmação | Alteração conserva valor anterior e autoria; conclusão exige registro explícito |
| Agenda | Distinguir compromisso de prazo; exibir situação da integração | Falha externa deixa pendência visível e preserva o registro no Advpot |
| Documento | Vincular documento a cliente/caso com identificador externo e estado de acesso | Arquivo sem acesso gera mensagem tratável, sem expor conteúdo restrito |
| Financeiro futuro | Separar previsão, vencimento e recebimento; correções preservam histórico | Previsto não entra como recebido no painel |
| Painel | Indicador tem definição, período, filtro e origem dos dados | Total corresponde à lista que o usuário autorizado consegue consultar |

Estados candidatos: oportunidade aberta/ganha/perdida; caso ativo/suspenso/encerrado/arquivado; tarefa pendente/em andamento/concluída/cancelada. Validar transições com a equipe. Vencimento deve ser uma condição calculada a partir de data e estado, preservando o histórico.

Alertas auxiliam a rotina, mas não concluem tarefas, confirmam prazos nem substituem conferência profissional. Não inferir contagem processual, feriados ou publicação judicial.

## Integrações Workspace: contrato funcional proposto

**Calendar:** começar com publicação unidirecional de compromissos aprovados do Advpot para uma agenda definida. O prazo jurídico permanece no Advpot. Edições externas não sobrescrevem automaticamente seus dados. Validar tratamento de cancelamento, participantes, fuso e alterações feitas diretamente na agenda.

**Drive:** começar com criação controlada de estrutura e vinculação de arquivos/pastas em conta institucional. Confirmar se o plano e a configuração permitem drives compartilhados; definir alternativa quando não permitirem. Evitar propriedade em contas pessoais. Não criar links públicos por padrão. Permissão no Advpot não concede nem revoga automaticamente permissão no Drive.

Ambas devem prever autorização pelo administrador, acesso mínimo necessário, tokens protegidos, identificador externo, prevenção de duplicação, novas tentativas limitadas e registro de falha. Credencial revogada, indisponibilidade, limite de chamadas e exclusão externa precisam de tratamento visível. Definir como reconciliar acessos entre os sistemas.

A viabilidade técnica, os requisitos de autorização e as restrições do plano devem ser conferidos na documentação oficial vigente antes de estimar ou implementar. Estes limites são uma proposta de comportamento, não confirmação de capacidade já validada.

## Estrutura técnica a definir

Arquitetura lógica: aplicação e banco em VPS; documentos no Drive quando contratado; cópias externas ao servidor; integrações em processamento controlado. Seleção de tecnologias e dimensionamento seguem decisão registrada após diagnóstico.

Entidades candidatas: usuário, perfil, cliente/contato, oportunidade, caso, participação no caso, processo, tarefa, prazo, compromisso, vínculo documental, evento de auditoria e execução de integração. Lançamentos financeiros entram no lote específico.

Requisitos estruturais propostos: conexão protegida, controle de acesso no servidor, proteção de segredos, histórico de ações críticas, ambientes de teste e produção separados, monitoramento, procedimento de atualização e recuperação. Auditoria deve restringir acesso e evitar cópias desnecessárias de dados sensíveis.

Definir antes da produção: frequência/retenção dos backups, perda máxima aceitável de dados, tempo-alvo de recuperação e procedimento de teste. Backup no mesmo servidor não atende à cópia externa. Dados e documentos exigem estratégias compatíveis; vínculo com Drive não é backup do arquivo.

Exportar cadastros e relações em formato documentado, com inventário de arquivos e instruções de obtenção do conteúdo. Acesso a código e migração assistida são condições comerciais separadas.

## Critério de conclusão

Um recurso só passa a disponível após verificação do fluxo, das restrições de acesso e dos principais erros; documentação de uso; aceite registrado; e publicação no ambiente acordado. Demonstrações e telas com dados fictícios permanecem identificadas como tal.
