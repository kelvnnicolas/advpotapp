# Google Workspace — preparação e limites

26/11/2026. Verificação do código atual e das decisões do projeto. Preparação arquitetural documentada; integração operacional ainda não implementada ou homologada. Nenhuma conta, pasta, agenda, token, permissão ou dado real foi conectado por esta entrega.

## O que existe e o que falta

| Necessidade | Situação atual | Entrega antes de dados reais |
| --- | --- | --- |
| Registros jurídicos como fonte principal | Contact, Demand, Case; vínculo contato/demanda; UUIDs, autoria e versões | Fechar mapeamento dos campos reais por lote; casos atuais ainda são envelopes mínimos |
| Autorização interna | Setor + ação por registro, histórico, revogação | Revisar matriz com responsáveis reais; acesso interno nunca substitui permissão Google |
| Continuidade do fluxo | Serviços transacionais e chaves de repetição locais | Outbox persistente e worker ainda ausentes; não executar Google dentro da transação da demanda |
| Documentos no Drive | Diretriz ADR-006; conteúdo no Drive, metadados no Advpot | DocumentReference, vínculo a registro, fileId/driveId, confirmação de propriedade/permissão, adaptador e reconciliação |
| Compromissos no Calendar | Datas de próximo passo são acompanhamento, não prazo fatal | Appointment com início/fim/fuso e opt-in de publicação; calendarId/eventId e adaptador. Não publicar automaticamente next_step_on |
| Autorização Google | Nenhuma configuração OAuth implementada | Projeto Cloud institucional, APIs habilitadas, consentimento, redirect URI, escopos mínimos e responsáveis indicados |
| Credenciais | Segredos locais fora do repositório | Armazenamento protegido de refresh tokens, renovação, revogação, rotação e erros sanitizados; login Advpot e conexão Google separados |
| Importação real | Nenhum importador de cliente ou sincronização Google | Staging, origem/versão/source_id → UUID interno, relatório de rejeições, reconciliação e retorno; não usar a carga demonstrativa como importador |
| Operação | Ambiente local de revisão | HTTPS, recuperação privilegiada, backup externo/restauração, monitoramento e aceite antes do piloto |

## Recorte recomendado para o marco M3

Drive primeiro: seleção explícita de arquivos/pasta institucionais, metadados e vínculo a demanda/caso autorizado. Considerar `drive.file` para arquivos criados/abertos/compartilhados com o aplicativo; não presumir que esse escopo permita varrer todo o acervo existente. Definir My Drive versus drive compartilhado com a equipe; shared drives exigem suporte próprio e parâmetros como `supportsAllDrives` nas operações documentadas. [Escopos oficiais](https://developers.google.com/workspace/drive/api/guides/api-specific-auth), [suporte a drives compartilhados](https://developers.google.com/workspace/drive/api/guides/enable-shareddrives).

Calendar depois: publicação unidirecional opt-in de compromisso escolhido, agenda institucional definida e referência interna mínima. Registrar início/fim/fuso America/Sao_Paulo, identificador externo e estado de sincronização. Não enviar convidados no primeiro recorte; configurar lembretes explicitamente e não tratar `sendUpdates=none` isoladamente como garantia de ausência de e-mails. O recurso diferencia id e iCalUID; um UUID interno não deve ser enviado com hífens como event id, cujo alfabeto é próprio. [Referência oficial events.insert](https://developers.google.com/workspace/calendar/api/v3/reference/events/insert).

Essas são recomendações de desenho, não decisões de consentimento/escopos já aprovadas. Não usar conta pessoal ou delegação ampla de domínio por inferência. Gmail, comunicações, IA e importação de todo o Workspace exigem escopo próprio.

## Aceite mínimo da integração futura

1. Identificar domínio/conta autorizada, proprietário da pasta, agenda de destino, grupos e responsável por revogar acesso.
2. Validar matriz campo a campo e piloto com dados fictícios em pasta/agenda de homologação segregadas.
3. Registrar operação externa no mesmo commit de domínio; worker reivindica com lease, tentativas e backoff, sem duplicar a ação após resposta perdida.
4. Testar token revogado, escopo insuficiente, arquivo movido/excluído, permissão divergente, indisponibilidade, timeout após sucesso e conflitos de alteração. Exibir falha e permitir retomada autorizada.
5. Testar segredo fora de logs/exports, acesso por registro, reconciliação de IDs, backup/restauração e exportação/saída.
6. Fazer dry-run do lote real autorizado, conferir totais/rejeições/relacionamentos com o escritório e obter aceite antes da carga definitiva.

Conclusão verificável: a fundação é compatível com a evolução planejada para Drive/Calendar, mas faltam componentes e testes específicos. Não é correto declarar pronta a integração de dados reais hoje. A carga sintética local não aciona ou comprova integração Google.
