from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
from handlers.user import (
    start,
    handle_button,
    get_main_keyboard,
    handle_appeal_start,
    forward_appeal_to_admin,
    WAITING_FOR_APPEAL
)
from handlers.admin import start_admin
from config import BOT_TOKEN, ADMIN_CHAT_ID

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Обработчик команды /start
    app.add_handler(CommandHandler("start", start))
    
    # ConversationHandler для обработки обращений
    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^(Обращение)$"), handle_appeal_start)
        ],
        states={
            WAITING_FOR_APPEAL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, forward_appeal_to_admin)
            ]
        },
        fallbacks=[]
    )
    app.add_handler(conv_handler)
    
    # Обработчик остальных кнопок
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button))
    
    app.run_polling()

if __name__ == "__main__":
    main()