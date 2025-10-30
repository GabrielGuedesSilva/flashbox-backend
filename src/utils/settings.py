from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TZ: str = 'America/Sao_Paulo'
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_HOURS: float = 8
    REFRESH_TOKEN_EXPIRE_DAYS: int = 5
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )
