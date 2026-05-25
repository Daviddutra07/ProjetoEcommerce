from datetime import datetime
import hashlib
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session

from database.database import get_session
from models.models import Usuario


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)


def hash_senha(senha: str):
    return hashlib.sha256(senha.encode()).hexdigest()


@router.get("/", response_model=list[Usuario])
def get_usuarios(session: SessionDep):

    return session.exec(select(Usuario)).all()


@router.get("/{id}", response_model=Usuario)
def get_usuario_by_id(id: int, session: SessionDep):

    usuario = session.get(Usuario, id)

    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")

    return usuario


@router.post("/", response_model=Usuario)
def create_usuario(usuario: Usuario, session: SessionDep):

    existente = session.exec(
        select(Usuario).where(Usuario.email == usuario.email)
    ).first()

    if existente:
        raise HTTPException(400, "Email já cadastrado")

    usuario.id = None
    usuario.criado_em = datetime.now()
    usuario.senha_hash = hash_senha(usuario.senha_hash)

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


@router.delete("/{id}")
def delete_usuario(id: int, session: SessionDep):

    usuario = session.get(Usuario, id)

    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")

    session.delete(usuario)
    session.commit()


@router.put("/{id}")
def update_usuario(id: int, dados: Usuario, session: SessionDep):

    usuario = session.get(Usuario, id)

    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")

    if dados.nome:
        usuario.nome = dados.nome

    if dados.email:
        usuario.email = dados.email

    if dados.senha_hash:
        usuario.senha_hash = hash_senha(dados.senha_hash)

    session.commit()
    session.refresh(usuario)

    return usuario