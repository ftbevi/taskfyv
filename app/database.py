from collections.abc import AsyncGenerator
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.config import dsn_async, settings


class Base(DeclarativeBase):
    pass


connect_args = {
    # O endpoint pooled da Neon é PgBouncer em modo transaction, que não
    # suporta prepared statements nomeados. Sem estes três ajustes você
    # colhe DuplicatePreparedStatementError de forma intermitente.
    "statement_cache_size": 0,
    "prepared_statement_cache_size": 0,
    "prepared_statement_name_func": lambda: f"__asyncpg_{uuid4()}__",
}

if settings.db_ssl:
    connect_args["ssl"] = "require"

engine = create_async_engine(
    dsn_async(settings.database_url),
    # NullPool porque o pooling já acontece no PgBouncer. Manter um pool do
    # SQLAlchemy por cima seria pooling duplo, com conexões que a função
    # serverless não vai reutilizar de forma previsível.
    poolclass=NullPool,
    connect_args=connect_args,
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as sessao:
        yield sessao