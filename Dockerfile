FROM python:3.11-slim

# Установка зависимостей для браузера
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libdbus-1-3 \
    libatk-1.0-0 \
    libatk-bridge2.0-0 \
    libexpat1 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxi6 \
    libxrandr2 \
    libxfixes3 \
    libx11-xcb1

# Установка зависимостей для Playwright
RUN pip install playwright
RUN playwright install --with-deps

# Копирование файлов проекта в контейнер
WORKDIR /app
COPY . /app

# Установка Python зависимостей
RUN pip install -r requirements.txt

# Запуск вашего скрипта
CMD ["python", "bot.py"]
