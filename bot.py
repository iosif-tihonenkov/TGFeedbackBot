from handlers.user import start_user
from handlers.admin import start_admin
from config import ADMIN_CHAT_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id == ADMIN_CHAT_ID:
        return await start_admin(update, context)
    return await start_user(update, context)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))  # Только один обработчик
    app.run_polling()