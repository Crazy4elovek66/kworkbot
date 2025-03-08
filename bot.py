import telebot

# Вставьте сюда свой токен, который вы получите от @BotFather в Telegram
API_TOKEN = '8081177731:AAHi6xBekqBeOxsxweLd7P-075UobWS38j8'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой бот. Чем могу помочь?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()
