from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes
from telegram import Update

BOT_TOKEN = "8158399936:AAGZaDsO9D-mQ-wXlOMnzR8X-us0xmNThEY"

async def on_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request
    await context.bot.send_message(
        chat_id=req.from_user.id,
        text=(
            "👋 Merci d’avoir rejoint le canal !\n"
            "✅ Pour bénéficier de mes services, il suffit de m’envoyer un message privé avec ce que vous souhaitez.\n"
            "📩 Je vous réponds rapidement et je validerai votre demande sous peu.\n"
            "👉 Contact direct : @lafameee"
        )
    )

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(on_join_request))
    app.run_polling()
