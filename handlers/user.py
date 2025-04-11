from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes

# Клавиатура для кнопок (вынесена отдельно для reuse)
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["Обращение", "Целеуказание"],
            ["Разбан", "Сообщить о проблеме"]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

async def start_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text="Добрый день, пользователь! Выберите действие:",
        reply_markup=get_main_keyboard()
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    responses = {
        "Обращение": "Опишите ваше обращение в следующем сообщении...",
        "Целеуказание": "Укажите цель и местоположение...",
        "Разбан": "Запрос на разбан отправлен администраторам",
        "Сообщить о проблеме": "Опишите проблему подробнее..."
    }
    
    if text in responses:
        await update.message.reply_text(responses[text], reply_markup=get_main_keyboard())
    else:
        await update.message.reply_text("Пожалуйста, используйте кнопки меню", reply_markup=get_main_keyboard())