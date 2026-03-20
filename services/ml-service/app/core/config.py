from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'ml-service'
    app_version: str = '1.0.0'
    app_db_url: str = 'postgresql+asyncpg://postgres:postgres@postgres:5432/ml_service_db'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
