from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.database import SessionLocal, engine
from app.routers import tarefas


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # A Vercel dá no máximo 500ms após o SIGTERM para o shutdown,
    # e logs desta etapa não aparecem no dashboard.
    await engine.dispose()


app = FastAPI(title="Tarefas API", version="0.1.0", lifespan=lifespan)
app.include_router(tarefas.router)


@app.get("/")
async def raiz():
    return {"status": "ok"}


@app.get("/health")
async def health():
    async with SessionLocal() as sessao:
        await sessao.execute(text("SELECT 1"))
    return {"database": "ok"}
