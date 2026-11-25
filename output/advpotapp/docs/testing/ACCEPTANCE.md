# Matriz de aceites proposta

Status inicial de todos os cenários: **não executado**. Critérios do novo produto; não resultados de teste ADVBOX. Definir dados de cenário antes de executar; não carregar o pacote original automaticamente.

| ID | Cenário | Resultado exigido | Marco |
| --- | --- | --- | --- |
| A01 | Usuário sem sessão abre detalhe direto | Acesso negado sem expor dados | M1 |
| A02 | Usuário tenta caso restrito por busca, URL, contador e exportação | Nenhuma informação fora do escopo | M1/M2 |
| A03 | Administração técnica cotidiana consulta caso sem concessão | Acesso negado; acesso emergencial tem fluxo explícito e trilha | M1 |
| A04 | Usuário desativado tem sessão ativa e tarefas antigas | Sessão revogada, histórico preservado, novas atribuições impedidas | M1 |
| A05 | Atendimento é convertido duas vezes por repetição de comando | Um contato/caso conforme regra; sem duplicação | M2 |
| A06 | Dois atendentes aceitam a mesma passagem simultaneamente | Um aceite vence; outro recebe conflito recuperável | M2 |
| A07 | Setor devolve demanda incompleta | Motivo e checklist visíveis; responsável e fila rastreáveis | M2 |
| A08 | Jurídico tenta liberar financeiramente o caso sem permissão | Servidor rejeita, mesmo por chamada direta | M2 |
| A09 | Financeiro libera caso com parcelas futuras | Liberação manual com motivo; nada marcado pago automaticamente | M2/M4 |
| A10 | Consultoria sem número/tribunal e tarefa interna | Funcionam sem processo judicial artificial | M2 |
| A11 | Tarefa tem entrega no dia e depois fica com data anterior | Hoje não aparece atrasada; anterior aberta aparece; concluída/cancelada não | M2 |
| A12 | Data de entrega da tarefa é alterada | Prazo fatal não muda; histórico conserva alteração | M2 |
| A13 | Prazo fatal é criado/alterado | Origem, responsável e confirmação obrigatórios; sem cálculo automático | M2 |
| A14 | Tarefa concluída é reaberta | Estado correto e histórico preservado | M2 |
| A15 | Quadro usado só por teclado e tela pequena | Etapa muda por comando acessível; feedback e foco preservados | M2 |
| A16 | Cadastro/formulário recebe erro de validação | Entrada preservada, erro junto ao campo e sem falso sucesso | M2 |
| A17 | Documento sem conteúdo no pacote é exibido | Indicação de metadado/arquivo ausente; nenhum download fictício | M2 |
| A18 | Google falha ou credencial é revogada | Registro interno salvo; falha visível, novas tentativas limitadas | M3 |
| A19 | Timeout ocorre após pasta/evento criado no Google | Repetição reconcilia objeto; não cria duplicado | M3 |
| A20 | Operador muda/cancela compromisso publicado | Objeto externo correto reconciliado; sem convidar/enviar por padrão | M3 |
| A21 | Usuário tem acesso Advpot, mas não ao arquivo Drive | Não contorna permissão externa nem cria link público | M3 |
| A22 | Financeiro lança previsão, recebimento parcial e correção | Totais distinguem cada conceito, com Decimal e trilha | M4 |
| A23 | Caso é encerrado com parcela em aberto | Pendência financeira preservada; encerramentos separados | M4 |
| A24 | Importação piloto é repetida | Mapeamento por fonte/versão evita duplicação; erros rastreáveis | M5 |
| A25 | Dados migram com arquivos e relações | Contagens, amostra e inventário documental reconciliados | M5 |
| A26 | Ambiente é restaurado de cópia externa | Dados, configurações e dependências recuperáveis; tempos medidos | M6 |
| A27 | Aplicação e adaptadores executam testes locais | Nenhum envio real, cobrança, convite ou comunicação externa | Todos |
| A28 | Contador do painel é aberto como lista | Mesmo filtro, conceito e autorização produzem o total | M2/M4 |
| A29 | Financeiro acompanha recebimentos durante a execução jurídica | Trilha financeira não rouba a responsabilidade operacional; regra validada de uma passagem por trilha | M2/M4 |
| A30 | Nova pendência financeira surge depois da liberação | Não bloqueia tarefas/prazos automaticamente; registra e encaminha para decisão autorizada | M2/M4 |
| A31 | Passagem de caso restrito aparece em fila autorizada somente ao recebimento | Metadados mínimos aprovados; nenhum nome/título/conteúdo sensível sem concessão | M2 |

## Evidência por aceite

Registrar versão do código, ambiente, cenário/dados, relógio/fuso, resultado esperado/obtido, falhas e responsável. Um teste automatizado valida comportamento; homologação da cliente valida aderência. Nenhum dos dois deve ser afirmado sem execução.

## Camadas de verificação

Regra de domínio: datas, estados, liberação e valores. Integração local: transações, autorização e concorrência em PostgreSQL. Navegador: fluxo completo, teclado e mensagens. Adaptadores: simuladores de falha e testes controlados no ambiente Google autorizado. Operação: restauração e procedimento de retorno.

Utilizar fixtures derivadas revisadas. Não exigir que os testes aceitem documentos inválidos como válidos, inventem anexos ou calculem produtividade a partir de eventos ausentes.
