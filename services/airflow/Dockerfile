FROM apache/airflow:2.10.5-python3.11

USER root
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
USER airflow
RUN pip install --no-cache-dir psycopg2-binary mlflow
