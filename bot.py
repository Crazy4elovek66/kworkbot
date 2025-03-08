import requests
from bs4 import BeautifulSoup
import telebot
import time
import threading
from telebot import types

# Токен твоего бота
API_TOKEN = '8081177731:AAHi6xBekqBeOxsxweLd7P-075UobWS38j8'
bot = telebot.TeleBot(API_TOKEN)

# ID чата, куда бот будет отправлять уведомления
CHAT_ID = '437225657'

# URL категории "Графический дизайн" на Kwork
KWORK_URL = "https://kwork.ru/projects?c=41"

# 🔥 Ключевые слова, которые должны быть в заказе (ТОЛЬКО такие заказы отправляем)
KEYWORDS = [
    "логотип", "баннер", "оформление YouTube", "оформление Twitch",
    "аватарка", "превью", "иконки", "фирменный стиль", "дизайн визитки",
    "дизайн буклета", "дизайн флаера", "дизайн упаковки",
    "инфографика", "иллюстрация", "постер", "стикеры",
    "дизайн презентации", "веб-дизайн", "оформление постов", "креативный дизайн",
    "листовка", "флаер", "дизайн листовки", "дизайн флаера", "рекламная листовка", 
    "рекламный флаер", "брендовая листовка", "брендовый флаер", "листовка для мероприятия", 
    "флаер для мероприятия", "промо-листовка", "промо-флаер", "визитка", "дизайн визитки", 
    "визитная карточка", "брендовая визитка", "корпоративная визитка", "персональная визитка", 
    "визитка для компании", "визитка для бизнеса", "креативная визитка", "премиум визитка", 
    "эксклюзивная визитка"
]

# 🚫 Стоп-слова (если есть в заказе — игнорируем)
STOPWORDS = [
    "презентация", "отредактировать", "изменить текст",
    "чертеж", "архитектура", "3D", "моделирование", "интерьер", "экстерьер"
]

# Храним последний найденный заказ
last_order = None

def get_kwork_orders():
    """Функция парсит сайт Kwork и возвращает только подходящие заказы."""
    global last_order
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(KWORK_URL, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        orders = soup.find_all("div", class_="card__content")  # Ищем заказы

        results = []
        for order in orders:
            title = order.find("a", class_="wants-card__header-title").text.strip()
            link = "https://kwork.ru" + order.find("a")["href"]
            price = order.find("div", class_="wants-card__price").text.strip()

            # Фильтрация по ключевым словам
            if any(word.lower() in title.lower() for word in KEYWORDS):
                # Проверяем, что в заказе НЕТ стоп-слов
                if not any(stopword.lower() in title.lower() for stopword in STOPWORDS):
                    result = f"📌 {title}\n💰 {price}\n🔗 {link}"
                    results.append(result)
                    last_order = result  # Сохраняем последний найденный заказ

        return results
    else:
        return ["❌ Ошибка парсинга Kwork"]

def check_orders():
    """Функция проверяет заказы и отправляет уведомления в Telegram."""
    sent_orders = set()  # Храним уже отправленные заказы

    while True:
        orders = get_kwork_orders()
        for order in orders:
            if order not in sent_orders:  # Отправляем только новые заказы
                bot.send_message(CHAT_ID, order)
                sent_orders.add(order)

        time.sleep(600)  # Ждем 10 минут перед следующей проверкой

# Функция для обработки команды /start и кнопки
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton("Последний заказ")
    markup.add(button)
    bot.send_message(message.chat.id, "Привет! Нажми кнопку, чтобы получить последний подходящий заказ с Kwork.", reply_markup=markup)

# Обработчик нажатия кнопки "Последний заказ"
@bot.message_handler(func=lambda message: message.text == "Последний заказ")
def send_last_order(message):
    if last_order:
        bot.send_message(message.chat.id, last_order)
    else:
        bot.send_message(message.chat.id, "На данный момент нет подходящих заказов.")

# Запускаем проверку заказов в отдельном потоке
threading.Thread(target=check_orders, daemon=True).start()

# Запускаем бота
bot.polling()
