FROM python:3.11-slim

# Обновление пакетов и установка зависимостей
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libdbus-1-3 \
    libatk-bridge2.0-0 \
    libexpat1 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxi6 \
    libxrandr2 \
    libxfixes3 \
    libx11-xcb1 \
    libatk-bridge2.0-0

# Определяем переменные окружения (если нужно)
ENV BOT_TOKEN=8081177731:AAHi6xBekqBeOxsxweLd7P-075UobWS38j8
ENV CHAT_ID=437225657
ENV KEYWORDS="логотип,баннер,оформление,оформление ютуб,оформление YouTube,оформление твич,оформление Twitch,twitch,youtube,аватарка,превью,иконки,фирменный стиль,дизайн визитки,дизайн,дизайн буклета,дизайн флаера,дизайн объявления,дизайн листовки,дизайн упаковки,постер,креативный дизайн,листовка,флаер,рекламная листовка,рекламный флаер,визитка,дизайн визитки"

# Установка Playwright
RUN pip install playwright
RUN playwright install --with-deps

# Копирование файлов проекта
WORKDIR /app
COPY . /app

# Установка зависимостей Python
RUN pip install -r requirements.txt

# Запуск приложения
CMD ["python", "bot.py"]
