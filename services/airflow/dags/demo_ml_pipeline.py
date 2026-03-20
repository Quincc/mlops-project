from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def extract_data():
    print("Extracting demo data")


def train_model():
    print("Training demo model")


def log_to_mlflow():
    print("Logging artifacts to MLflow")


with DAG(
    dag_id="demo_ml_pipeline",
    start_date=datetime(2026, 3, 1),
    schedule=None,
    catchup=False,
    tags=["demo", "ml"],
) as dag:
    task_extract = PythonOperator(task_id="extract_data", python_callable=extract_data)
    task_train = PythonOperator(task_id="train_model", python_callable=train_model)
    task_log = PythonOperator(task_id="log_to_mlflow", python_callable=log_to_mlflow)

    task_extract >> task_train >> task_log
