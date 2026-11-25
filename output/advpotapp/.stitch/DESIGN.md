---
name: Advpotapp M1 — implementação local
colors:
  primary: '#123e34'
  accent: '#d3edaa'
  background: '#f6f7f3'
  surface: '#ffffff'
  text: '#172e2a'
  muted: '#61706c'
  border: '#dce2dc'
  error: '#9d302d'
  focus: '#886127'
---

# Design System: Advpotapp M1

## 1. Visual Theme & Atmosphere

Extraído de src/static/app.css e templates Django. Interface de trabalho discreta, com navegação ancorada, superfície clara e informação de acesso explícita. Poucos elementos e estados vazios reais evitam simular uma operação já implantada.

Este documento descreve a implementação local. O projeto Stitch preserva o sistema anterior Ateliê Jurídico (assets/d4b4d8b972a448b1a9cee4c47c1de2f4), com seus tokens editoriais próprios, nas referências históricas. Após revisão da geração, as três telas M1 foram substituídas por HTML e screenshots reais do Django com os tokens deste documento. Não houve substituição global do sistema anterior.

## 2. Color Palette & Roles

Verde profundo #123e34 ancora a barra lateral e ações primárias. Lima suave #d3edaa identifica navegação atual e ação sobre superfície escura. Fundo #f6f7f3 e superfícies #ffffff mantêm separação por borda #dce2dc, sem sombras decorativas. Texto #172e2a e secundário #61706c; erro #9d302d sempre acompanhado de mensagem. Foco #886127 com contorno de 3px.

## 3. Typography Rules

Arial/Helvetica/sans-serif do sistema, sem fontes remotas. Corpo 15px com linha 1.5. Título principal 32px/1.2, peso 600, tracking -1px; no celular 27px. Seções 21px, cartões 17px, rótulos 12px. Metadados compactos de 9–11px na apresentação desktop exigem validação com usuários. Referências usam Consolas/monospace.

## 4. Component Stylings

Botões de pelo menos 44px, raio 6px, foco visível. Painéis com borda de 1px e raio 10px. Navegação atual com aria-current. Campos com label visível; erros próximos ao campo e resumo. Estado vazio informa como obter acesso, sem criar botões simulados. Tabelas com cabeçalhos semânticos e rolagem própria. Busca funciona sem JavaScript e recebe atualização parcial via HTMX local.

## 5. Layout Principles

Barra lateral 236px e área flexível. Conteúdo máximo 1500px, margens 38px; acima de 1500px margens 56px. Breakpoints 1050px e 720px. No celular, navegação vira faixa superior e painéis empilham. Tela de acesso usa duas colunas, simplificadas abaixo de 720px. Base de espaçamento 8px com ajustes tipográficos. Sem fotografias ou ativos externos.

## 6. Design System Notes for Stitch Generation

Na geração de alternativas históricas, usar o sistema Ateliê Jurídico existente sem repetir tokens nos prompts. Para M1, os arquivos exportados e os tokens acima são a referência fiel. Priorizar estados de revisão e navegação condizente com cada perfil. Não acrescentar módulos, métricas, garantias de segurança ou integração Google como capacidades disponíveis. Somente dados fictícios em protótipos. As sugestões da geração original ficam em feedback.json como histórico, não como escopo aprovado.
