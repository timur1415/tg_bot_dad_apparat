# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /app

# Копируем файлы
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Команда запуска бота
CMD ["watchfiles", "--ignore-paths", "/app/.venv", "--ignore-paths", "/app/__pycache__", "--", "python -u main.py"]