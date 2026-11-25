# Fontes, evidências e uso

Consolidação: 24/11/2026. O [manifesto](INPUT_MANIFEST.json) registra caminhos, tamanhos e hashes das fontes locais para rastreabilidade. Ele não prova validação operacional nem leitura integral de cada arquivo listado.

## Registro

| ID | Fonte | Grau e uso nesta estrutura |
| --- | --- | --- |
| U01 | Revisão do dossiê e confirmação prévia do usuário | Definição registrada: tasks.due_date é entrega/compromisso, não fatal |
| U02 | Resposta do usuário nesta conversa | Primeira versão exclusiva da Delfino |
| S01 | Documentos criados neste chat, incorporados em product/project/commercial | Posicionamento Workspace/VPS e propostas anteriores de produto/contratação |
| S02 | AGENTS.md, README.md e PROJECT_STATUS.md do dossiê pai | Limites, histórico, estágio e proibição de presumir carga/validação |
| S03 | docs/architecture, workflows, functional, ux e backlog do dossiê | Referência documental ADVBOX e limites das observações; não schema do Advpot |
| S04 | docs/testing/mapping-review.md, review-checklist.md, scenario-proposals.md e data-quality-report.md | Semântica confirmada e lacunas de mapeamento/cobertura |
| S05 | data/synthetic/advbox-synthetic-test-data: README, dicionário, cenários, prompt e dataset.json | Estrutura sintética e restrições; originais não modificados |
| S06 | data/synthetic/proposals/v1 e relatórios correspondentes | Cenários ainda propostos, não incorporados ou carregados |
| S07 | fluxogramaclientedelfino.jpeg | Fluxo de seis etapas lido visualmente; fotografado, sem versão formal declarada |
| S08 | proposta_delfino_gestao_local.pptx | Texto dos 12 slides: contexto histórico, perfis e hipótese local; sem validação de preço/prazo atual |
| S09 | Imagens demonstrativas do workspace anterior | Referências visuais com dados fictícios; não evidência de aplicação funcional |
| W01 | [Delfino Advogados](https://www.delfinoadv.com.br/) | Conteúdo público observado no navegador em 24/11: seis áreas, contexto institucional e canais |
| W02 | [Django — autenticação](https://docs.djangoproject.com/en/5.2/topics/auth/) | Documentação oficial consultada para fundamentar recomendação arquitetural; não fixa versão de implementação |
| W03 | [Calendar — criar eventos](https://developers.google.com/calendar/api/guides/create-events) | Referência oficial consultada; conta e integração não configuradas/testadas |
| W04 | [Drive — drives compartilhados](https://developers.google.com/drive/api/guides/about-shareddrives) | Referência oficial consultada; disponibilidade do plano e configuração da cliente pendentes |

As fontes locais S02–S08 permanecem no diretório pai da aplicação. S01 foi copiada como base de trabalho, sem substituir os originais. Nenhum arquivo do pacote sintético foi convertido em importador ou fixture executada.

## Rastreabilidade das decisões principais

| Decisão/requisito | Origem | Estado |
| --- | --- | --- |
| Exclusividade Delfino | U02 | Confirmado pelo usuário |
| VPS + Workspace | S01 | Posicionamento consolidado |
| Passagens entre setores | S07, apoio S08 | Fluxo observado no material; comportamento de aceite/devolução é proposta nova |
| Liberação financeira manual, sem quitação obrigatória | S07 + interpretação de produto | Proposta a validar |
| Área/natureza do caso | W01 + S07 | Catálogo inicial proposto, sem afirmar demanda por volume |
| Entrega separada de fatal | U01/S04 | Semântica de origem confirmada; implementação proposta |
| Monólito Django/HTMX/PostgreSQL | Recomendação técnica desta entrega | Não aprovado especificamente |
| Outbox, permissões por caso e controle de concorrência | Recomendação técnica desta entrega | Não observados nem copiados da ADVBOX |

## Limitações de acesso e verificação

A ferramenta de pesquisa web retornou erro de decodificação. A leitura pública foi obtida pelo navegador. O site Delfino apresentou inicialmente verificação do próprio site e depois carregou normalmente; não houve envio de formulário, login ou contorno de controle de acesso.

O dossiê já contém fontes e observações ADVBOX de etapas anteriores. Esta tarefa não repetiu testes de conta, não consultou registros de clientes e não promoveu hipóteses anteriores a fatos verificados. Preços, uso de Workspace, volume de casos e capacidade da infraestrutura não foram auditados.

Nenhum conteúdo bruto de sessão, cookie, token ou resposta autenticada foi incorporado à entrega. O manifesto identifica arquivos existentes; não é pacote de dados pessoais nem comprovação de ausência de todo dado sensível.
