from urllib.parse import quote

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.error import Forbidden
from telegram.ext import (
    Application,
    CommandHandler,
    ChatJoinRequestHandler,
    ContextTypes,
    CallbackQueryHandler,
)

# --- CONFIG ---
BOT_TOKEN = "8158399936:AAGZaDsO9D-mQ-wXlOMnzR8X-us0xmNThEY"
OWNER_USERNAME = "lafameee"  # ton @ sans le @

WELCOME_TEXT = (
    "👋 Merci d’avoir rejoint le canal !\n\n"
    "Voici mes services disponibles 👇\n"
    "Clique sur la catégorie puis choisis le service qui t’intéresse.\n"
    "⚡ Je te répondrai rapidement et validerai ta demande.\n"
    "👉 Contact direct : @lafameee"
)

# --- DONNÉES ---
# id court -> (label affiché, {sous_service_label: message_DM})
CATEGORIES = {
    "docs": (
        "📄 Documents Officiels",
        {
            "Arrêt maladie": "Bonjour, je souhaite un document : arrêt maladie.",
            "Facture (EDF/Gaz/Internet)": "Bonjour, je souhaite une facture (EDF/Gaz/Internet).",
            "Avis d’imposition": "Bonjour, je souhaite un avis d’imposition.",
            "Taxes foncières": "Bonjour, je souhaite un document : taxes foncières.",
            "Certificat de scolarité": "Bonjour, je souhaite un certificat de scolarité.",
        },
    ),
    "id": (
        "🆔 Pièces d’identité Officielles",
        {
            "Passeport": "Bonjour, je souhaite une pièce d’identité : passeport.",
            "Carte nationale": "Bonjour, je souhaite une pièce d’identité : carte nationale.",
            "Permis de conduire": "Bonjour, je souhaite : permis de conduire.",
            "Carte Vitale": "Bonjour, je souhaite : carte vitale.",
        },
    ),
    "bank": (
        "🏦 Ouvertures de Comptes bancaires verifiés",
        {
            "Revolut": "Bonjour, je souhaite une ouverture de compte Revolut.",
            "Boursorama": "Bonjour, je souhaite une ouverture de compte Boursorama.",
            "Nickel": "Bonjour, je souhaite une ouverture de compte Nickel.",
            "Binance": "Bonjour, je souhaite une ouverture de compte Binance.",
            "Kraken": "Bonjour, je souhaite une ouverture de compte Kraken.",
        },
    ),
    "fx": (
        "💸 Échanges & Monnaies",
        {
            "Crypto ➜ Cash": "Bonjour, je souhaite un échange : crypto vers cash.",
            "Cash ➜ Virement": "Bonjour, je souhaite un échange : cash vers virement.",
            "Autres options d’échange": "Bonjour, je souhaite un autre type d’échange de monnaie.",
        },
    ),
    "contracts": (
        "📑 Contrats & Justificatifs",
        {
            "Contrat de travail": "Bonjour, je souhaite un contrat de travail.",
            "Contrat de bail": "Bonjour, je souhaite un contrat de bail.",
            "Fiche de paie": "Bonjour, je souhaite une fiche de paie.",
            "Déclaration de revenus": "Bonjour, je souhaite une déclaration de revenus.",
        },
    ),
    "online": (
        "💻 Compte Airbnb verfiés, Leboncoin etc..",
        {
            "Airbnb": "Bonjour, je souhaite ouvrir un compte Airbnb.",
            "Leboncoin": "Bonjour, je souhaite ouvrir un compte Leboncoin.",
            "Amazon": "Bonjour, je souhaite ouvrir un compte Amazon.",
            "Booking": "Bonjour, je souhaite ouvrir un compte Booking.",
            "Vinted / Cdiscount / Nike": "Bonjour, je souhaite ouvrir un compte (Vinted / Cdiscount / Nike).",
        },
    ),
    "other": (
        "🚗 Autres Services",
        {
            "Location de voiture": "Bonjour, je souhaite louer une voiture pas à mon nom.",
            "Mutuelle": "Bonjour, je souhaite une prestation liée à la mutuelle.",
            "Autre (précisez)": "Bonjour, j’ai une demande spécifique (autre).",
        },
    ),
    "custom": (
        "❓ Demande Spécifique",
        {
            "Décrire ma demande": "Bonjour, j’ai une demande spécifique : …",
        },
    ),
}

# --- HELPERS ---

def dm_url(text: str) -> str:
    # encode tout sauf les espaces (pour un rendu propre)
    encoded = quote(text, safe=" ")
    return f"https://t.me/{OWNER_USERNAME}?text={encoded}"

def kb_main() -> InlineKeyboardMarkup:
    rows = []
    for cat_id, (label, _) in CATEGORIES.items():
        rows.append([InlineKeyboardButton(label, callback_data=f"CAT|{cat_id}")])
    return InlineKeyboardMarkup(rows)

def kb_sub(cat_id: str) -> InlineKeyboardMarkup:
    label, services = CATEGORIES[cat_id]
    rows = []
    for sub_label, message in services.items():
        rows.append([InlineKeyboardButton(f"➡️ {sub_label}", url=dm_url(message))])
    # Bouton “Autre sur demande” présent dans CHAQUE sous-menu
    rows.append([InlineKeyboardButton("📝 Autre sur demande", url=dm_url("Bonjour, j’ai une demande qui n’est pas dans la liste."))])
    rows.append([InlineKeyboardButton("🔙 Retour", callback_data="BACK")])
    return InlineKeyboardMarkup(rows)

# --- HANDLERS ---

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT, reply_markup=kb_main())

async def on_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        req = update.chat_join_request
        await context.bot.send_message(
            chat_id=req.from_user.id,
            text=WELCOME_TEXT,
            reply_markup=kb_main(),
        )
    except Forbidden:
        # L’utilisateur n’accepte pas les MP — on ignore proprement
        pass

async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data or ""
    if data.startswith("CAT|"):
        _, cat_id = data.split("|", 1)
        if cat_id in CATEGORIES:
            label, _ = CATEGORIES[cat_id]
            await query.edit_message_text(
                text=f"{WELCOME_TEXT}\n\n**{label}** — choisis un service :",
                reply_markup=kb_sub(cat_id),
                parse_mode=None,  # pas besoin de Markdown ici
            )
    elif data == "BACK":
        await query.edit_message_text(
            text=WELCOME_TEXT,
            reply_markup=kb_main(),
        )

# --- APP ---

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(ChatJoinRequestHandler(on_join_request))
    app.add_handler(CallbackQueryHandler(on_button))

    app.run_polling()

