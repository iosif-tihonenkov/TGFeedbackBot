from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

# Состояния для ConversationHandler
WAITING_FOR_APPEAL = 1

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["Обращение", "Целеуказание"],
            ["Разбан", "Сообщить о проблеме"]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def handle_appeal_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Пожалуйста, опишите ваше обращение:",
        reply_markup=ReplyKeyboardRemove()
    )
    return WAITING_FOR_APPEAL

async def forward_appeal_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    appeal_text = update.message.text
    
    admin_message = (
        "📨 Новое обращение:\n\n"
        f"📝 Текст: {appeal_text}\n"
        f"👤 Отправитель:\n"
        f"   Имя: {user.full_name}\n"
        f"   Юзернейм: @{user.username if user.username else 'нет'}\n"
        f"   ID: {user.id}"
    )
    
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=admin_message
    )
    
    await update.message.reply_text(
        "Ваше обращение отправлено администраторам. Спасибо!",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END