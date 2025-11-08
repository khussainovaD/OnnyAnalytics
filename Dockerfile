# Dockerfile для Custom Exporter
FROM python:3.9-slim

WORKDIR /app

# Копируем требования и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем наш скрипт
COPY custom_exporter.py .

# Команда для запуска экспортера
CMD ["python", "custom_exporter.py"]