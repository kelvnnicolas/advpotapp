# Evidências técnicas — fundação M1

24/11/2026 · America/Sao_Paulo. Verificação local; responsável operacional/homologador ainda não definido. Estado: em desenvolvimento com revisão técnica, sem aceite de uso.

## Problema, usuário e escopo

Preparar a base interna da Delfino para que cada pessoa entre com conta individual, consulte somente registros concedidos e tenha ações administrativas rastreáveis. Fluxo verificado: login → Meu trabalho → lista/detalhe mínimo de caso → exportação autorizada; administrador → criar/alterar/desativar conta → revogar sessão; auditor → consultar eventos.

Regras: negar por padrão, separar perfil de concessão por caso/ação, preservar histórico, evitar enumeração de contas, mutações com CSRF, dependência do banco interno sem Google. Não há triagem, contratação, tarefas, prazos, envio ou financeiro implementado.

## Execução e resultado

Ambiente: Python 3.13.18, Django 5.2.19, psycopg 3.3.9, PostgreSQL 17.12 em Docker local. Chrome headless via Playwright 1.65.2. O banco de testes é temporário; nenhuma carga de cliente ou pacote Aurora.

Comando de suíte: carregar scripts/env.ps1, definir ADVPOT_BROWSER_TESTS=1 e executar com .venv/Scripts/python.exe: `src/manage.py test tests --settings=config.test_postgres --verbosity 1`.

Resultado final observado: **28 testes, todos aprovados**, incluindo dois cenários de navegador, serialização de bootstrap em PostgreSQL, segurança de sessão e autorização. `makemigrations --check --dry-run`: nenhuma mudança pendente. `manage.py check`: nenhum problema. Migrações aplicadas no banco local, incluindo identidade, auditoria, casos e sessões. Isso não é validação de produção.

| Aceite técnico do recorte | Evidência |
| --- | --- |
| Sem sessão não consulta páginas internas | tests/test_identity.py |
| Login, mutações e logout respeitam CSRF/método | tests/test_identity.py, test_administration.py, test_access.py |
| Retorno externo de login ignorado | tests/test_identity.py |
| Limite por conta coerente com espaços e por IP sem alocação ilimitada | tests/test_identity.py |
| Desativar/reativar ou trocar perfil não revive sessão anterior | tests/test_administration.py |
| Admin, responsável e auditor não recebem leitura implícita | tests/test_access.py |
| Busca, total, detalhe e exportação não revelam caso alheio | tests/test_access.py |
| Criação com colisão de username preserva validação e transação | tests/test_administration.py |
| Bootstrap único sob duas execuções, sem entrada de senha redirecionada | tests/test_bootstrap.py |
| Acesso real, criação de conta, navegação, logout e celular sem overflow | tests/test_browser.py |
| Filtro parcial atualiza total e não grava conteúdo em sessionStorage | tests/test_browser.py |
| Sessão expirada em fragmento redireciona a página inteira | tests/test_identity.py |
| Log de acesso não registra texto da busca | tests/test_logging.py |

## Revisão independente e regressões

Revisão estática independente identificou riscos de snapshots HTMX, normalização e alocação do limitador de login e bootstrap concorrente. Os testes reproduziram as falhas antes das correções. Reativar temporariamente o histórico padrão do HTMX fez o teste detectar conteúdo fictício em sessionStorage; a proteção foi restaurada em finally. O teste de bootstrap criou dois administradores antes da correção e passou a aceitar apenas um depois dela.

Outros itens foram tratados como necessários à correção funcional: contagem do filtro, retorno ao login em fragmento, senha sem terminal, colisão de nome de usuário e remoção de query string do log local. Não houve segunda rodada de revisão independente após as correções; a suíte ampliada verificou os ajustes.

## Capturas e prototipagem

Capturas da aplicação estão em .stitch/previews: login, Meu trabalho, casos vazios, usuários e celular. Somente usuários fictícios do banco temporário aparecem. A primeira geração nativa no Stitch acrescentou descrições e garantias indevidas; a revisão visual a substituiu por HTML e screenshots reais do Django para login, Meu trabalho e usuários. HTML com CSS inline, sem scripts ou CSRF, e submit desabilitado no protótipo. IDs/URLs atualizados em .stitch/metadata.json; arquivos finais em .stitch/designs. As duas referências anteriores e o sistema Ateliê Jurídico foram preservados, e as três telas M1 agrupadas no canvas.

Após acrescentar a captura estática, os dois cenários de navegador foram executados novamente e aprovados. A suíte funcional completa de 28 testes já havia passado após a última alteração de código de produto. A extração não contém dados reais ou credenciais. O check de implantação executado com configuração local apresenta os cinco avisos esperados de DEBUG e HTTPS/cookies; não foi considerado aprovação de produção.

## Limites e aceite pendente

Nenhum aceite do escritório foi coletado. Não declarar M1 disponível para operação ou substituição do sistema atual. Concessão operacional/cadastro completo de casos, recuperação de senha, MFA privilegiado, perfis por setor, revisão de proxy/logs, TLS, backup externo/restauração e monitoração permanecem antes do piloto/produção. Exportação cobre somente o envelope M1. Sessões em andamento não são interrompidas retroativamente pela revogação.

Integrações não foram testadas porque não foram implementadas nem configuradas. Não houve teste de carga, auditoria de segurança exaustiva, migração, publicação ou ensaio de recuperação. O guia local registra como executar e os limites do ambiente.
