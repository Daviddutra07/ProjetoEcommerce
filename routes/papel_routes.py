from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database.database import get_session
from models.models import Papel, Usuario


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/papeis",
    tags=["papeis"]
)


@router.post("/", response_model=Papel)
def criar_papel(papel: Papel, session: SessionDep):

    papel.id = None

    session.add(papel)
    session.commit()
    session.refresh(papel)

    return papel


@router.get("/", response_model=list[Papel])
def listar_papeis(session: SessionDep):

    return session.exec(select(Papel)).all()


@router.get("/{papel_id}", response_model=Papel)
def buscar_papel(papel_id: int, session: SessionDep):

    papel = session.get(Papel, papel_id)

    if not papel:
        raise HTTPException(404, "Papel não encontrado")

    return papel


@router.delete("/{papel_id}")
def deletar_papel(papel_id: int, session: SessionDep):

    papel = session.get(Papel, papel_id)

    if not papel:
        raise HTTPException(404, "Papel não encontrado")

    session.delete(papel)
    session.commit()

    return {"ok": True}


@router.post("/usuarios/{usuario_id}/{papel_id}")
def adicionar_papel(
    usuario_id: int,
    papel_id: int,
    session: SessionDep
):

    usuario = session.get(Usuario, usuario_id)
    papel = session.get(Papel, papel_id)

    if not usuario or not papel:
        raise HTTPException(404, "Usuário ou papel não encontrado")

    if papel in usuario.papeis:
        return {"msg": "Usuário já possui esse papel"}

    usuario.papeis.append(papel)

    session.add(usuario)
    session.commit()

    return {"ok": True}


@router.get("/usuarios/{usuario_id}")
def listar_papeis_usuario(
    usuario_id: int,
    session: SessionDep
):

    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")

    return usuario.papeis