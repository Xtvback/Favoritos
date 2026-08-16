# Favoritos

Site pessoal de favoritos do utilizador (Xtvback), publicado via GitHub Pages a partir da branch `main`. Ficheiros HTML autónomos (sem build step) — cada `.html` é uma mini-app independente.

## Convenções gerais

- **Nunca adivinhar URLs.** Antes de adicionar qualquer link/entrada nova (em `links.html`, `extras.html`, `chatgpt-extras.html` ou noutro ficheiro), confirma o URL oficial por pesquisa. Nunca inventes ou assumas um endereço.
- **Evitar duplicados.** Lê o ficheiro alvo na branch `main` antes de adicionar — é a única fonte de verdade sobre o que já lá está. Não repitas o mesmo produto/ferramenta mesmo com nome ligeiramente diferente.
- **Qualidade > quantidade.** Se não encontrares nada genuinamente novo, bom e relevante, não adiciones nada nessa sessão/dia. Não encher secções com entradas fracas, obscuras ou redundantes só para "cumprir a rotina".
- **Assinalar riscos e avisos de ToS.** Sempre que uma ferramenta/serviço a adicionar envolver algo que mereça um aviso — contornar limites de uma conta paga, agregar contas/camadas gratuitas de vários fornecedores, reselling de acesso a APIs, dados pessoais, práticas que possam violar os termos de serviço de terceiros, etc. — inclui esse aviso diretamente na descrição da entrada (não só numa mensagem de chat que se perde). Usa um ⚠️ no início da frase de aviso e mantém-na curta e honesta. Isto aplica-se tanto a adições manuais como às rotinas diárias automáticas.
- **Fluxo de publicação:** branch nova a partir de `main` → commit → push → PR → merge → confirmar que o workflow "Deploy GitHub Pages" corre com sucesso. Não é necessário pedir confirmação antes de mesclar — o utilizador já autorizou este fluxo autónomo.

## Estrutura relevante

- `links.html` — página principal de links, organizada em secções (`.section-block` com `data-section`) e navegável por "pills" no topo (`#catNav`). Cada link é uma `.row` com `.row-icon`, `.row-title`, `.row-desc` opcional.
- `extras.html` — "Claude Extras", centro de descoberta com array `CATALOG` no `<script>` (tipos: `skill`, `mcp`, `plugin`).
- `chatgpt-extras.html` — "ChatGPT Extras", mesmo motor que o `extras.html` mas com tipos `gpt`, `app`, `action`.

Ao adicionar uma entrada nova a um `CATALOG`, segue exatamente o formato dos objetos já existentes (`id`, `emoji`, `name`, `type`, `cat`, `desc`, `tags`, `use`, `install`, `steps`).
