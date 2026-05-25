from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database.database import get_session
from models.models import Endereco


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/enderecos",
    tags=["enderecos"]
)


@router.post("/", response_model=Endereco)
def criar_endereco(
    endereco: Endereco,
    session: SessionDep
):

    endereco.id = None

    session.add(endereco)
    session.commit()
    session.refresh(endereco)

    return endereco


@router.get("/", response_model=list[Endereco])
def listar_enderecos(session: SessionDep):

    return session.exec(
        select(Endereco)
    ).all()


@router.get("/{endereco_id}", response_model=Endereco)
def buscar_endereco(
    endereco_id: int,
    session: SessionDep
):

    endereco = session.get(
        Endereco,
        endereco_id
    )

    if not endereco:
        raise HTTPException(
            404,
            "Endereço não encontrado"
        )

    return endereco


@router.put("/{endereco_id}", response_model=Endereco)
def atualizar_endereco(
    endereco_id: int,
    dados: Endereco,
    session: SessionDep
):

    endereco = session.get(
        Endereco,
        endereco_id
    )

    if not endereco:
        raise HTTPException(
            404,
            "Endereço não encontrado"
        )

    endereco.rua = dados.rua
    endereco.cidade = dados.cidade
    endereco.estado = dados.estado
    endereco.cep = dados.cep

    session.commit()
    session.refresh(endereco)

    return endereco


@router.delete("/{endereco_id}")
def deletar_endereco(
    endereco_id: int,
    session: SessionDep
):

    endereco = session.get(
        Endereco,
        endereco_id
    )

    if not endereco:
        raise HTTPException(
            404,
            "Endereço não encontrado"
        )

    session.delete(endereco)
    session.commit()

    return {"ok": True}