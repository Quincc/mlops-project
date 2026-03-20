# MLOps Project

Платформа для полного цикла ML-разработки: от экспериментов и обучения моделей до продакшн-деплоя с мониторингом. Все сервисы оркестрируются через Docker Compose, а для Kubernetes-деплоя подготовлены манифесты и Helm-чарт.

## Архитектура

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Airflow    │     │   MLflow     │     │  JupyterHub  │
│  Пайплайны   │     │  Трекинг     │     │  Ноутбуки    │
│  :8080       │     │  :5001       │     │  :8001       │
└──────┬───────┘     └──────┬───────┘     └──────────────┘
       │                    │
       ▼                    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  ML Service  │────▶│  PostgreSQL  │◀────│   LakeFS     │
│  FastAPI     │     │    :5432     │     │   :8000      │
│  :8002       │     └──────────────┘     └──────┬───────┘
└──────┬───────┘                                 │
       │                                         ▼
       ▼                                  ┌──────────────┐
┌──────────────┐     ┌──────────────┐     │    MinIO      │
│  Prometheus  │────▶│   Grafana    │     │  S3-хранилище │
│  :9090       │     │   :3000      │     │  :9000/:9001  │
└──────────────┘     └──────────────┘     └──────────────┘
```

## Стек технологий

| Компонент | Технология | Назначение |
|-----------|-----------|------------|
| ML-сервис | FastAPI + Uvicorn | Prediction API с метриками |
| База данных | PostgreSQL 16 | Хранение данных всех сервисов |
| Миграции | Alembic + SQLAlchemy 2.0 (async) | Управление схемой БД |
| Трекинг экспериментов | MLflow | Логирование параметров и метрик |
| Оркестрация пайплайнов | Apache Airflow | DAG-и для ML-пайплайнов |
| Версионирование данных | LakeFS + MinIO | Git-подобное управление данными |
| Ноутбуки | JupyterHub | Интерактивная разработка |
| Мониторинг | Prometheus + Grafana | Сбор и визуализация метрик |
| Контейнеризация | Docker Compose | Локальная оркестрация |
| Деплой | Kubernetes / Helm | Продакшн-деплой |

## Структура проекта

```
mlops-project/
├── docker-compose.yml              # Оркестрация всех сервисов
├── .env / .env.example             # Переменные окружения
├── services/
│   ├── ml-service/                 # FastAPI prediction-сервис
│   │   ├── app/
│   │   │   ├── main.py             # Точка входа, lifespan, метрики
│   │   │   ├── api/routes.py       # POST /api/v1/predict
│   │   │   ├── core/config.py      # Pydantic Settings
│   │   │   ├── db/                 # AsyncSession, Base
│   │   │   ├── models/             # SQLAlchemy-модель PredictionLog
│   │   │   ├── schemas/            # Pydantic-схемы запроса/ответа
│   │   │   └── services/           # Бизнес-логика предсказания и логирования
│   │   ├── alembic/                # Миграции БД
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── airflow/                    # Airflow + демо-DAG
│   ├── mlflow/                     # MLflow Tracking Server
│   ├── jupyterhub/                 # JupyterHub + JupyterLab
│   └── postgres/init/              # SQL-скрипт инициализации БД
├── monitoring/
│   └── prometheus.yml              # Конфигурация Prometheus
├── k8s/                            # Kubernetes-манифесты
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
├── helm/ml-service/                # Helm-чарт для ML-сервиса
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
├── prompts/                        # Версионированные промпты
│   ├── prompt_v1.txt
│   ├── prompt_v2.txt
│   └── prompt_v3.txt
├── tests/                          # Тесты
│   └── test_mlflow.py
└── logs/                           # Логи сервисов
```

## Быстрый старт

### Требования

- Docker и Docker Compose
- (опционально) `kubectl` + `helm` для K8s-деплоя

### Запуск

1. **Склонировать репозиторий и настроить окружение:**

```bash
cp .env.example .env
```

2. **Поднять все сервисы:**

```bash
docker compose up -d
```

3. **Проверить ML-сервис:**

```bash
# Health-check
curl http://localhost:8002/health

# Предсказание
curl -X POST http://localhost:8002/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"feature1": 1.0, "feature2": 2.0, "feature3": 0.5}'
```

### Доступ к сервисам

| Сервис | URL | Логин / Пароль |
|--------|-----|----------------|
| ML Service | http://localhost:8002 | — |
| MLflow | http://localhost:5001 | — |
| Airflow | http://localhost:8080 | admin / admin |
| JupyterHub | http://localhost:8001 | admin / admin |
| LakeFS | http://localhost:8000 | lakefs / lakefssecret |
| MinIO Console | http://localhost:9001 | minioadmin / minioadmin |
| Prometheus | http://localhost:9090 | — |
| Grafana | http://localhost:3000 | admin / admin |

## ML Service API

### `POST /api/v1/predict`

**Запрос:**
```json
{
  "feature1": 1.0,
  "feature2": 2.0,
  "feature3": 0.5
}
```

**Ответ:**
```json
{
  "prediction": 1.15,
  "model_version": "demo-model-1.0.0",
  "duration_ms": 0.042
}
```

### `GET /health`

Возвращает `{"status": "ok"}`.

### `GET /metrics`

Prometheus-метрики в формате OpenMetrics:
- `ml_service_requests_total` — общее количество запросов
- `ml_service_prediction_latency_seconds` — латентность предсказания
- `ml_service_prediction_value` — последнее значение предсказания

## Деплой в Kubernetes

### Манифесты

```bash
kubectl apply -f k8s/
```

### Helm

```bash
helm install ml-service ./helm/ml-service
```

Параметры настраиваются в `helm/ml-service/values.yaml`:
- `replicaCount` — количество реплик
- `image.repository` / `image.tag` — образ контейнера
- `resources` — CPU/memory лимиты
- `ingress.host` — хост для Ingress
- `env.APP_DB_URL` — строка подключения к БД

## Мониторинг

Prometheus собирает метрики с ML-сервиса каждые 5 секунд (`/metrics`). Grafana подключается к Prometheus как источник данных для построения дашбордов.

## Версионирование промптов

Директория `prompts/` содержит версионированные промпт-шаблоны для LLM-классификатора тональности:

- **v1** — базовая классификация (только метка)
- **v2** — расширенная версия (JSON с меткой и confidence)
- **v3** — строгий формат (JSON без пояснений)
