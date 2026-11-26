# M2 — cenários de aceite propostos

25/11/2026. Especificação para testes futuros, não execução ou comprovação de funcionalidade. Base: [desenho M2](../superpowers/specs/2026-11-25-m2-workflow-design.md) e [evidência da imagem](../context/DELFINO_FLOW_EVIDENCE.md). Usar usuários/casos fictícios próprios, sem dados reais ou carga Aurora. Autorização de desenho não é aceite de ambiente operacional.

| ID | Cenário | Resultado exigido |
| --- | --- | --- |
| M2-01 | Secretaria registra contato mínimo e demanda | Responsável e próximo passo persistidos; origem/canais ausentes justificados; sem processo obrigatório |
| M2-02 | Busca identifica possível homônimo | Aviso somente sobre cadastro autorizado; usuário escolhe reusar ou manter pessoa distinta |
| M2-03 | Outro usuário busca demanda/caso restrito e lê contadores | Nenhum nome/título/valor/vínculo/total revela registro sem concessão |
| M2-04 | Comercial formaliza condições com referência e repete a operação | Uma contratação/revisão; mesmo contato, sem duplicações; nenhum caso iniciado/criado nesta etapa |
| M2-05 | Formalizar sem serviço, condições ou referência | Erro de validação; nenhuma passagem financeira ou caso criado parcialmente |
| M2-06 | Enviar ao financeiro | Pedido fica aguardando, origem continua responsável, fila autorizada recebe referência do mesmo item |
| M2-07 | Dois usuários financeiros aceitam a mesma versão | Um aceite e um conflito; apenas um responsável, um avanço e um evento de transição |
| M2-08 | Repetir comando com mesma chave e conteúdo; depois trocar conteúdo | Primeiro retorna resultado anterior; segundo gera conflito sem gravação |
| M2-09 | Destino devolve pendência antes do aceite | Motivo e pendência preservados; origem mantém etapa/responsabilidade; reenvio cria outro pedido |
| M2-10 | Financeiro libera contrato parcelado/gratuito com motivo e evidência | Operação liberada manualmente sem marcar quitação ou recebimento |
| M2-11 | Profissional sem ação financeira tenta liberar via POST direto | Negado; estado e histórico financeiro permanecem intactos |
| M2-12 | Alterar condições após liberação, antes da distribuição | Liberação antiga preservada; nova revisão precisa de nova conferência antes de seguir |
| M2-13 | Secretaria tenta distribuir com documento obrigatório pendente | Bloqueia; dispensa documental só por ação autorizada com motivo; contratação/liberação não dispensadas |
| M2-14 | Preparar caso na etapa 4 duas vezes e tentar distribuir para usuário inativo ou sem concessão operacional | Um caso preparado com responsável ativo; nenhuma execução iniciada; distribuição inválida falha sem transferência ou concessão automática |
| M2-15 | Operacional aceita distribuição válida | Demanda/caso/contratação mantêm vínculos; mesmo registro avança à execução e responsável ativo assume |
| M2-16 | Responsável jurídico registra entrega e prazo fatal diferentes | Datas persistem separadamente; prazo exige origem e confirmação profissional; nenhum cálculo automático |
| M2-17 | Documento ou providência faltante durante execução | Pendência interna com próximo passo; responsável atual permanece; sem mensagem externa ou suspensão automática |
| M2-18 | Nova pendência financeira durante execução | Ficha financeira registra/escalona; tarefa e prazo permanecem ativos; liberação histórica não é apagada |
| M2-19 | Concluir serviço com tarefa/prazo aberto, mesmo com justificativa ou responsável transferido | Bloqueia; obrigação exige estado terminal, sem conclusão implícita ou desaparecimento do prazo |
| M2-20 | Concluir serviço com tarefas/prazos concluídos ou cancelados validamente e pendência financeira informada | Caso pode encerrar; ficha financeira permanece aberta; cancelamento de prazo exige profissional, motivo e evidência; nenhum saldo calculado |
| M2-21 | Financeiro final registra conferência | Conclui apenas com situação documentada e decisão pertinente; pendência aceita exige gestão autorizada e motivo |
| M2-22 | Nova necessidade após demanda concluída | Nova demanda vinculada ao contato; não reabre silenciosamente registro anterior |
| M2-23 | Desativar responsável com trabalho aberto pela administração M1 | Revoga acesso sem aguardar substituto; transfere responsabilidade atual à fila institucional, preserva obrigações/datas/histórico e bloqueia novas ações em passagens afetadas até recuperação |
| M2-24 | Falha ao gravar histórico durante formalização/aceite/liberação | Rollback de todos os efeitos; tela não informa sucesso |
| M2-25 | Sessão expira em filtro parcial e usuário tenta Voltar após revogação | Login integral e nova autorização no servidor; nenhum conteúdo jurídico salvo em histórico HTMX |
| M2-26 | Regressão M1 | Login, throttle, CSRF, bootstrap, auditoria e exportação por concessão continuam funcionando |
| M2-27 | Inicializar acesso de negócio e tentar repetir ou usar apenas papel técnico | Só indicação autorizada e auditada cria primeira autoridade; repetição não cria outra raiz e access_admin não ganha leitura ou setor por implicação |
| M2-28 | Criador autorizado abre demanda e tenta encaminhar sem destinatário habilitado | Recebe apenas concessões iniciais documentadas; envio bloqueado até concessão do destinatário; nenhum contato restrito é aberto |
| M2-29 | Retirar setor/ação ou revogar acesso do executor e também indisponibilizar o gestor | Retirada planejada pede reassociação; revogação de segurança é imediata com fila pendente, sem reativar usuário ou expor conteúdo à administração técnica |
| M2-30 | Tentar retroceder etapa aceita, reabrir demanda finalizada ou corrigir contratação durante execução | Retrocesso/reabertura negados no primeiro M2; correção vinculada preserva etapa, obrigações e liberações históricas |

## Condição para homologação

Implementar e executar esses cenários no PostgreSQL, com evidências reais e revisão das permissões. Registrar também teclado/lista alternativa ao quadro, layout pequeno, preservação de formulário e mensagens de erro. Não criar testes que apenas comparem nomes das colunas com esta especificação: verificar persistência, invariantes, autoria e negações reais.

Responsável pelo aceite, data de homologação, resultado e ambiente: ainda não preenchidos. M2 só será disponível depois de aceite explícito e publicação no ambiente acordado. Financeiro gerencial, integrações, migração e requisitos de produção têm seus marcos próprios.
