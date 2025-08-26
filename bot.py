from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = "8158399936:AAGZaDsO9D-mQ-wXlOMnzR8X-us0xmNThEY"
ADMIN_ID = 1233060758  # Ton ID Telegram

# Liste de services avec message adapté
services = {
    "site_web": ("🌐 Création de site", "Bonjour, je suis intéressé par la création d’un site web."),
    "app_mobile": ("📱 Développement App", "Bonjour, je suis intéressé par le développement d’une application mobile."),
    "design": ("🎨 Design Logo", "Bonjour, je souhaite un logo / design graphique."),
    "marketing": ("📢 Marketing Réseaux", "Bonjour, je souhaite un accompagnement marketing réseaux."),
    "redaction": ("✍️ Rédaction Contenu", "Bonjour, j’ai besoin de rédaction de contenu."),
    "seo": ("🔎 SEO Référencement", "Bonjour, je souhaite améliorer mon référencement SEO."),
    "video": ("🎥 Montage Vidéo", "Bonjour, je cherche un service de montage vidéo."),
    "publicite": ("📊 Gestion Publicité", "Bonjour, je souhaite de l’aide pour gérer mes publicités."),
    "bots": ("🤖 Automatisation Bot", "Bonjour, je souhaite mettre en place un bot / automatisation."),
    "business": ("📈 Stratégie Business", "Bonjour, je souhaite des conseils en stratégie business.")
}

# Quand quelqu’un rejoint
async def on_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request

    # Générer les boutons avec callback
    keyboard = [
        [InlineKeyboardButton(label, callback_data=key)]
        for key, (label, _) in services.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=req.from_user.id,
        text="👋 Merci d’avoir rejoint le canal !\n\nSélectionne le service qui t’intéresse 👇",
        reply_markup=reply_markup
    )

# Quand l’utilisateur clique
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    service_key = query.data
    label, message = services[service_key]

    # Message de confirmation pour l’utilisateur
    await query.edit_message_text(
        text=f"✅ Merci ! Tu as choisi : {label}\n\n"
             f"👉 Clique ici pour m’envoyer directement un message :\n"
             f"https://t.me/lafameee?text={message.replace(' ', '%20')}"
    )

    # Notification pour toi (admin)
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📢 Nouvel utilisateur : @{query.from_user.username}\n"
             f"Service choisi : {label}"
    )

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(on_join_request))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
