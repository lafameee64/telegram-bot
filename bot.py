from urllib.parse import quote

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import Forbidden
from telegram.ext import (
    Application, CommandHandler, ChatJoinRequestHandler, ContextTypes
)

BOT_TOKEN = "8158399936:AAGZaDsO9D-mQ-wXlOMnzR8X-us0xmNThEY"
OWNER_USERNAME = "lafameee"

SERVICES = {
    "🌐 Création de site":        "Bonjour, je souhaite un site web ✨",
    "📱 Développement App":       "Bonjour, je souhaite une application 📱",
    "🎨 Design Logo":             "Bonjour, je souhaite un logo/design 🎨",
    "📢 Marketing Réseaux":       "Bonjour, je souhaite un accompagnement marketing 📢",
    "✍️ Rédaction Contenu":       "Bonjour, je souhaite une rédaction de contenu ✍️",
    "🔎 SEO Référencement":       "Bonjour, je souhaite un service SEO 🔎",
    "🎬 Montage Vidéo":           "Bonjour, je souhaite un montage vidéo 🎬",
    "📊 Gestion Publicité":       "Bonjour, je souhaite une gestion de publicité 📊",
    "🤖 Automatisation Bot":      "Bonjour, je souhaite une automatisation via bot 🤖",
    "📈 Stratégie Business":      "Bonjour, je souhaite une stratégie business 📈",
}

def build_keyboard() -> InlineKeyboardMarkup:
    rows = []
    for label, msg in SERVICES.items():
        encoded = quote(msg, safe=" ")  # garde les espaces normaux
        url = f"https://t.me/{OWNER_USERNAME}?text={encoded}"
        rows.append([InlineKeyboardButton(label, url=url)])
    return InlineKeyboardMarkup(rows)

WELCOME_TEXT = (
    "👋 Merci d’avoir rejoint le canal !\n\n"
    "Voici mes services disponibles 👇\n"
    "Clique sur le service qui t’intéresse et **envoie-moi un message privé automatiquement** ✅"
)

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT, reply_markup=build_keyboard(), parse_mode="Markdown")

async def on_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        req = update.chat_join_request
        await context.bot.send_message(
            chat_id=req.from_user.id,
            text=WELCOME_TEXT,
            reply_markup=build_keyboard(),
            parse_mode="Markdown",
        )
    except Forbidden:
        pass

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(ChatJoinRequestHandler(on_join_request))
    app.run_polling()
