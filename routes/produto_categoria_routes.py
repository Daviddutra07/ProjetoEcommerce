from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from database.database import get_session
from models.models import Produto, Categoria


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/produtos",
    tags=["produto_categoria"]
)


@router.post("/{produto_id}/categorias/{categoria_id}")
def adicionar_categoria_produto(
    produto_id: int,
    categoria_id: int,
    session: SessionDep
):

    produto = session.get(Produto, produto_id)
    categoria = session.get(Categoria, categoria_id)

    if not produto or not categoria:
        raise HTTPException(
            404,
            "Produto ou categoria não encontrado"
        )

    if categoria in produto.categorias:
        return {
            "msg": "Produto já possui essa categoria"
        }

    produto.categorias.append(categoria)

    session.add(produto)
    session.commit()

    return {"ok": True}


@router.get("/{produto_id}/categorias")
def listar_categorias_produto(
    produto_id: int,
    session: SessionDep
):

    produto = session.get(Produto, produto_id)

    if not produto:
        raise HTTPException(
            404,
            "Produto não encontrado"
        )

    return produto.categorias


@router.put("/{produto_id}/categorias/{categoria_antiga_id}")
def atualizar_categoria_produto(
    produto_id: int,
    categoria_antiga_id: int,
    nova_categoria_id: int,
    session: SessionDep
):

    produto = session.get(Produto, produto_id)

    if not produto:
        raise HTTPException(
            404,
            "Produto não encontrado"
        )

    categoria_antiga = session.get(
        Categoria,
        categoria_antiga_id
    )

    nova_categoria = session.get(
        Categoria,
        nova_categoria_id
    )

    if not categoria_antiga or not nova_categoria:
        raise HTTPException(
            404,
            "Categoria não encontrada"
        )

    if categoria_antiga not in produto.categorias:
        raise HTTPException(
            404,
            "Categoria não vinculada ao produto"
        )

    produto.categorias.remove(categoria_antiga)

    if nova_categoria not in produto.categorias:
        produto.categorias.append(nova_categoria)

    session.commit()

    return {"ok": True}


@router.delete("/{produto_id}/categorias/{categoria_id}")
def remover_categoria_produto(
    produto_id: int,
    categoria_id: int,
    session: SessionDep
):

    produto = session.get(Produto, produto_id)
    categoria = session.get(Categoria, categoria_id)

    if not produto or not categoria:
        raise HTTPException(
            404,
            "Produto ou categoria não encontrado"
        )

    if categoria not in produto.categorias:
        raise HTTPException(
            404,
            "Categoria não vinculada ao produto"
        )

    produto.categorias.remove(categoria)

    session.commit()

    return {"ok": True}