FROM python:3.10-slim-bullseye

# Настройки Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Системные зависимости: компиляторы, dev-пакеты для PostgreSQL/MySQL, wkhtmltopdf и шрифты для кириллицы
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       default-libmysqlclient-dev \
       wkhtmltopdf \
       fontconfig \
       xfonts-75dpi \
       xfonts-base \
       fonts-dejavu \
       fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Устанавливаем Python-зависимости
COPY requirements.txt /code
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . /code
