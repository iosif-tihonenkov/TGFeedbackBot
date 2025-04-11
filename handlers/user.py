from telegram import Update
from telegram.ext import ContextTypes

async def start_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добрый день, пользователь")