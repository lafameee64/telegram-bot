from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = "8158399936:AAGZaDsO9D-mQ-wXlOMnzR8X-us0xmNThEY"

# Quand quelqu’un rejoint le canal
async def on_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request

    # Liste des services
    services = [
        ("🌐 Création de site", "Je souhaite un site web."),
        ("📱 Développement App", "Je souhaite une application mobile."),
        ("🎨 Design Logo", "Je souhaite un logo/design."),
        ("📢 Marketing Réseaux", "Je souhaite du marketing réseaux."),
        ("✍️ Rédaction Contenu", "Je souhaite de la rédaction."),
        ("🔎 SEO Référencement", "Je souhaite du référencement SEO."),
        ("🎥 Montage Vidéo", "Je souhaite du montage vidéo."),
        ("📊 Gestion Publicité", "Je souhaite une gestion publicité."),
        ("🤖 Automatisation Bot", "Je souhaite un bot/automation."),
        ("📈 Stratégie Business", "Je souhaite une stratégie business.")
    ]

    # Générer les boutons avec URL vers @lafameee + message pré-rempli
    keyboard = [
        [InlineKeyboardButton(
            text=label,
            url=f"https://t.me/lafameee?text=Bonjour%2C%20je%20suis%20intéressé%20par%20le%20service%20: %20{message.replace(' ', '%20')}"
        )]
        for label, message in services
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=req.from_user.id,
        text=(
            "👋 Merci d’avoir rejoint le canal !\n\n"
            "Voici mes services disponibles 👇\n"
            "Clique sur le service qui t’intéresse et envoie-moi un message privé automatiquement ✅"
        ),
        reply_markup=reply_markup
    )

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(on_join_request))
    app.run_polling()
