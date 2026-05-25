from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database.database import get_session
from models.models import Avaliacao


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/avaliacoes",
    tags=["avaliacoes"]
)


@router.post("/", response_model=Avaliacao)
def criar_avaliacao(
    avaliacao: Avaliacao,
    session: SessionDep
):

    avaliacao.id = None
    avaliacao.criado_em = datetime.now()

    session.add(avaliacao)
    session.commit()
    session.refresh(avaliacao)

    return avaliacao


@router.get("/", response_model=list[Avaliacao])
def listar_avaliacoes(session: SessionDep):

    return session.exec(
        select(Avaliacao)
    ).all()


@router.get("/{avaliacao_id}", response_model=Avaliacao)
def buscar_avaliacao(
    avaliacao_id: int,
    session: SessionDep
):

    avaliacao = session.get(
        Avaliacao,
        avaliacao_id
    )

    if not avaliacao:
        raise HTTPException(
            404,
            "Avaliação não encontrada"
        )

    return avaliacao


@router.put("/{avaliacao_id}", response_model=Avaliacao)
def atualizar_avaliacao(
    avaliacao_id: int,
    dados: Avaliacao,
    session: SessionDep
):

    avaliacao = session.get(
        Avaliacao,
        avaliacao_id
    )

    if not avaliacao:
        raise HTTPException(
            404,
            "Avaliação não encontrada"
        )

    avaliacao.nota = dados.nota
    avaliacao.comentario = dados.comentario

    session.commit()
    session.refresh(avaliacao)

    return avaliacao


@router.delete("/{avaliacao_id}")
def deletar_avaliacao(
    avaliacao_id: int,
    session: SessionDep
):

    avaliacao = session.get(
        Avaliacao,
        avaliacao_id
    )

    if not avaliacao:
        raise HTTPException(
            404,
            "Avaliação não encontrada"
        )

    session.delete(avaliacao)
    session.commit()

    return {"ok": True}