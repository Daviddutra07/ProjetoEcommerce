from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database.database import get_session
from models.models import Categoria


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/categorias",
    tags=["categorias"]
)


@router.post("/", response_model=Categoria)
def criar_categoria(
    categoria: Categoria,
    session: SessionDep
):

    categoria.id = None

    session.add(categoria)
    session.commit()
    session.refresh(categoria)

    return categoria


@router.get("/", response_model=list[Categoria])
def listar_categorias(session: SessionDep):

    return session.exec(select(Categoria)).all()


@router.delete("/{categoria_id}")
def deletar_categoria(
    categoria_id: int,
    session: SessionDep
):

    categoria = session.get(Categoria, categoria_id)

    if not categoria:
        raise HTTPException(404, "Categoria não encontrada")

    session.delete(categoria)
    session.commit()

    return {"ok": True}