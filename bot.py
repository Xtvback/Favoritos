import os
import json
import logging
from datetime import datetime
from anthropic import Anthropic
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
YOUR_CHAT_ID = os.getenv("YOUR_CHAT_ID")

client = Anthropic(api_key=ANTHROPIC_API_KEY)
NOTES_FILE = "notas.json"
conversation_history = []


def is_authorized(update: Update) -> bool:
    if not YOUR_CHAT_ID:
        return True
    return str(update.effective_chat.id) == YOUR_CHAT_ID


def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.reply_text(
        "Olá! Sou o teu assistente pessoal.\n\n"
        "Envia qualquer mensagem e respondo com IA.\n\n"
        "Comandos:\n"
        "/anotar [texto] — Guarda uma nota\n"
        "/listar — Lista as tuas notas\n"
        "/apagar [número] — Apaga uma nota\n"
        "/limpar — Apaga o histórico da conversa\n"
        "/id — Mostra o teu Chat ID\n"
        "/ajuda — Mostra esta mensagem"
    )


async def cmd_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"O teu Chat ID é: `{update.effective_chat.id}`", parse_mode="Markdown")


async def cmd_anotar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    texto = " ".join(context.args)
    if not texto:
        await update.message.reply_text("Usa: /anotar [texto da nota]")
        return
    notes = load_notes()
    note = {
        "id": len(notes) + 1,
        "texto": texto,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    notes.append(note)
    save_notes(notes)
    await update.message.reply_text(f"Nota #{note['id']} guardada.")


async def cmd_listar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    notes = load_notes()
    if not notes:
        await update.message.reply_text("Ainda não tens notas.")
        return
    linhas = ["As tuas notas:\n"]
    for n in notes:
        linhas.append(f"*#{n['id']}* [{n['data']}]\n{n['texto']}")
    await update.message.reply_text("\n\n".join(linhas), parse_mode="Markdown")


async def cmd_apagar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Usa: /apagar [número da nota]")
        return
    num = int(context.args[0])
    notes = load_notes()
    nova_lista = [n for n in notes if n["id"] != num]
    if len(nova_lista) == len(notes):
        await update.message.reply_text(f"Nota #{num} não encontrada.")
        return
    save_notes(nova_lista)
    await update.message.reply_text(f"Nota #{num} apagada.")


async def cmd_limpar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    global conversation_history
    conversation_history = []
    await update.message.reply_text("Histórico da conversa apagado.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return

    global conversation_history
    user_text = update.message.text
    conversation_history.append({"role": "user", "content": user_text})

    # Mantém só as últimas 20 mensagens para não exceder limites
    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=(
            "És um assistente pessoal útil que responde sempre em português de Portugal. "
            "Ajuda com tarefas, perguntas, cálculos, textos, lembretes e o que for pedido. "
            "Sê direto e conciso."
        ),
        messages=conversation_history,
    )

    reply = response.content[0].text
    conversation_history.append({"role": "assistant", "content": reply})

    await update.message.reply_text(reply)


def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN não definido no ficheiro .env")
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY não definido no ficheiro .env")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("ajuda", cmd_start))
    app.add_handler(CommandHandler("id", cmd_id))
    app.add_handler(CommandHandler("anotar", cmd_anotar))
    app.add_handler(CommandHandler("listar", cmd_listar))
    app.add_handler(CommandHandler("apagar", cmd_apagar))
    app.add_handler(CommandHandler("limpar", cmd_limpar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot iniciado. Ctrl+C para parar.")
    app.run_polling()


if __name__ == "__main__":
    main()
