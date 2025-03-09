import requests
from bs4 import BeautifulSoup
import telebot
import time
import threading

# Токен и ID чата
API_TOKEN = '8081177731:AAHi6xBekqBeOxsxweLd7P-075UobWS38j8'
CHAT_ID = '437225657'
bot = telebot.TeleBot(API_TOKEN)

# URL Kwork категории "Графический дизайн"
KWORK_URL = "https://kwork.ru/projects?c=15"

# Ключевые слова (обновлённые)
KEYWORDS = [
    "логотип", "баннер", "оформление YouTube", "оформление Twitch",
    "YouTube", "Twitch", "VK", "ВКонтакте", "аватарка", "превью", "иконки",
    "фирменный стиль", "визитка", "листовка", "флаер", "презентация",
    "дизайн визитки", "дизайн листовки", "дизайн флаера",
    "брендовая листовка", "корпоративная визитка"
]

# Получение заказов
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
                full_text = order.get_text(separator=" ").lower()
                if any(keyword.lower() in full_text for keyword in KEYWORDS):
                    title_tag = order.find("a", class_="wants-card__header-title")
                    description_tag = order.find("div", class_="wants-card__description")
                    price_tag = order.find("div", class_="wants-card__price")

                    title = title_tag.text.strip() if title_tag else "Без названия"
                    description = description_tag.text.strip() if description_tag else ""
                    price = price_tag.text.strip() if price_tag else "Цена не указана"
                    link = "https://kwork.ru" + title_tag["href"] if title_tag else "Ссылка не найдена"

                    orders.append(f"📌 {title}\n💰 {price}\n🔗 {link}")
    return orders

# Хранение последних заказов
last_orders = []

# Фоновая проверка каждые 10 минут
def run_checker():
    global last_orders
    while True:
        new_orders = get_kwork_orders()
        if new_orders:
            for order in new_orders:
                if order not in last_orders:
                    bot.send_message(CHAT_ID, order)
                    last_orders.append(order)
        time.sleep(600)

# Команда /last_order
@bot.message_handler(commands=['last_order'])
def send_last_order(message):
    if last_orders:
        bot.send_message(message.chat.id, last_orders[-1])
    else:
        bot.send_message(message.chat.id, "❌ Пока нет сохранённых заказов.")

# Команда /scan — ручной запуск и отображение результата
@bot.message_handler(commands=['scan'])
def force_scan(message):
    global last_orders
    new_orders = get_kwork_orders()
    found = 0
    if new_orders:
        for order in new_orders:
            if order not in last_orders:
                bot.send_message(message.chat.id, order)
                last_orders.append(order)
                found += 1
        bot.send_message(message.chat.id, f"✅ Найдено новых заказов: {found}")
    else:
        bot.send_message(message.chat.id, "❌ Подходящих заказов не найдено.")

# Запуск фонового потока и бота
threading.Thread(target=run_checker, daemon=True).start()
bot.polling()
