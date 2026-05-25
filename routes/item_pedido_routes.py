from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database.database import get_session
from models.models import ItemPedido, Pedido


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/itens-pedido",
    tags=["itens-pedido"]
)


@router.post("/", response_model=ItemPedido)
def criar_item(
    item: ItemPedido,
    session: SessionDep
):

    item.id = None

    session.add(item)
    session.commit()
    session.refresh(item)

    return item


@router.get("/", response_model=list[ItemPedido])
def listar_itens(session: SessionDep):

    return session.exec(
        select(ItemPedido)
    ).all()


@router.get("/{item_id}", response_model=ItemPedido)
def buscar_item(
    item_id: int,
    session: SessionDep
):

    item = session.get(
        ItemPedido,
        item_id
    )

    if not item:
        raise HTTPException(
            404,
            "Item não encontrado"
        )

    return item


@router.put("/{item_id}", response_model=ItemPedido)
def atualizar_item(
    item_id: int,
    dados: ItemPedido,
    session: SessionDep
):

    item = session.get(
        ItemPedido,
        item_id
    )

    if not item:
        raise HTTPException(
            404,
            "Item não encontrado"
        )

    item.quantidade = dados.quantidade
    item.preco = dados.preco

    session.commit()
    session.refresh(item)

    return item


@router.delete("/{item_id}")
def deletar_item(
    item_id: int,
    session: SessionDep
):

    item = session.get(
        ItemPedido,
        item_id
    )

    if not item:
        raise HTTPException(
            404,
            "Item não encontrado"
        )

    session.delete(item)
    session.commit()

    return {"ok": True}


@router.get("/pedidos/{pedido_id}/itens")
def listar_itens_pedido(
    pedido_id: int,
    session: SessionDep
):

    pedido = session.get(
        Pedido,
        pedido_id
    )

    if not pedido:
        raise HTTPException(
            404,
            "Pedido não encontrado"
        )

    return pedido.itens