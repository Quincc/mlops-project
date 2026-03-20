import mlflow

mlflow.set_tracking_uri("http://localhost:5001")
mlflow.set_experiment("homework-exp")

with mlflow.start_run():
    mlflow.log_param("model", "test-model")
    mlflow.log_metric("accuracy", 0.95)