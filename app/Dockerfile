FROM python:3.13-slim

WORKDIR /app

# Установка зависимостей с подробной отладкой
COPY requirements.txt .
RUN set -ex && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
