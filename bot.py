import telebot
from playwright.sync_api import sync_playwright
import time
import threading

# Токен твоего бота
API_TOKEN = '8081177731:AAHi6xBekqBeOxsxweLd7P-075UobWS38j8'
bot = telebot.TeleBot(API_TOKEN)

# ID чата, куда бот будет отправлять уведомления
CHAT_ID = '437225657'

# URL категории "Графический дизайн" на Kwork
KWORK_URL = "https://kwork.ru/projects?c=15"

# Ключевые слова для поиска
KEYWORDS = [
    "логотип", "баннер", "оформление YouTube", "оформление Twitch",
    "аватарка", "превью", "иконки", "фирменный стиль", "дизайн визитки",
    "дизайн буклета", "дизайн флаера", "дизайн упаковки",
    "инфографика", "иллюстрация", "постер", "стикеры",
    "дизайн презентации", "веб-дизайн", "оформление постов", "креативный дизайн",
    "листовка", "флаер", "дизайн листовки", "дизайн флаера", "рекламная листовка",
    "рекламный флаер", "визитка", "дизайн визитки",
]

# Функция парсит сайт Kwork с использованием Playwright
def get_kwork_orders():
    """Функция парсит сайт Kwork и возвращает только подходящие заказы."""
    orders = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(KWORK_URL)

        page.wait_for_load_state("networkidle")  # Ждем, пока страница полностью загрузится

        # Перебор нескольких страниц с повторной попыткой при ошибке
        for page_num in range(1, 5):  # Перебираем 4 страницы
            try:
                page.goto(f"{KWORK_URL}&page={page_num}")
                page.wait_for_timeout(5000)  # Ждем 5 секунд для стабильности
                time.sleep(3)  # Дополнительная пауза для корректной загрузки контента

                order_cards = page.query_selector_all(".card__content")
                print(f"Страница {page_num}: найдено {len(order_cards)} заказов.")  # Логирование найденных карточек

                for order in order_cards:
                    title = order.query_selector(".wants-card__header-title")
                    description = order.query_selector(".wants-card__description")
                    price = order.query_selector(".wants-card__price")

                    if title and description and price:
                        title = title.inner_text().strip()
                        description = description.inner_text().strip()
                        price = price.inner_text().strip()

                        link = "https://kwork.ru" + order.query_selector("a")["href"]

                        # Логируем данные о заказе
                        print(f"Заголовок: {title}")
                        print(f"Описание: {description}")
                        print(f"Цена: {price}")
                        print(f"Ссылка: {link}")

                        # Фильтрация по ключевым словам
                        if any(word.lower() in title.lower() for word in KEYWORDS) or any(word.lower() in description.lower() for word in KEYWORDS):
                            orders.append(f"📌 {title}\n💰 {price}\n🔗 {link}")
            except Exception as e:
                print(f"Ошибка при загрузке страницы {page_num}: {e}")
                time.sleep(10)  # Ждем 10 секунд перед повтором

        browser.close()

    return orders

# Функция проверяет заказы и отправляет уведомления в Telegram
def check_orders():
    """Функция проверяет заказы и отправляет уведомления в Telegram."""
    last_orders = []  # Храним список найденных заказов

    while True:
        orders = get_kwork_orders()
        print(f"Найдено заказов: {len(orders)}")  # Логирование количества найденных заказов
        if orders:  # Если есть новые заказы
            for order in orders:
                if order not in last_orders:  # Отправляем только новые заказы
                    bot.send_message(CHAT_ID, order)
                    last_orders.append(order)
        time.sleep(600)  # Ждем 10 минут перед следующей проверкой

# Функция для отправки последнего найденного заказа
def send_last_order(message):
    """Отправляет последний найденный заказ при запросе."""
    last_orders = get_kwork_orders()
    if last_orders:
        bot.send_message(message.chat.id, last_orders[-1])
    else:
        bot.send_message(message.chat.id, "❌ Нет подходящих заказов.")

# Обработка кнопки для запроса последнего заказа
@bot.message_handler(commands=['last_order'])
def handle_last_order(message):
    send_last_order(message)

# Добавление кнопки для принудительного сканирования
@bot.message_handler(commands=['scan'])
def handle_scan(message):
    bot.send_message(message.chat.id, "✅ Принудительное сканирование завершено!")
    orders = get_kwork_orders()
    
    if orders:
        for order in orders:
            bot.send_message(message.chat.id, order)
    else:
        bot.send_message(message.chat.id, "❌ Нет подходящих заказов.")

# Запускаем проверку заказов в отдельном потоке
threading.Thread(target=check_orders, daemon=True).start()

# Запускаем бота
bot.polling()
