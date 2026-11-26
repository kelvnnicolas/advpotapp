# Base fictícia local v1

26/11/2026. Carga explicitamente solicitada pelo usuário para testar a aplicação. Pacote próprio `advpot.local-demo.v1`; não deriva da base Aurora nem usa dados públicos/reais da Delfino.

## Conteúdo e uso

- 6 clientes/contatos sem CPF/CNPJ, telefone, e-mail ou endereço real.
- 8 demandas: 2 em triagem, 1 passagem pendente para a conta teste, 1 diagnóstico, 1 proposta, 1 preparação de formalização, 1 perdida e 1 cancelada. Data de referência fixa 26/11/2026; datas posteriores não avançam com o relógio.
- 3 casos de demonstração: envelopes mínimos M1, sem número judicial, documentos, tarefas, contrato ou financeiro. Não são criados pela formalização comercial.
- Títulos e cadastros identificados com `[FICTÍCIO]`; namespace e chaves determinísticas específicos de versão. Fonte em src/advpot/intake/data/local_demo_v1.json.

Com o ambiente local carregado, executar `src/manage.py seed_local_demo` com o Python da .venv. Exige conta `teste` ativa e Profissional, sem staff/superuser, DEBUG local e banco local. Não cria ou altera senha nem autoridade de negócio. Cria auxiliar `demo.recepcao` sem senha utilizável apenas para representar a origem de uma passagem pendente.

Atribui Secretaria e Comercial à conta teste para navegar nas ações demonstradas. Concede leitura/edição/histórico dos contatos e ações do fluxo somente nas demandas geradas. Nos três envelopes concede consulta/exportação. Não concede administração técnica, gestão de concessões ou recuperação. A carga é uma operação explícita de preparação de fixture pelo terminal, não uma concessão automática do produto ou fluxo disponível a usuários web.

Para testar: Clientes e contatos → Atendimentos (Lista/Quadro) → Passagens ao Comercial → Casos autorizados. Perdas/cancelamentos aparecem no filtro “Todas”. A passagem pendente exige aceite explícito para transferir responsabilidade. Nenhuma chamada externa, pasta Drive, evento Calendar, convite ou cobrança é criado.

## Reexecução e preparação real

Transação única: erro reverte toda a carga. Chaves de versão evitam duplicar a base ao repetir o comando. Demandas já criadas não têm etapa/conteúdo resetados; contatos respeitam a chave de criação; casos existentes não são sobrescritos. Os totais acima descrevem o pacote, não um relatório de todo o banco após testes manuais. Não há limpeza automática nem conversão desses cadastros em pessoas reais.

Esta é uma fixture local e não um importador genérico. Para migração futura, usar staging e mapeamento próprio de origem, preservando registros reais e mantendo o pacote fictício fora da carga de produção. [Preparação Workspace](../integrations/GOOGLE_WORKSPACE_READINESS.md).

## Verificação

Testes da carga cobrem repetição sem duplicidade, fluxo persistido, preservação do login, ausência de autoridade/administração implícita e bloqueio fora do desenvolvimento local. Suíte completa em PostgreSQL: 63 testes aprovados, incluindo três jornadas de navegador; check e migrações sem pendências. Carga local executada duas vezes: primeira criou 8 demandas; segunda criou zero. Sem exclusão ou reset do conteúdo existente.

Conferência adicional no servidor local com login real da conta teste: 6 contatos, 8 demandas no quadro com situação Todas, 3 casos autorizados e 1 formulário de passagem pendente. [Captura fictícia do quadro](../../.stitch/previews/demo-v1-atendimentos.png). A conferência não aceitou a passagem nem alterou as etapas demonstrativas.
