from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

#Здесь задается токен бота
TOKEN = "7770486473:123"

#Тут у нас работает команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я бот. Как дела?' + update.message.text)  #объект update содержит всю информацию о входящем сообщении.
    #В данном случае мы видим следующее: await (не закрывать функцию, пока не выполнится участок кода) update(см.коомент выше).message(объект сообщения).reply_text("Привет! Я бот. Как дела") - ну тут понятно - вернуть текст в скобках

#Здесь работает возврат сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)


#Основной пул работы
def main():
    # Создаем Application
    application = Application.builder().token(TOKEN).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start)) #Тут у нас обработчик команды /start. Как вводить команду - указано в кавычках. 
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo)) #А этот обработчик на команду echo
    
    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()