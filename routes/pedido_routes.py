from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database.database import get_session
from models.models import Pedido


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/pedidos",
    tags=["pedidos"]
)


@router.post("/", response_model=Pedido)
def criar_pedido(
    pedido: Pedido,
    session: SessionDep
):

    pedido.id = None
    pedido.criado_em = datetime.now()

    session.add(pedido)
    session.commit()
    session.refresh(pedido)

    return pedido


@router.get("/", response_model=list[Pedido])
def listar_pedidos(session: SessionDep):

    return session.exec(select(Pedido)).all()


@router.get("/{pedido_id}", response_model=Pedido)
def buscar_pedido(
    pedido_id: int,
    session: SessionDep
):

    pedido = session.get(Pedido, pedido_id)

    if not pedido:
        raise HTTPException(
            404,
            "Pedido não encontrado"
        )

    return pedido


@router.delete("/{pedido_id}")
def deletar_pedido(
    pedido_id: int,
    session: SessionDep
):

    pedido = session.get(Pedido, pedido_id)

    if not pedido:
        raise HTTPException(
            404,
            "Pedido não encontrado"
        )

    session.delete(pedido)
    session.commit()

    return {"ok": True}