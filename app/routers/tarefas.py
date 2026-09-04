from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Tarefa
from app.schemas import TarefaAtualizar, TarefaCriar, TarefaLer

router = APIRouter(prefix="/tarefas", tags=["tarefas"])

Sessao = Annotated[AsyncSession, Depends(get_session)]


@router.get("", response_model=list[TarefaLer])
async def listar(sessao: Sessao, limite: int = 50):
    resultado = await sessao.execute(select(Tarefa).order_by(Tarefa.id).limit(limite))
    return resultado.scalars().all()


@router.post("", response_model=TarefaLer, status_code=status.HTTP_201_CREATED)
async def criar(dados: TarefaCriar, sessao: Sessao):
    tarefa = Tarefa(**dados.model_dump())
    sessao.add(tarefa)
    await sessao.commit()
    await sessao.refresh(tarefa)
    return tarefa


@router.patch("/{tarefa_id}", response_model=TarefaLer)
async def atualizar(tarefa_id: int, dados: TarefaAtualizar, sessao: Sessao):
    tarefa = await sessao.get(Tarefa, tarefa_id)
    if tarefa is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tarefa não encontrada")

    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(tarefa, campo, valor)

    await sessao.commit()
    await sessao.refresh(tarefa)
    return tarefa


@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover(tarefa_id: int, sessao: Sessao):
    tarefa = await sessao.get(Tarefa, tarefa_id)
    if tarefa is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tarefa não encontrada")

    await sessao.delete(tarefa)
    await sessao.commit()
