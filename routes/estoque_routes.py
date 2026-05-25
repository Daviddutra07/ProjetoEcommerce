from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database.database import get_session
from models.models import Estoque


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/estoque",
    tags=["estoque"]
)


@router.post("/", response_model=Estoque)
def criar_estoque(
    estoque: Estoque,
    session: SessionDep
):

    estoque.id = None
    estoque.atualizado_em = datetime.now()

    session.add(estoque)
    session.commit()
    session.refresh(estoque)

    return estoque


@router.get("/", response_model=list[Estoque])
def listar_estoque(session: SessionDep):

    return session.exec(
        select(Estoque)
    ).all()


@router.get("/{estoque_id}", response_model=Estoque)
def buscar_estoque(
    estoque_id: int,
    session: SessionDep
):

    estoque = session.get(
        Estoque,
        estoque_id
    )

    if not estoque:
        raise HTTPException(
            404,
            "Estoque não encontrado"
        )

    return estoque


@router.put("/{estoque_id}", response_model=Estoque)
def atualizar_estoque(
    estoque_id: int,
    dados: Estoque,
    session: SessionDep
):

    estoque = session.get(
        Estoque,
        estoque_id
    )

    if not estoque:
        raise HTTPException(
            404,
            "Estoque não encontrado"
        )

    estoque.quantidade = dados.quantidade
    estoque.atualizado_em = datetime.now()

    session.commit()
    session.refresh(estoque)

    return estoque


@router.delete("/{estoque_id}")
def deletar_estoque(
    estoque_id: int,
    session: SessionDep
):

    estoque = session.get(
        Estoque,
        estoque_id
    )

    if not estoque:
        raise HTTPException(
            404,
            "Estoque não encontrado"
        )

    session.delete(estoque)
    session.commit()

    return {"ok": True}