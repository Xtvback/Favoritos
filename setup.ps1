# Setup Claude Code + Telegram no Windows
# Corre como Administrador: clica direito > "Executar como administrador"

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Host "`n>> $msg" -ForegroundColor Cyan }
function Write-OK($msg)   { Write-Host "   OK: $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "   AVISO: $msg" -ForegroundColor Yellow }

Write-Host @"

  ╔══════════════════════════════════════════╗
  ║   Claude Code + Telegram  (Windows)     ║
  ╚══════════════════════════════════════════╝

"@ -ForegroundColor Magenta

# ── 1. Node.js ───────────────────────────────────────────────────────────────
Write-Step "A verificar Node.js..."
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Warn "Node.js nao encontrado. A instalar via winget..."
    winget install OpenJS.NodeJS.LTS --silent --accept-package-agreements --accept-source-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
        Write-Host "  Fecha e reabre este terminal como Administrador e volta a correr o script." -ForegroundColor Red
        exit 1
    }
}
Write-OK "Node.js $(node --version)"

# ── 2. Claude Code CLI ────────────────────────────────────────────────────────
Write-Step "A instalar Claude Code CLI..."
npm install -g @anthropic-ai/claude-code | Out-Null
Write-OK "Claude Code instalado"

# ── 3. Bun ───────────────────────────────────────────────────────────────────
Write-Step "A instalar Bun (necessario para os plugins)..."
if (-not (Get-Command bun -ErrorAction SilentlyContinue)) {
    powershell -Command "irm bun.sh/install.ps1 | iex"
    $env:Path = "$env:USERPROFILE\.bun\bin;" + $env:Path
    [System.Environment]::SetEnvironmentVariable("Path", "$env:USERPROFILE\.bun\bin;" + [System.Environment]::GetEnvironmentVariable("Path","User"), "User")
}
Write-OK "Bun $(bun --version)"

# ── 4. Login Anthropic ────────────────────────────────────────────────────────
Write-Step "Login na conta Anthropic..."
Write-Host "   Vai abrir o browser para fazeres login. Volta aqui depois." -ForegroundColor Yellow
Read-Host "   Pressiona ENTER para abrir o browser"
claude login
Write-OK "Login concluido"

# ── 5. Plugin Telegram ────────────────────────────────────────────────────────
Write-Step "A instalar plugin Telegram..."
claude -p "run the command /plugin install telegram@claude-plugins-official and then /reload-plugins" 2>$null
Write-OK "Plugin instalado"

# ── 6. Token do bot ───────────────────────────────────────────────────────────
Write-Host @"

  ──────────────────────────────────────────
   PASSO MANUAL: Cria o teu bot no Telegram
  ──────────────────────────────────────────
  1. Abre o Telegram no iPhone
  2. Procura @BotFather
  3. Envia /newbot
  4. Escolhe um nome (ex: "O meu assistente")
  5. Escolhe um username (ex: meuassistente_bot)
  6. Copia o TOKEN que ele te envia

"@ -ForegroundColor Yellow

$token = Read-Host "   Cola aqui o token do BotFather"
$token = $token.Trim()

if ($token -eq "") {
    Write-Host "  Token em branco. Podes configurar mais tarde com: claude /telegram:configure <token>" -ForegroundColor Red
    exit 1
}

# Guarda o token
$channelDir = "$env:USERPROFILE\.claude\channels\telegram"
New-Item -ItemType Directory -Force -Path $channelDir | Out-Null
"TELEGRAM_BOT_TOKEN=$token" | Out-File -FilePath "$channelDir\.env" -Encoding utf8
Write-OK "Token guardado"

# ── 7. Cria o atalho de arranque ─────────────────────────────────────────────
Write-Step "A criar atalho de arranque..."

$batPath = "$env:USERPROFILE\Desktop\Iniciar Bot Claude.bat"
@"
@echo off
title Claude Code + Telegram
echo.
echo  A iniciar Claude Code com canal Telegram...
echo  Podes fechar esta janela para PARAR o bot.
echo.
claude --channels plugin:telegram@claude-plugins-official
pause
"@ | Out-File -FilePath $batPath -Encoding ascii

Write-OK "Atalho criado no Ambiente de Trabalho: 'Iniciar Bot Claude.bat'"

# ── Concluido ─────────────────────────────────────────────────────────────────
Write-Host @"

  ╔══════════════════════════════════════════╗
  ║            INSTALACAO CONCLUIDA!        ║
  ╚══════════════════════════════════════════╝

  COMO USAR:
  1. Clica duas vezes em "Iniciar Bot Claude.bat" no Desktop
  2. No iPhone, abre o Telegram e fala com o teu bot
  3. Na primeira mensagem, o bot envia um codigo de emparelhamento
  4. No terminal que abriu, aparece o codigo -- confirma-o

  DEPOIS DE EMPARELHADO:
  Envia qualquer mensagem ao bot no Telegram e o Claude
  executa no teu computador Windows.

"@ -ForegroundColor Green
