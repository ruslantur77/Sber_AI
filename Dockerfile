# Указываем конкретный базовый образ TensorFlow
FROM tensorflow/tensorflow:2.18.0

# Обновляем список пакетов и устанавливаем необходимые утилиты
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        git \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Переустанавливаем пакет blinker с игнорированием существующей установки
RUN pip install --ignore-installed --no-cache-dir blinker

# Копируем файл с зависимостями в контейнер
COPY requirements.txt /

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt && \
    rm -rf /root/.cache/pip

# Копируем весь проект в контейнер
COPY . /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Открываем порт для доступа к приложению снаружи контейнера
EXPOSE 5000

# Запускаем приложение
CMD ["python", "app.py"]