import time
import telebot
from playwright.sync_api import sync_playwright

# Ваши настройки
API_TOKEN = '8081177731:AAHi6xBekqBeOxsxweLd7P-075UobWS38j8'
KWORK_URL = "https://kwork.ru/projects?c=15"  # Убедись, что это правильный URL
KEYWORDS = ['python', 'дизайн', 'веб']  # Пример ключевых слов
CHAT_ID = '437225657'  # ID чата для отправки сообщений

bot = telebot.TeleBot(API_TOKEN)

def send_telegram_message(message):
    """Функция для отправки сообщений в Telegram."""
    bot.send_message(CHAT_ID, message)

def get_kwork_orders():
    """Функция парсит сайт Kwork и возвращает только подходящие заказы."""
    orders = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(KWORK_URL, timeout=30000)  # Тайм-аут на загрузку страницы
            page.wait_for_load_state("load")  # Ждем полной загрузки страницы

            # Перебор нескольких страниц с повторной попыткой при ошибке
            for page_num in range(1, 5):
                try:
                    page.goto(f"{KWORK_URL}&page={page_num}", timeout=30000)  # Тайм-аут на каждую страницу
                    page.wait_for_timeout(5000)  # Дополнительная пауза

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

        except Exception as e:
            print(f"Ошибка загрузки страницы: {e}")
        finally:
            browser.close()

    return orders

def check_orders():
    """Запускает функцию проверки заказов по расписанию."""
    while True:
        orders = get_kwork_orders()
        if orders:
            message = f"Найдено {len(orders)} подходящих заказов:\n"
            message += "\n\n".join(orders)
            send_telegram_message(message)
        else:
            send_telegram_message("Нет подходящих заказов.")
        time.sleep(600)  # Пауза в 10 минут

if __name__ == "__main__":
    check_orders()
