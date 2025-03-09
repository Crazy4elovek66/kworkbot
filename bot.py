import requests
from bs4 import BeautifulSoup
import telebot
import time
import threading
from telebot import types

# Токен бота
API_TOKEN = '8081177731:AAHi6xBekqBeOxsxweLd7P-075UobWS38j8'
bot = telebot.TeleBot(API_TOKEN)

# ID чата
CHAT_ID = '437225657'

# URL категории "Графический дизайн"
KWORK_URL = "https://kwork.ru/projects?c=15"

# Ключевые слова
KEYWORDS = [
    "логотип", "баннер", "оформление YouTube", "оформление Twitch", "оформление VK",
    "аватарка", "превью", "иконки", "фирменный стиль", "дизайн визитки",
    "дизайн буклета", "дизайн флаера", "дизайн упаковки",
    "инфографика", "иллюстрация", "постер", "стикеры",
    "дизайн презентации", "веб-дизайн", "оформление постов", "креативный дизайн",
    "листовка", "флаер", "дизайн листовки", "дизайн флаера", "рекламная листовка",
    "рекламный флаер", "брендовая листовка", "брендовый флаер", "листовка для мероприятия",
    "флаер для мероприятия", "промо-листовка", "промо-флаер", "визитка", "дизайн визитки",
    "визитная карточка", "брендовая визитка", "корпоративная визитка", "персональная визитка",
    "визитка для компании", "визитка для бизнеса", "креативная визитка", "премиум визитка",
    "эксклюзивная визитка", "YouTube", "Twitch", "VK"
]

# Получение подходящих заказов без фильтрации по стоп-словам
def get_kwork_orders():
    headers = {"User-Agent": "Mozilla/5.0"}
    orders = []

    for page in range(1, 5):
        url = f"{KWORK_URL}&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            order_cards = soup.find_all("div", class_="card__content")

            for order in order_cards:
                title_tag = order.find("a", class_="wants-card__header-title")
                description_tag = order.find("div", class_="wants-card__description")
                price_tag = order.find("div", class_="wants-card__price")

                if not title_tag or not price_tag:
                    continue

                title = title_tag.text.strip()
                description = description_tag.text.strip() if description_tag else ""
                link = "https://kwork.ru" + title_tag["href"]
                price = price_tag.text.strip()

                if any(word.lower() in title.lower() or word.lower() in description.lower() for word in KEYWORDS):
                    orders.append(f"📌 {title}\n💰 {price}\n🔗 {link}")

    return orders

# Проверка заказов и отправка новых
def check_orders():
    last_orders = []

    while True:
        orders = get_kwork_orders()
        if orders:
            for order in orders:
                if order not in last_orders:
                    bot.send_message(CHAT_ID, order)
                    last_orders.append(order)
        time.sleep(600)

# Ручной показ последнего заказа
def send_last_order(message):
    last_orders = get_kwork_orders()
    if last_orders:
        bot.send_message(message.chat.id, last_orders[-1])
    else:
        bot.send_message(message.chat.id, "❌ Нет подходящих заказов.")

# Принудительный запуск проверки
def force_scan_orders(message):
    orders = get_kwork_orders()
    if orders:
        for order in orders:
            bot.send_message(message.chat.id, order)
    else:
        bot.send_message(message.chat.id, "❌ Нет подходящих заказов.")

# Обработка команды /last_order
@bot.message_handler(commands=['last_order'])
def handle_last_order(message):
    send_last_order(message)

# Обработка команды /force_scan — вывод кнопки
@bot.message_handler(commands=['force_scan'])
def handle_force_scan(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text="🔍 Найти заказы сейчас", callback_data="force_scan_orders")
    markup.add(btn)
    bot.send_message(message.chat.id, "Нажми кнопку ниже для сканирования:", reply_markup=markup)

# Обработка нажатия на кнопку
@bot.callback_query_handler(func=lambda call: call.data == "force_scan_orders")
def callback_force_scan(call):
    force_scan_orders(call.message)

# Запуск в отдельном потоке
threading.Thread(target=check_orders, daemon=True).start()

# Старт бота
bot.polling()
