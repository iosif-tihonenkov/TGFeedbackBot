from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from handlers.user import start_user
from handlers.admin import start_admin
from config import BOT_TOKEN, ADMIN_CHAT_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id == ADMIN_CHAT_ID:
        return await start_admin(update, context)
    return await start_user(update, context)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()