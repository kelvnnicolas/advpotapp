# M2 — revisão do desenho

25/11/2026. Entrega documental derivada do fluxograma da cliente. Não é resultado de testes de software M2.

## Fontes e escopo

- [Fotografia preservada e leitura](../context/DELFINO_FLOW_EVIDENCE.md): seis etapas, responsabilidades e entregas.
- [Desenho M2](../superpowers/specs/2026-11-25-m2-workflow-design.md): regras adicionais explicitamente propostas.
- [Matriz de acesso](../product/M2_ACCESS_MATRIX.md) e [30 cenários de aceite](M2_ACCEPTANCE.md).

## Revisão independente

Um agente revisor leu o desenho como implementador e apontou quatro lacunas relevantes. As respostas abaixo são propostas de construção do agente principal, não respostas atribuídas à cliente.

| Lacuna | Decisão registrada no desenho | Cobertura proposta |
| --- | --- | --- |
| Primeiro acesso de negócio/criador | Inicialização interativa de autoridade de negócio por indicação expressa; criador recebe somente ações documentadas sobre o registro novo; destinatário precisa de concessões antes do envio | M2-27 e M2-28 |
| Obrigações abertas no encerramento | Exigir estados terminais em tarefas/prazos; mera justificativa ou transferência não basta; cancelamento de prazo exige profissional, motivo e evidência | M2-19 e M2-20 |
| Responsabilidade após revogação | Retirada planejada pede reassociação; revogação de segurança não espera substituto e encaminha responsabilidade à fila institucional restrita, sem apagar obrigações ou reativar conta | M2-23 e M2-29 |
| Retrocesso após aceite | Excluído do primeiro M2; correções vinculadas preservam etapa, prazo e liberação; nova necessidade cria demanda vinculada | M2-22 e M2-30 |

Também foi ajustado o momento de criar caso: etapa 4, com responsável jurídico indicado, antes da passagem ao Operacional; não na formalização comercial. Isso conserva a exigência M1 de Case.responsible e permite concessão explícita de acesso antes do aceite. M2-04 e M2-14 distinguem esses comportamentos.

## Verificações documentais executadas

Conferidos dez documentos novos/alterados: nenhum link relativo ausente. A lista contém trinta IDs de cenário, todos únicos. SHA-256 da cópia da foto igual ao original: 138c8bf45f5c51b477c01ce6a7cdeed003cc1850189ddbdc1335dbc58e8fbd00.

Alterações desta etapa limitam-se a documentação e à cópia da imagem. Não houve alteração de código, migração, carga ou testes funcionais M2. Os resultados anteriores do M1 não comprovam funcionamento deste desenho. Não foi reexecutada suíte de aplicação para alterações exclusivamente documentais.

## Revisão necessária antes da construção

Aprovar ou corrigir o desenho e a matriz, principalmente as quatro decisões acima. Não se pede novo levantamento para redescobrir a sequência já fornecida pela cliente. Após aprovação, elaborar plano de implementação e executar M2-A → M2-B → M2-C → M2-D. Pessoas reais, homologador e checklist por área dependem de indicação antes da homologação. Não há preço/prazo contratados nem disponibilidade operacional nesta entrega.
