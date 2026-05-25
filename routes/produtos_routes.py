from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database.database import get_session
from models.models import Produto


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/produtos",
    tags=["produtos"]
)


@router.post("/", response_model=Produto)
def criar_produto(produto: Produto, session: SessionDep):

    produto.id = None
    produto.criado_em = datetime.now()

    session.add(produto)
    session.commit()
    session.refresh(produto)

    return produto


@router.get("/", response_model=list[Produto])
def listar_produtos(session: SessionDep):

    return session.exec(select(Produto)).all()


@router.get("/{produto_id}", response_model=Produto)
def buscar_produto(produto_id: int, session: SessionDep):

    produto = session.get(Produto, produto_id)

    if not produto:
        raise HTTPException(404, "Produto não encontrado")

    return produto


@router.put("/{produto_id}", response_model=Produto)
def atualizar_produto(
    produto_id: int,
    dados: Produto,
    session: SessionDep
):

    produto = session.get(Produto, produto_id)

    if not produto:
        raise HTTPException(404, "Produto não encontrado")

    produto.nome = dados.nome
    produto.descricao = dados.descricao
    produto.preco = dados.preco

    session.commit()
    session.refresh(produto)

    return produto


@router.delete("/{produto_id}")
def deletar_produto(
    produto_id: int,
    session: SessionDep
):

    produto = session.get(Produto, produto_id)

    if not produto:
        raise HTTPException(404, "Produto não encontrado")

    session.delete(produto)
    session.commit()

    return {"ok": True}