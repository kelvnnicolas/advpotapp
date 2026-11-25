# Operação em VPS — preparação

Plano de requisitos, ainda não executado. Nenhum servidor ou serviço foi contratado nesta entrega.

## Antes do provisionamento

Confirmar titularidade das contas, pagador, orçamento, domínio, localização/região, volume de banco/documentos, uso simultâneo, janela de manutenção, suporte e recuperação. Selecionar capacidade após medir piloto; oito usuários e 1.500 clientes não determinam sozinhos CPU, memória e disco.

Topologia inicial proposta: proxy HTTPS público; aplicação web e worker do mesmo projeto em rede privada com PostgreSQL; armazenamento persistente; backup fora da VPS. Só o proxy publica o acesso web; banco não publica porta na internet. Administração por acesso restrito e individual.

## Checklist de configuração

- Ambientes de teste e produção separados em dados, segredos e contas de integração.
- Segredos fora do código e da imagem; credenciais por ambiente, com revogação e recuperação definidas.
- HTTPS, cookies seguros, proteção CSRF, hosts/origens autorizados, debug desligado e erro sem dados sensíveis.
- Acesso por menor privilégio, proteção das contas privilegiadas e procedimento emergencial auditado.
- Logs sanitizados, rotação, retenção e acesso definidos; não registrar tokens, conteúdo jurídico ou documentos por padrão.
- Monitorar disponibilidade da aplicação, banco, espaço, falhas do worker, atraso da fila, validade da cópia e resultado da restauração.
- Documentar atualização, migração de banco, manutenção e retorno; backup compatível antes de alteração irreversível.

## Backup e recuperação

Definir com a cliente: frequência, retenção, proteção, conta/local externo, perda máxima aceitável de dados e tempo-alvo de recuperação. Um ponto de partida para discussão é cópia diária e ensaio mensal, mas isso não atende a qualquer exigência nem representa política contratada.

Cobrir banco, configurações necessárias e conteúdo documental no escopo aprovado. Referência de arquivo não restaura arquivo apagado do Drive. Definir procedimento independente para documentos, permissões e versões, sem presumir que sincronização equivale a backup.

Roteiro de ensaio: obter cópia externa → restaurar ambiente isolado → verificar versão/schema → conferir contagens e vínculos → conferir acesso a documentos → testar login e fluxo crítico → medir tempo e perda → registrar resultado e responsável. Não restaurar testes sobre produção.

## Incidente e retorno

Classificar impacto, informar responsável pelo canal acordado, preservar evidências sanitizadas e escolher recuperação. Se necessário, impedir novas escritas até reconciliar dados. Retorno de versão precisa considerar mudanças no banco; voltar só o código pode ser insuficiente.

Definir convivência temporária e canal de registro de urgências caso o ambiente fique indisponível. Não pressupor prazo garantido de solução, atendimento 24h ou alta disponibilidade em uma VPS única.

## Passagem para suporte

Entregar inventário de contas e responsáveis, versões, arquitetura publicada, evidência de recuperação, canais, cobertura, limites, escalonamento, rotina de manutenção e procedimento de exportação/saída. Somente após preencher esses itens a sustentação pode ter compromisso operacional concreto.
