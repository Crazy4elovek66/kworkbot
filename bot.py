import requests
from bs4 import BeautifulSoup
import telebot
import time
import threading

# Токен твоего бота
API_TOKEN = '8081177731:AAHi6xBekqBeOxsxweLd7P-075UobWS38j8'
bot = telebot.TeleBot(API_TOKEN)

# ID чата, куда бот будет отправлять уведомления
CHAT_ID = '437225657'

# URL категории "Графический дизайн" на Kwork
KWORK_URL = "https://kwork.ru/projects?c=15"

# Ключевые слова, которые должны быть в заказе (ТОЛЬКО такие заказы отправляем)
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

# Стоп-слова (если есть в заказе — игнорируем)
STOPWORDS = [
    "презентация", "отредактировать", "изменить текст",
    "чертеж", "архитектура", "3D", "моделирование", "интерьер", "экстерьер"
]

# Функция парсит сайт Kwork и возвращает только подходящие заказы
def get_kwork_orders():
    """Функция парсит сайт Kwork и возвращает только подходящие заказы."""
    headers = {"User-Agent": "Mozilla/5.0"}
    orders = []

    for page in range(1, 5):  # Перебираем 4 страницы
        url = f"{KWORK_URL}&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            order_cards = soup.find_all("div", class_="card__content")

            for order in order_cards:
                title = order.find("a", class_="wants-card__header-title").text.strip()
                link = "https://kwork.ru" + order.find("a")["href"]
                price = order.find("div", class_="wants-card__price").text.strip()

                # Фильтрация по ключевым словам
                if any(word.lower() in title.lower() for word in KEYWORDS):
                    # Проверяем, что в заказе НЕТ стоп-слов
                    if not any(stopword.lower() in title.lower() for stopword in STOPWORDS):
                        orders.append(f"📌 {title}\n💰 {price}\n🔗 {link}")

    return orders

# Функция проверяет заказы и отправляет уведомления в Telegram
def check_orders():
    """Функция проверяет заказы и отправляет уведомления в Telegram."""
    last_orders = []  # Храним список найденных заказов
