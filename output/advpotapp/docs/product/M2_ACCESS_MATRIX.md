# M2 — matriz proposta de acesso

25/11/2026. Derivada das responsabilidades IMG-01–07, não de uma matriz de segurança fornecida pela cliente. Desenho aprovado pelo usuário para construção em 25/11/2026; M2-A implementa o subconjunto indicado em M2A_VERIFICATION.md. Homologação operacional permanece pendente.

Cada célula significa uma capacidade de setor. Para consultar/alterar um registro, exigir também concessão explícita por demanda/caso e ação. “Gestão” não é superusuário e não abre todos os casos. Sem capacidade ou concessão: negar. Nenhuma atribuição será criada automaticamente a partir das contas M1.

| Ação de negócio | Secretaria | Comercial | Financeiro | Operacional | Gestão |
| --- | --- | --- | --- | --- | --- |
| Criar contato/demanda | Sim | Sim | Não por padrão | Não por padrão | Com concessão |
| Consultar dados mínimos da demanda | Com concessão | Com concessão | Com concessão | Com concessão | Com concessão |
| Editar recepção e organizar cadastro/documentos | Etapas 1/4 | Não | Somente campos de conferência próprios | Não | Correção motivada autorizada |
| Registrar proposta/condições e formalizar | Não | Sim | Não | Não | Apenas com capacidade comercial explícita |
| Ler honorários/condições | Não por padrão | Com concessão financeira de leitura | Com concessão financeira de leitura | Não por padrão | Com concessão financeira de leitura |
| Conferir e liberar operação | Não | Não | Sim, com motivo/evidência | Não | Somente se também receber capacidade financeira |
| Conferir checklist | Etapa 4 | Itens comerciais próprios | Itens financeiros próprios | Itens da execução próprios | Revisão autorizada |
| Dispensar item documental | Não | Não | Não | Não | Ação específica, motivo e concessão documental |
| Encaminhar etapa principal | Responsável atual autorizado | Responsável atual autorizado | Responsável atual autorizado | Responsável atual autorizado | Reatribuição/correção motivada |
| Receber/devolver passagem | Apenas destino Secretaria | Apenas destino Comercial | Apenas destino Financeiro | Apenas destino Operacional | Não substitui o destinatário por padrão |
| Distribuir ao jurídico | Etapa 4 | Não | Não | Não | Com capacidade de distribuição |
| Executar tarefas jurídicas/confirmar prazo | Não por padrão | Não | Não | Com concessão da ação e do caso | Somente se também tiver capacidade operacional |
| Registrar pendência financeira/conferência final | Não | Não | Sim | Não | Com capacidade financeira |
| Encerrar juridicamente/suspender caso | Não | Não | Não | Responsável autorizado; encerramento exige zero obrigações abertas | Com capacidade operacional e concessão |
| Concluir demanda com pendência aceita | Não | Não | Solicita decisão | Não | Ação específica + motivo + concessões pertinentes |
| Consultar quadro/contagem/exportar | Só registros e campos permitidos | Idem | Idem | Idem | Idem; exportar exige ação separada |
| Conceder acesso de negócio | Não por padrão | Não por padrão | Não por padrão | Não por padrão | Grant delegado de gestão de acesso para aquele registro |

O administrador de acessos M1 continua administrando contas técnicas; não recebe capacidade de Gestão, de financeiro, de conceder acesso de negócio ou de leitura jurídica por implicação. Auditor M1 vê auditoria técnica; histórico de domínio e conteúdo exigem concessões próprias.

## Inicialização de negócio e primeiro registro

Precisão implementada M2-A: o Comercial pode corrigir dados iniciais da demanda que ele próprio criou, enquanto ainda responsável na recepção, com `view` e `edit_intake`. Não abre recepção de terceiros, nem solução/proposta antes do aceite. A primeira passagem explícita permanece exigida, inclusive para destinatário Comercial igual ao criador. Isso resolve a criação permitida ao Comercial sem deixá-lo incapaz de corrigir sua entrada.

