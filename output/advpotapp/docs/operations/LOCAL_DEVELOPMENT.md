# Executar e revisar a fundação M1

24/11/2026. Ambiente local de desenvolvimento; não é produção nem homologação da Delfino.

## Instalação

Pré-requisitos: Python 3.13 com patch suportado, Docker Desktop em execução, PowerShell. O runtime preparado nesta sessão está no workspace pai em .tools/python; o ambiente virtual já está em .venv. Instalação reproduzível: criar .venv com Python 3.13 e instalar requirements.txt; para jornada visual, requirements-dev.txt e Google Chrome instalado.

1. No diretório output/advpotapp, executar `.venv/Scripts/python.exe scripts/init_local.py`. Gera .env com segredos aleatórios, não imprime nem sobrescreve os valores.
2. Executar `powershell -ExecutionPolicy Bypass -File scripts/start.ps1`. Inicia apenas o banco local, aguarda saúde, aplica migrações e inicia Django em http://127.0.0.1:8765.
3. Em outro terminal, executar `. ./scripts/env.ps1` e `.venv/Scripts/python.exe src/manage.py bootstrap_access_admin`. O terminal pede nome e senha sem eco; não existe conta ou senha padrão. O primeiro administrador não é superusuário e não lê casos automaticamente.
4. Abrir /entrar/. Na administração é possível criar contas, mudar perfil, desativar/reativar e revogar sessões. Perfis M1 são técnicos provisórios (profissional, administrador de acessos, auditor); não equivalem à matriz departamental M2 aprovada.

O banco local fica no volume advpotapp-m1_advpot_m1_data, com porta 55432 publicada apenas em 127.0.0.1. Parar com `docker compose --project-name advpotapp-m1 --env-file .env -f deploy/compose.local.yml stop`. Não usar remoção de volumes como procedimento rotineiro.

## Verificação

### Inicialização e uso do M2-A

Após carregar `scripts/env.ps1`, aplicar `src/manage.py migrate` com o Python da .venv. A migração cria tabelas; não cria setores, autoridades, contatos ou demandas de demonstração.

No terminal interativo, executar `src/manage.py bootstrap_business_authority`. Informar administrador técnico executor, sua senha oculta, conta ativa indicada pela gestão e referência da autorização expressa. Executável uma vez; não substitui recuperação de conta privilegiada. A conta indicada passa a ver “Acessos de negócio”, sem leitura implícita dos registros.

Na tela de acessos de negócio, a autoridade atribui Secretaria/Comercial às contas indicadas. Contatos novos concedem ao criador leitura, edição e histórico do próprio cadastro. Demandas novas concedem leitura, edição de recepção, encaminhamento e histórico do próprio registro. Para destinatário Comercial, conceder separadamente `view`, `receive_handoff` e `manage_opportunity` na referência da demanda; `view_history` e acesso ao contato também são concessões separadas. O usuário de origem fornece a referência completa do registro à autoridade.

Em “Clientes e contatos”, reutilizar cadastro visível ou registrar novo. Em “Atendimentos”, abrir demanda e manter necessidade, origem e próximo passo. Encaminhar ao destinatário habilitado; a responsabilidade permanece na origem. O destinatário acessa “Passagens ao Comercial” e aceita ou devolve com motivo. Após aceitar, atualiza solução/proposta e avança sequencialmente. Lista e quadro compartilham os filtros e a página de até 20 registros.

Se uma revogação/desativação impedir a atuação do responsável, a demanda passa à fila “Recuperar responsabilidade”. A gestão indicada configura as concessões do novo responsável antes de reassociar. A reassociação encerra passagens pendentes bloqueadas com histórico; um novo encaminhamento explícito é necessário. Gestão só recupera com ação recover previamente concedida para a demanda; setor Gestão isolado não basta.

O recorte termina em “Preparar formalização”: sem contrato, caso ou efeito financeiro. [Evidências e limitações](../testing/M2A_VERIFICATION.md). Não inserir dados reais para experimentar este ambiente de revisão.

Executar `powershell -ExecutionPolicy Bypass -File scripts/test.ps1` para testes PostgreSQL, ausência de migrações pendentes e check Django. `-SQLite` permite o ciclo rápido, mas não verifica bloqueio de linha nem concorrência do PostgreSQL.

Para a jornada visual: carregar env.ps1, definir ADVPOT_BROWSER_TESTS=1 e executar `src/manage.py test tests --settings=config.test_postgres` com o Python da .venv. Os dados fictícios são criados no banco temporário test_advpot e removidos ao final. Não há carga Aurora nem usuário demonstrativo permanente. Capturas ficam em .stitch/previews. Não executar duas suítes PostgreSQL simultaneamente sobre o mesmo nome de banco de teste.

Contadores de login: cinco tentativas por identificador e vinte por IP em quinze minutos; resposta genérica sem informar se a conta existe. O endereço vem de REMOTE_ADDR, sem confiar em headers encaminhados. Em proxy compartilhado, revisar a política de IP antes de produção. Rotina `prune_login_buckets` remove contadores com mais de 24h. Não apaga o histórico de auditoria.

## Limites e recuperação

M1 contém um envelope mínimo de caso e concessões view/export para verificar a política no servidor; cadastro completo, concessão operacional de casos, tarefas, passagens e recuperação administrativa de senha são entregas posteriores. Não editar o banco de produção para substituir fluxos ausentes. Se perder o único acesso administrativo, interromper o uso e executar recuperação controlada com operador autorizado, após cópia e registro; esse procedimento ainda precisa ser implementado antes do piloto.

Exportação atual: POST no detalhe do caso, somente com view e export explícitos. JSON schema advpot.case-envelope.v1 inclui ID, título, responsável e data; não equivale à exportação integral futura de clientes, documentos, histórico ou migração.

O PostgreSQL no volume local não é backup externo. A política de frequência/retenção, RPO/RTO, cópia externa cifrada e ensaio de restauração permanece no marco de operação. Nada nesta entrega comprova recuperação de produção. Antes de dados reais: MFA privilegiado, recuperação de acesso auditada, matriz validada, revisão de segredos, TLS/proxy/static, usuário de banco restrito, backup/restauração, monitoramento e aceite no ambiente acordado.

## Logs e sessões

Log local de acesso registra rota e status sem query string. Senhas são marcadas como sensíveis; auditoria contém apenas autoria, ação e referência. Outros servidores/proxies também devem remover parâmetros de busca e conteúdo sensível; a configuração local não os protege automaticamente. Respostas privadas são no-store e o cache de histórico HTMX é desabilitado. Revogação vale na próxima requisição; não interrompe uma operação que já estava sendo executada.

Desativação, mudança de perfil e revogação incrementam a versão da sessão. Reativar não recupera sessão antiga. Não há envio de e-mail, SSO Google, cadastro público, Workspace ou integrações habilitadas.
