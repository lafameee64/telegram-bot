from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "TON_TOKEN_ICI"

SERVICES = {
    "🌐 Création de site": "Bonjour, je souhaite un site web.",
    "📱 Développement App": "Bonjour, je souhaite une application.",
    "🎨 Design Logo": "Bonjour, je souhaite un logo/design graphique.",
    "📢 Marketing Réseaux": "Bonjour, je souhaite un accompagnement marketing réseaux.",
    "✍️ Rédaction Contenu": "Bonjour, je souhaite une rédaction de contenu.",
    "🔎 SEO Référencement": "Bonjour, je souhaite un service SEO / référencement.",
    "🎬 Montage Vidéo": "Bonjour, je souhaite un montage vidéo.",
    "📊 Gestion Publicité": "Bonjour, je souhaite une gestion de publicité.",
    "🤖 Automatisation Bot": "Bonjour, je souhaite une automatisation via bot.",
    "📈 Stratégie Business": "Bonjour, je souhaite une stratégie business.",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for name, text in SERVICES.items():
        url = f"https://t.me/lafameee?text={text.replace(' ', '+')}"
        keyboard.append([InlineKeyboardButton(name, url=url)])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Merci d’avoir rejoint le canal !\n\n"
        "Voici mes services disponibles 👇\n"
        "Clique sur le service qui t’intéresse et envoie-moi un message privé automatiquement ✅",
        reply_markup=reply_markup
    )

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
