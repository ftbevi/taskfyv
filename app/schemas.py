from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TarefaCriar(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    concluida: bool = False


class TarefaAtualizar(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=200)
    concluida: bool | None = None


class TarefaLer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    concluida: bool
    criada_em: datetime
