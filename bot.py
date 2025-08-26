from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = "8158399936:AAGZaDsO9D-mQ-wXlOMnzR8X-us0xmNThEY"
ADMIN_ID = 1233060758  # Ton ID Telegram

# Quand quelqu’un rejoint le canal
async def on_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request

    # Boutons de services
    keyboard = [
        [InlineKeyboardButton("🌐 Création de site", callback_data="Création de site")],
        [InlineKeyboardButton("📱 Développement App", callback_data="Développement App")],
        [InlineKeyboardButton("🎨 Design Logo", callback_data="Design Logo")],
        [InlineKeyboardButton("📢 Marketing Réseaux", callback_data="Marketing Réseaux")],
        [InlineKeyboardButton("✍️ Rédaction Contenu", callback_data="Rédaction Contenu")],
        [InlineKeyboardButton("🔎 SEO Référencement", callback_data="SEO Référencement")],
        [InlineKeyboardButton("🎥 Montage Vidéo", callback_data="Montage Vidéo")],
        [InlineKeyboardButton("📊 Gestion Publicité", callback_data="Gestion Publicité")],
        [InlineKeyboardButton("🤖 Automatisation Bot", callback_data="Automatisation Bot")],
        [InlineKeyboardButton("📈 Stratégie Business", callback_data="Stratégie Business")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=req.from_user.id,
        text=(
            "👋 Merci d’avoir rejoint le canal !\n\n"
            "Voici mes services disponibles 👇\n"
            "Clique sur celui qui t'intéresse et je prendrai contact rapidement ✅"
        ),
        reply_markup=reply_markup
    )

# Quand un utilisateur clique sur un bouton
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Message pour l'utilisateur
    await query.edit_message_text(
        text=f"✅ Merci ! Tu as choisi : {query.data}\n"
             "Je vais transmettre ta demande à @lafameee 📩"
    )

    # Message pour toi (admin)
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📢 Nouvel utilisateur intéressé par : {query.data}\n"
             f"Utilisateur : @{query.from_user.username}"
    )

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(on_join_request))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
