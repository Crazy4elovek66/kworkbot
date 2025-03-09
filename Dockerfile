# Используем официальный Python-образ
FROM python:3.11-slim

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    wget unzip gnupg curl \
    && apt-get clean

# Устанавливаем Playwright и необходимые браузеры
RUN pip install playwright && playwright install

# Копируем проект в контейнер
COPY . /app
WORKDIR /app

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем основной скрипт
CMD ["python", "bot.py"]
