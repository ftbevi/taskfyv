from functools import lru_cache
from urllib.parse import urlsplit, urlunsplit

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    db_ssl: bool = True


def dsn_async(url: str) -> str:
    """postgresql://... -> postgresql+asyncpg://..., sem a query string.

    O asyncpg não é libpq: ele não reconhece `sslmode` nem `channel_binding`,
    e levanta TypeError se esses parâmetros chegarem até ele. Como a Neon
    entrega a URL com os dois, a query é descartada aqui e o TLS é ligado
    depois, em connect_args.
    """
    partes = urlsplit(url)
    return urlunsplit(("postgresql+asyncpg", partes.netloc, partes.path, "", ""))


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()