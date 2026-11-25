# Organização prevista da implementação

Estrutura proposta para quando a construção for autorizada. As pastas de código abaixo ainda não foram criadas; esta entrega contém somente documentação.

```text
advpotapp/
  AGENTS.md
  README.md
  PROJECT_STATUS.md
  docs/                         contexto, produto, arquitetura e aceites
  src/
    manage.py
    config/                     configuração e URLs por ambiente
    advpot/
      identity/                 usuário, papéis e concessões
      contacts/                 pessoas, organizações e canais
      intake/                   triagem e oportunidade comercial
      engagements/              contratação e referência documental
      cases/                    casos, partes e processos
      work/                     tarefas, prazos e compromissos
      handoffs/                 filas, checklist e aceite/devolução
      finance/                  liberação; gerencial em marco próprio
      documents/                referências e requisitos documentais
      integrations/             outbox e adaptadores Google
      audit/                    eventos de auditoria
      reporting/                consultas e definições de indicadores
    templates/                  layout, componentes e páginas
    static/                     CSS, ícones e JavaScript pontual
  tests/                        testes de integração e jornadas
  deploy/                       configuração de contêineres e publicação
  scripts/                      verificações e operações documentadas
```

Nomes e granularidade são escolhas propostas; não criar módulos vazios indiscriminadamente. Começar pelos necessários ao lote M1/M2. Adiar gerencial financeiro e adaptadores reais até o marco correspondente.

Em cada domínio, separar modelos persistidos, comandos de negócio, consultas autorizadas, formulários, páginas e testes conforme a complexidade. Transições relevantes ficam em comandos transacionais, não duplicadas em views, administração e jobs.

## Contratos de interface propostos

| Rota lógica própria | Finalidade | Controle |
| --- | --- | --- |
| /entrar | Sessão interna | Sem cadastro público; erro sem enumerar contas |
| /meu-trabalho | Tarefas e filas do usuário | Consulta autorizada |
| /atendimentos | Lista/quadro e triagem | Filtro por papel e responsabilidade |
| /atendimentos/{id} | Próximo passo, proposta e contratação | Leitura/ação separadas |
| /clientes/{id} | Dados e relações do contato | Escopo do registro e dados restritos |
| /casos/{id} | Contexto, pessoas e execução | Concessão ao caso |
| /passagens/{id}/aceitar | Aceite de demanda | Comando mutável, versão e autorização |
| /passagens/{id}/devolver | Retorno com pendência | Comando mutável e motivo |
| /casos/{id}/liberacao | Decisão financeira operacional | Permissão específica e auditoria |
| /agenda | Compromissos internos | Integração externa opt-in |
| /gestao | Indicadores operacionais | Conceito, período e filtro explícitos |

Essas são rotas de projeto, não endpoints observados na ADVBOX. Mutações usam método apropriado com CSRF e autorização; nenhuma ação de salvar, liberar ou excluir por GET. Uma API pública não integra o escopo inicial. Formalizar respostas, erros e idempotência dos comandos quando implementados.

## Preparação da execução

Antes de criar o código, registrar revisão do desenho e lote autorizado. Depois confirmar ferramentas/versões, iniciar repositório de aplicação isolado se acordado e preservar o dossiê pai. Não iniciar repositório ou copiar todo o diretório pai automaticamente: ele inclui arquivos alheios ao produto.

Nunca copiar credenciais, ZIPs, downloads incompletos, proposta histórica ou dados sintéticos para imagens de produção. Configuração real e conteúdo documental ficam fora do repositório. Arquivos de exemplo devem conter somente nomes de variáveis e valores fictícios, nunca chaves reais.
