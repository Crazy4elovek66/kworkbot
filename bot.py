import telebot
import schedule
import time

# Вставьте сюда свой токен, который вы получите от @BotFather в Telegram
API_TOKEN = '8081177731:AAHi6xBekqBeOxsxweLd7P-075UobWS38j8'

bot = telebot.TeleBot(API_TOKEN)

# Функция, которая будет проверять задания на Kwork
def check_kwork():
    # Здесь будет код для мониторинга заданий на Kwork
    # Например, выведем сообщение в консоль (позже заменим на отправку сообщений в Telegram)
    print("Проверяю задания на Kwork...")

    # Здесь нужно добавить реальный код для поиска заданий на Kwork
    # После нахождения подходящего задания, отправляем уведомление в Telegram
    bot.send_message(437225657, "Найдено новое подходящее задание на Kwork!")  # Замените 123456789 на свой чат ID

# Настроим периодическую проверку каждую 10 минут
schedule.every(10).minutes.do(check_kwork)

# Обработчик команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой бот. Чем могу помочь?")

# Обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Основной цикл бота, который будет работать постоянно
while True:
    schedule.run_pending()  # Проверяем задания
    time.sleep(1)  # Ожидаем 1 секунду перед следующей проверкой
    bot.polling(none_stop=True)  # Продолжаем слушать команды от пользователей
