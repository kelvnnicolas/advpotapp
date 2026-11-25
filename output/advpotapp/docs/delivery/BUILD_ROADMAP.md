# Roteiro de criação por entregas

Proposta de sequência e critérios. Não é autorização de construção, cronograma fechado ou estimativa de preço. O primeiro lote é interno à Delfino e não inclui todos os módulos apresentados nas referências.

## M0 — fechar o desenho do lote inicial

Entradas: desenho da aplicação, fluxo da cliente e questões prioritárias. Revisar arquitetura recomendada, acesso por caso, condições de liberação e exceções do fluxo. Definir usuários responsáveis por homologação e dados permitidos.

Saídas: desenho aprovado, matriz de acesso do lote, transições e checklists mínimos, recorte de cenários de teste. Revisões de schema ADVBOX só bloqueiam importação/integração com aquele destino, não o desenvolvimento independente com regras próprias aprovadas.

## M1 — fundação

Criar projeto Django e configuração por ambiente; fixar versões; PostgreSQL; sessões, papéis e política por registro; revogação; proteção de formulários; auditoria; configuração institucional; estrutura de testes e rotina de verificação.

Projetar a interface base e navegação em português. Implementar lista, formulário, paginação, filtros e estados de erro reutilizáveis. Nenhuma integração habilitada por padrão. Saída: login real e negação de acesso comprovada, sem dados reais e sem conta pública administrativa.

## M2 — primeira fatia operacional completa

Entregar nesta ordem:

1. Contato mínimo, busca e aviso de duplicidade.
2. Atendimento com área, responsável, etapa e próximo passo.
3. Registro de proposta/condições e contratação com referência documental.
4. Passagem ao financeiro e liberação manual auditada.
5. Conferência documental e distribuição ao jurídico.
6. Caso sem processo obrigatório, pessoas por papel e tarefa atribuída.
7. Entrega separada de prazo fatal, compromisso interno e histórico.
8. Meu trabalho e filas por setor, filtrados por autorização.

Testar o fluxo completo com devolução por pendência e concorrência de aceite. Saída: demonstração interna funcional, dados explicitamente fictícios e documentação curta de uso. Ainda há convivência com financeiro atual, Drive/agenda manuais e eventuais funções não substituídas.

## M3 — Workspace conectado

Confirmar plano, conta institucional, local de documentos, agenda e autorizações. Implementar adaptadores e outbox; Drive primeiro por vínculo e criação controlada de pasta; Calendar unidirecional para compromissos selecionados, sem convidados iniciais.

Testar indisponibilidade, permissão negada, token revogado, repetição, cancelamento e timeout após sucesso. Saída: evidência no ambiente autorizado, instruções de revogação e reconciliação de acessos. Uma tela de configuração sem teste não conclui esse marco.

## M4 — financeiro gerencial e encerramento

Entregar contratos/parcelas, recebimentos manuais, pendências e visão por cliente/caso; preservar correções. Projeção não entra em recebido. Validar valores e moeda. Não incluir conciliação, pagamento ou cobrança automatizada por inferência.

Saída: fluxo final do financeiro e relatórios conferidos por responsável autorizado. Caso encerrado pode conservar saldo aberto; encerramento jurídico e financeiro independentes. Se esse marco for adiado, não declarar substituição integral do uso financeiro atual.

## M5 — preparação de dados e piloto

Aprovar mapeamento e cenários antes de carga sintética. Depois validar amostra real autorizada e mecanismo de exportação. Produzir ensaio, rejeições, reconciliação, corte/retorno e treinamento por setor. Não tratar a fixture Aurora como amostra da base real.

Saída: piloto com responsáveis identificados, resultados de aceite, volume medido e pendências classificadas. Medir tempos de consulta, filas e adesão com linha de base, sem prometer ganho antes da medição.

## M6 — entrada em produção

Escolher/provisionar VPS apenas no escopo autorizado. Aplicar plano de operação, testes de recuperação, monitoramento, acessos, documentação e canais de suporte. Concluir a matriz de aceites e o plano de convivência/encerramento do sistema anterior.

Saída: autorização de produção registrada, restauração comprovada, responsável pelo ambiente e procedimento de suporte. Uma única VPS não significa alta disponibilidade.

## Backlog posterior

Automações de workflow; Gmail e templates com envio; assinatura eletrônica; IA opcional; relatórios avançados; portal do cliente; integrações judiciais; operações bancárias; SaaS para vários escritórios. Cada item exige definição, custo e aceite próprios.

## Modelo de tarefa para a execução futura

Registrar ID, problema/usuário, regra, escopo, dependência, arquivos esperados, aceite, verificação e evidência. A conclusão do desenvolvimento não substitui aceite de operação. Reestimar quando mudar regra, integração, migração ou responsabilidade de suporte; não reaproveitar prazos ou preços da apresentação antiga.
