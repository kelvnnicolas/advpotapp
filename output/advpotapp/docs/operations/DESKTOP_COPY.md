# Cópia de continuidade no Desktop

26/11/2026. Destino autorizado: `C:/Users/Kelvin Oliveira/Desktop/projetos/advpot`. O aplicativo nesse destino fica diretamente em `advpotapp`; o repositório de execução em Documents/ChatGPT mantém `output/advpotapp`.

A pasta Desktop conserva o dossiê original da investigação, a fotografia, a apresentação e os dados Aurora originais. As fontes atuais do aplicativo, documentação, requisitos, scripts, testes, migrações e capturas são atualizadas sem excluir arquivos antigos. Versões substituídas têm cópia em backups/progresso-2026-11-26-<revisão>/previous-files. Links Markdown relativos que usavam output/advpotapp são adaptados à disposição do Desktop; os hashes de origem e destino ficam no manifesto.

Na raiz do Desktop, README.md e PROJECT_STATUS.md ganham uma seção atual sem apagar o histórico. README_PRODUTO.md e AGENTS_PRODUTO.md preservam o conteúdo atual do repositório de produto. PROGRESS_SAVE_MANIFEST.json registra revisão, arquivos, hashes e diretório dos artefatos locais.

## Histórico e ambiente

O bundle advpot-history.bundle guarda o histórico Git de todos os branches/refs locais. Pode ser verificado por `git bundle verify` e clonado em um diretório novo, selecionando codex/business-frontend para retomar esse checkpoint. A cópia adaptada no Desktop não recebe uma pasta .git montada sobre o dossiê; use o repositório original ou clone o bundle para continuar commits com histórico exato.

Não são copiados .env, .venv, runtimes .tools, logs, cookies ou tokens. Dependências estão fixadas nos arquivos de requisitos. Não há senha padrão nova ou conexão Google copiada.

O servidor e o PostgreSQL existentes permanecem no ambiente original, com a mesma URL local. Para iniciar uma instalação independente pelo Desktop, preparar ambiente virtual/configuração próprios e decidir porta/projeto Compose antes de executar start.ps1: o script atual usa projeto advpotapp-m1 e porta 55432, já utilizados pelo ambiente original. Não remover o volume atual ou presumir que um .env recém-gerado altere a senha de um banco já inicializado.

## Dados locais sanitizados

O artefato advpot-local-sanitized.json é uma fixture Django com registros atuais de 17 modelos: usuários/perfis, referências de configuração, contatos, demandas, casos, concessões e histórico. Na cópia preparada em 26/11/2026 foram preservados 216 registros, incluindo 2 usuários, 6 contatos, 8 demandas e 3 casos. Cada senha foi substituída por marcador não utilizável; sessões e contadores transitórios de login foram excluídos. O banco em execução não foi alterado.

Restauração de verificação executada em banco PostgreSQL temporário separado: todas as contagens coincidiram, zero sessões e zero senhas utilizáveis. Esse banco de verificação foi removido. O manifesto database-manifest.json acompanha os detalhes. Isso valida o snapshot sanitizado, não substitui a política de backup externo/restauração de produção.

Uma recuperação futura exige banco novo/vazio com migrações aplicadas, importação autorizada da fixture e redefinição de acesso por terminal. Não carregar a fixture no banco atual: ela contém IDs e referências que podem colidir. Não usar como importador real, carga Aurora ou confirmação de prontidão SaaS.
