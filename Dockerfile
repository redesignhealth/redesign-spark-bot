FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Persistent volume for SQLite database
RUN mkdir -p /data
VOLUME ["/data"]

EXPOSE 8080

CMD ["python", "app.py"]
