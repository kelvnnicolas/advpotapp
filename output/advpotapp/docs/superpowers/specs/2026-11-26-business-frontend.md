# Business — primeiro checkpoint de implementação

Autorização: usuário pediu iniciar estrutura e implementação por checkpoints, frontend primeiro, backend/banco posteriormente. Modelo comercial confirmado: assinatura por escritório, colaboradores incluídos, sem trial. Preço, vagas, frequência e provedor ainda não definidos.

## Recorte entregue primeiro

Manter Django/HTML/HTMX, tokens atuais e JS local para interações de prévia. Alternativa SPA separada aumenta dependências/contratos sem necessidade neste checkpoint; não adotada. Não criar modelos/migrações, OAuth, serviço de cobrança ou entitlement real antes da validação do frontend e das decisões correspondentes. As rotas Django deste lote só entregam HTML; não são o backend de negócios Business.

Prévia local, apenas DEBUG=True. Área Business requer login ativo; contratação demonstrativa pode ser visitada sem login no ambiente local. Dados exclusivamente fictícios. Formulários interagem no navegador, sem gravação, convites, validação de pagamento ou criação de escritório. Recarregar reinicia alterações. Informar isso permanentemente, sem prometer recursos disponíveis.

Rotas GET/HEAD: /business/ (resumo), /business/equipe/, /business/fluxos/, /business/assinatura/, /business/integracoes/, /business/configuracoes/, /contratar/ e /contratar/retorno/. POST e outros métodos não são suportados. Produção retorna 404. Navegação conserva cenário permitido da assinatura: active, pending, expired, cancelled; qualquer outro é 404. A simulação não altera autorização M1/M2-A.

Interface: navegação Business própria; escritório fictício Horizonte identificado; voltar à operação local; estados de assinatura com ação contextual; equipe pesquisável e convite apenas preparado na tela; suspensão local de membro sem afetar usuários reais; configuração de nome/responsável do fluxo sem reordenar as seis etapas obrigatórias; configurações demonstrativas; conexão Google sempre desconectada; contratação com resumo e retorno pendente, nunca confirmação falsa de pagamento. Sem valor, frequência ou limite de vagas inventados.

Sem dados de formulário em query string, localStorage, sessionStorage ou cookies próprios. Não renderizar HTML de entradas do usuário; usar textContent/criação segura de elementos. O registro jurídico e seus dados não entram nesta prévia. Formulários sem JS informam necessidade de JS e não enviam dados ao servidor. Nenhum script, fonte, imagem ou SDK externo novo.

## Aceite deste checkpoint

Rotas nomeadas, links consistentes, login exigido na área Business, 404 em produção, 405 em mutações, entradas/cenários inválidos tratados, preview marcado em todas as telas. Em Chrome: navegar, pesquisar, preparar convite com duplicidade/validação, simular suspensão, alterar configuração do fluxo, revisar contratação sem cobrança, retorno sem liberação; sem escrita em User/grants/BusinessAuthority/Contact/Demand/Case/AuditEvent por ações da prévia. Responsivo em 390 px, teclado, labels e feedback de estado; nenhuma requisição de formulário ou serviço externo.

## Próximo checkpoint de domínio — ainda não implementado

Antes de backend/banco, validar contrato em docs/data/BUSINESS_DOMAIN_MODEL.md, estratégia de isolamento e regras comerciais pendentes. Serviços transacionais por escritório, participação/owner, fluxos versionados e entitlement devem anteceder cobrança real. Checkout e webhooks entram com provedor escolhido, sandbox e aceite próprios. Não publicar esta prévia como SaaS pronto.
