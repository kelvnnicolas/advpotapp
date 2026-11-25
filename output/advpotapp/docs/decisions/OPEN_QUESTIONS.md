# Decisões para revisão

24/11/2026. Campos em aberto não significam aceite. Esta lista organiza as próximas etapas; não exige todas as respostas antes de revisar o desenho.

## Já estabelecido

Aplicação inicial exclusiva da Delfino, confirmada pelo usuário. VPS e Workspace são diretrizes do posicionamento. U01 estabelece entrega/compromisso da tarefa como conceito distinto de prazo fatal. Não perguntar novamente essas decisões.

Em 25/11/2026, o usuário reiterou o fluxograma da cliente como fonte para M2. Secretaria/recepção → Comercial → Financeiro inicial → Secretaria/organização → Operacional → Financeiro final é a sequência de referência. Não pedir outro levantamento genérico do fluxo. Os detalhes que a imagem não define agora possuem propostas concretas no [desenho M2](../superpowers/specs/2026-11-25-m2-workflow-design.md).

## Revisão concreta do M2

Revisar o desenho e a matriz em conjunto, especialmente: manter origem responsável até aceite; uma passagem principal pendente; liberação manual vinculada à versão contratual sem quitação integral; pendência posterior sem suspensão automática; caso preparado na organização e execução iniciada no aceite; acesso por registro separado de setor; pendência financeira aceita para fechamento apenas por ação de gestão. A proposta não cria atalho urgente implícito. Estes pontos não são respostas já fornecidas pela cliente.

Nomes dos homologadores e checklists específicos por área serão necessários antes de homologação. Não bloqueiam a elaboração do desenho já solicitado, e não serão preenchidos com nomes reais por inferência.

## Antes de construir o primeiro lote

Atualização de 24/11/2026: stack e início do M1 foram autorizados pelo usuário. Os perfis técnicos da fundação não substituem a validação da matriz operacional. As decisões de passagem, liberação, concorrência por setor e metadados continuam bloqueando seus respectivos fluxos M2, não a construção já autorizada do M1.

| Decisão | Recomendação apresentada | Quem valida e por quê |
| --- | --- | --- |
| Stack e abordagem | Monólito Django + HTML/HTMX + PostgreSQL, autorizado para M1 | Implementação registrada em ADR-008; revisão se mudar o escopo |
| Passagens e exceções | Aceite/devolução explícitos por setor; liberação manual | Responsável operacional da Delfino; afeta estados e fluxo |
| Liberação urgente/gratuita/parcelada | Motivo e autor; sem exigir quitação integral | Gestão e financeiro; evita bloquear atendimento indevidamente |
| Matriz de acesso e casos restritos | Perfis por setor + concessão por caso | Gestão; afeta consultas e segurança do lote |
| Escopo da primeira homologação | Fluxo interno completo com ferramentas atuais em convivência | Responsável do projeto e validador da cliente |
| Concorrência entre setores | Uma passagem operacional principal; acompanhamento financeiro paralelo | Operação; define unicidade de passagem e responsabilidade |
| Metadados de caso restrito nas filas | Referência opaca e mínimo necessário; conteúdo exige concessão | Gestão e responsáveis de setor; evita exposição indireta |
| Pendência financeira após liberação | Registro/escalonamento, sem suspensão automática de tarefas/prazos | Financeiro e jurídico; define efeitos e autorização de suspensão |

## Antes de Workspace e financeiro

Conta/plano Workspace, propriedade de pastas, agenda de destino, escopos, revogação e acesso documental; condições de contratação, parcelas, recebimento parcial, descontos/correções e moeda; campos/checklists por área; necessidade de envio de convites. Não inferir conta a partir do domínio do site.

## Antes de migração e produção

Inventário real; exportação oficial disponível; volume e conteúdo dos arquivos; permissão para amostra/carga; aceite do novo mapeamento; procedimento de corte/retorno; titularidade de infraestrutura; custos; horários de suporte; retenção; política de backup e recuperação; critérios de produção; condições de uso/código/saída.

## Escolhas deixadas à execução técnica

Dentro da arquitetura aprovada, a equipe escolhe organização de funções, nomes internos, índices justificados, biblioteca CSS/ícones acessível e ferramentas de teste mantidas. Registrar dependências e decisões relevantes. Esses detalhes não exigem nova rodada de perguntas salvo se alterarem escopo, custo ou operação.

## Limites que não bloqueiam o desenho próprio

Catálogos, enums e rotas internas ADVBOX não resolvidos continuam no dossiê; só bloqueiam atividades que dependam deles. Não adivinhar esses contratos e não travar todo o Advpot à espera de evidência que ele não utiliza.
