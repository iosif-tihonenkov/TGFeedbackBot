from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_CHAT_ID

async def start_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id == ADMIN_CHAT_ID:  # Проверяем, что это админский чат
        await update.message.reply_text("Добрый день, администратор")