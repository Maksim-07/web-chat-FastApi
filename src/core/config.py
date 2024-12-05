import functools
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Класс настроек проекта: импорт параметров из .env
    и установка значений по умолчанию.
    """

    root_dir: str = os.path.abspath(__file__ + 3 * "/..")
    src_dir: str = os.path.join(root_dir, "src")

    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    ENVIRONMENT: str = "local"

    CORS_ALLOW_ORIGIN_LIST: str = "http://127.0.0.1:8000"

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    ALGORITHM: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @functools.cached_property
    def cors_allow_origins(self) -> list[str]:
        return self.CORS_ALLOW_ORIGIN_LIST.split("&")

    @functools.cached_property
    def postgres_dsn(self) -> str:
        postgres_host = "localhost" if self.ENVIRONMENT == "local" else self.POSTGRES_HOST
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{postgres_host}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@functools.lru_cache()
def settings():
    return Settings()
