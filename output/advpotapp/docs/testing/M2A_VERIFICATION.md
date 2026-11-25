# M2-A — verificação técnica local

25/11/2026. Construção aprovada pelo usuário. Estágio: em desenvolvimento com verificação local; sem homologação da Delfino ou disponibilidade operacional.

## Entrega

Problema: perda de contexto ou responsabilidade entre recepção e Comercial. Usuários: Secretaria, Comercial e autoridade de negócio indicada. Fluxo: contato → demanda vinculada → concessões ao destinatário → envio → aceite → solução/proposta → preparar formalização. Uma única demanda atravessa o fluxo.

Regras: setor e ação por registro são complementares; administrador técnico não ganha negócio/leitura. Duplicidade somente sugere contatos visíveis; homônimos podem permanecer separados mediante confirmação. Histórico possui concessão separada. Criação e comandos da demanda possuem chave de repetição; alterações exigem versão atual. Responsável de origem permanece até o aceite. Devolução/cancelamento exige motivo. Revogação/desativação recupera responsabilidade inviável em fila institucional sem reativar conta ou conceder conteúdo à gestão.

## Verificação executada

- Testes iniciais de núcleo e workflow; testes de interface observados falhando antes das rotas e aprovados após implementação.
- Suíte PostgreSQL com `ADVPOT_BROWSER_TESTS=1`: **60 testes aprovados, zero ignorados**. Inclui regressões M1, dois aceites simultâneos, permissões, CSRF, idempotência, revogação e três testes de navegador.
- `makemigrations --check --dry-run`: nenhuma mudança pendente. `manage.py check`: sem problemas identificados.
- Chrome real: cadastro/demanda persistidos; Secretaria permanece responsável até aceite; Comercial avança até preparar formalização. Sem Case criado; demanda autorizada não revelou nome do contato sem concessão cadastral.
- Inspeção visual em 1440 px e 390 px, sem rolagem horizontal ou erros JavaScript.

Capturas fictícias: [pipeline](../../.stitch/previews/m2a-pipeline.png), [atendimento](../../.stitch/previews/m2a-atendimento.png) e [celular](../../.stitch/previews/m2a-mobile.png). São evidências locais, sem publicação de novas telas no Stitch. Referências históricas M1 preservadas.

## Limites, dependências e aceite

Mesma stack aprovada no M1, sem dependências novas. Migrações incrementais intake 0001–0003 preservam Case/CaseGrant. Autoridade inicial configurada por terminal interativo com autenticação do executor técnico e referência da indicação expressa. Sem conta/senha padrão.

Migrações 0001–0003 aplicadas ao banco local de desenvolvimento após a suíte final. Servidor reiniciado em 127.0.0.1:8765; página de login respondeu HTTP 200. Não foi criada autoridade de negócio nem conta demonstrativa permanente por inferência.

Contratação/versionamento, honorários, liberação financeira, demais passagens, checklists/documentos, execução, tarefas, prazos fatais e financeiro final pertencem aos próximos lotes. “Preparar formalização” não gera contrato/caso. Exportação de contato/demanda ainda ausente; exportação M1 permanece restrita ao envelope de caso. Recuperação de responsabilidade não recupera senha nem substitui a autoridade inicial.

Dados fictícios somente no banco temporário de testes descartado; sem carga real/Aurora, comunicação, Workspace, tribunal, dinheiro ou VPS. Antes do piloto: recuperação privilegiada, MFA, backups/restauração, matriz com usuários indicados e aceite no ambiente destinado ao uso. Os 30 cenários do desenho M2 completo não são declarados aprovados por esta suíte do recorte A.

Revisão independente do commit f028bf3 identificou seis achados relevantes. Todos reproduzidos com testes falhando antes da correção e aprovados depois: autorização anterior ao formulário de recuperação; candidatos elegíveis por etapa; campos comerciais exclusivos após aceite; ausência de concessão automática à Gestão; correção de entrada própria pelo Comercial; encerramento de passagem bloqueada na recuperação; interface de delegação por demanda. A suíte completa posterior passou com 60 testes. Uma pendência menor foi adiada: o seletor de etapas ainda oferece combinações que o servidor rejeita, como formalização direta em diagnóstico; o estado inválido não é persistido. Recuperação privilegiada da autoridade singleton foi mantida fora deste lote e segue requisito pré-piloto.
