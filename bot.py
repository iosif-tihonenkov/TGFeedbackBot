from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN
from handlers.user import start_user
from handlers.admin import start_admin

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем команды
    app.add_handler(CommandHandler("start", start_user))  # Для пользователей
    app.add_handler(CommandHandler("start", start_admin))  # Для админов (проверка внутри функции)

    app.run_polling()

if __name__ == "__main__":
    main()