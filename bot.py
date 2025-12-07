import os
import telebot

# Получаем токен и ID админа из переменных окружения (безопасно!)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')

# Проверка: если токен не задан — выдаём ошибку
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден! Укажите его в переменных окружения на хостинге.")

if not ADMIN_CHAT_ID:
    raise ValueError("❌ ADMIN_CHAT_ID не задан! Укажите ваш Telegram ID.")

# Создаём бота
bot = telebot.TeleBot(BOT_TOKEN)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = (
        "👋 Привет! Я бот фотоуслуг в Бухте Тихая.\n\n"
        "✅ Реставрация старых фото\n"
        "✅ Оживление с ИИ\n"
        "✅ Коллажи и фото на документы\n\n"
        "📸 Просто пришлите фото — я приму заказ!"
    )
    bot.send_message(message.chat.id, text)

# Обработка фото
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user = message.from_user
    name = user.first_name or "Пользователь"
    username = f"@{user.username}" if user.username else "без @username"
    
    # Уведомление админу
    admin_msg = f"🆕 НОВЫЙ ЗАКАЗ!\nИмя: {name}\nКонтакт: {username}\nID чата: {message.chat.id}"
    bot.send_message(ADMIN_CHAT_ID, admin_msg)
    
    # Ответ клиенту
    client_msg = (
        "✅ Фото получено!\n"
        "Обрабатываю — результат через 20–40 минут.\n\n"
        "💰 Стоимость: от 100 ₽\n"
        "📲 Оплатите через СБП на номер: **+7 (XXX) XXX-XX-XX**\n"
        "После оплаты напишите сюда — сразу пришлю результат!"
    )
    bot.send_message(message.chat.id, client_msg, parse_mode="Markdown")

# Запуск (на хостинге это будет работать автоматически)
if __name__ == '__main__':
    bot.infinity_polling()