Ações implementadas: ContactGrant `view`, `edit`, `view_history`; DemandGrant `view`, `edit_intake`, `manage_opportunity`, `view_history`, `send_handoff`, `receive_handoff`, `recover`, `manage_access`. `view` corresponde a `view_minimal` do desenho, sem dados financeiros. Demais ações continuam planejadas.

Recuperação: autoridade inicial ou Gestão com `recover` previamente concedido para a demanda; o setor Gestão não cria essa concessão. Autorizar a demanda antes de carregar candidatos, limitados às capacidades da etapa. Reassociação encerra passagens pendentes bloqueadas com motivo/histórico e exige novo encaminhamento explícito.

Delegado com leitura e `manage_access` usa “Gerenciar acessos desta demanda” no detalhe. Só concede/revoga ações que possui; nunca `manage_access` ou `recover`. Não administra setores ou cadastros por essa delegação.

Comando interativo único designa a autoridade inicial de acesso de negócio por indicação expressa da gestão, registrando usuário ativo, referência da autorização e operador executor. Não usar access_admin como atribuição departamental nem abrir conteúdo implicitamente. A autoridade inicial pode atribuir setores e delegar gestão de concessões por escopo/registro; consultar, executar e exportar continuam exigindo concessão própria. A definição das pessoas reais só ocorre por indicação autorizada, antes do piloto.

Ao criar uma demanda nova, quem tem capacidade de criação recebe apenas view_minimal, edit_intake, send_handoff e view_history sobre o novo registro, na mesma transação. Contato novo também tem concessão cadastral mínima ao criador. Isso não abre outro atendimento, contato restrito ou caso. A autoridade de negócio concede ao destinatário receive_handoff e as ações necessárias para aquela entrega antes do envio; sem destinatário habilitado, não criar passagem impossível de receber. Aceitar não concede leitura implicitamente.

## Concessões e filas

- DemandGrant: ações separadas view_minimal, edit_intake, manage_opportunity, view_contract, manage_contract, receive_handoff, send_handoff, financial_review, distribute, manage_document_checklist, waive_document, view_history e export. Ações finais de encerramento/pendência têm concessões específicas, sem herança geral de editar.
- CaseGrant existente preserva view/export. M2 acrescentará ações de execução, tarefas/prazos e fechamento sem converter view em permissão de escrita.
- Uma pessoa pode trabalhar em mais de um setor apenas por atribuições explícitas; isso não muda seus registros autorizados.
- A fila de recebimento só inclui pedidos para os quais o usuário tenha receive_handoff concedido. Sem view_minimal: exibir apenas referência opaca, setores e estado. Não revelar título/cliente/checklist/motivo.
- Aceitar um pedido não concede view automaticamente. Distribuir ao executor exige concessão prévia das ações necessárias pelo gestor de acesso de negócio autorizado para a demanda/caso.
- Cadastros e sugestões de duplicidade só retornam contatos autorizados; não revelar a existência de cadastro restrito. Reuso oculto exige revisão por pessoa que possua acesso aos dois registros.

## Revogação, desligamento e migração do M1

Revogar ação vale na requisição seguinte. Retirada planejada de setor/ação exige reassociação explícita prévia. Desativação e revogação de segurança não são bloqueadas por trabalho aberto: revogam acesso e transferem a responsabilidade atual afetada à fila institucional “Gestão — recuperar responsabilidade”, preservando datas, obrigações e atribuição anterior no histórico. Nenhum executor novo é escolhido automaticamente.

Gestores designados recebem somente as ações/concessões de recuperação necessárias; fila não concede conteúdo jurídico ou financeiro. Pedidos pendentes envolvendo executor revogado ficam bloqueados para novos comandos até reassociação. Se o gestor também perder acesso, a fila permanece pendente e outra autoridade de negócio pode designar substituto. Nunca restaurar acesso da conta revogada por falta de substituto. A administração M1 e mudanças de setor/ação devem chamar a mesma política, descrita na seção 9.2 do desenho. Revogar apenas sessão não transfere trabalho quando a conta ainda tem as ações necessárias.

Migração não criará capacidades departamentais a partir de operator/access_admin/auditor. Antes dos cenários de homologação, cadastrar atribuições e concessões mínimas para usuários fictícios de teste autorizados. Não carregar pacote Aurora nem importar usuários reais por inferência.
