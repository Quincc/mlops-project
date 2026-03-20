FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir "mlflow<3" psycopg2-binary

EXPOSE 5000
