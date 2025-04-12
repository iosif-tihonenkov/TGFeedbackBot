import logging
from telegram import Update, Message
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from config import BOT_TOKEN, ADMIN_CHAT_ID

# Настройка логгирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Словарь для хранения соответствий: {id сообщения в админ-чате: (id пользователя, id оригинального сообщения)}
message_store = {}

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка сообщений от пользователей и пересылка админам"""
    user = update.message.from_user
    forwarded_msg = await update.message.forward(ADMIN_CHAT_ID)
    
    # Сохраняем связь между пересланным сообщением и пользователем
    message_store[forwarded_msg.message_id] = (
        update.message.chat_id,
        update.message.message_id
    )
    
    await update.message.reply_text("Ваше сообщение отправлено администраторам. Ожидайте ответа!")

async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /reply админа для ответа пользователю"""
    if update.message.chat.id != ADMIN_CHAT_ID:
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text("Ответьте командой /reply на пересланное сообщение пользователя")
        return
    
    replied_msg_id = update.message.reply_to_message.message_id
    
    if replied_msg_id not in message_store:
        await update.message.reply_text("Не удалось найти исходное сообщение пользователя")
        return
    
    user_chat_id, original_msg_id = message_store[replied_msg_id]
    admin_reply = update.message.text.replace('/reply', '').strip()
    
    if not admin_reply:
        await update.message.reply_text("Добавьте текст ответа после /reply")
        return
    
    try:
        await context.bot.send_message(
            chat_id=user_chat_id,
            text=f"Ответ администратора:\n{admin_reply}",
            reply_to_message_id=original_msg_id
        )
        await update.message.reply_text("Ответ отправлен пользователю")
    except Exception as e:
        logging.error(f"Ошибка при отправке: {e}")
        await update.message.reply_text("Не удалось отправить ответ")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Обработчики
    application.add_handler(CommandHandler("reply", reply_to_user))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))
    
    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()