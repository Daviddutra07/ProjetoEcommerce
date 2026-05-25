from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database.database import get_session
from models.models import Pagamento


SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/pagamentos",
    tags=["pagamentos"]
)


@router.post("/", response_model=Pagamento)
def criar_pagamento(
    pagamento: Pagamento,
    session: SessionDep
):

    pagamento.id = None

    session.add(pagamento)
    session.commit()
    session.refresh(pagamento)

    return pagamento


@router.get("/", response_model=list[Pagamento])
def listar_pagamentos(session: SessionDep):

    return session.exec(
        select(Pagamento)
    ).all()


@router.get("/{pagamento_id}", response_model=Pagamento)
def buscar_pagamento(
    pagamento_id: int,
    session: SessionDep
):

    pagamento = session.get(
        Pagamento,
        pagamento_id
    )

    if not pagamento:
        raise HTTPException(
            404,
            "Pagamento não encontrado"
        )

    return pagamento


@router.put("/{pagamento_id}", response_model=Pagamento)
def atualizar_pagamento(
    pagamento_id: int,
    dados: Pagamento,
    session: SessionDep
):

    pagamento = session.get(
        Pagamento,
        pagamento_id
    )

    if not pagamento:
        raise HTTPException(
            404,
            "Pagamento não encontrado"
        )

    pagamento.valor = dados.valor
    pagamento.metodo = dados.metodo
    pagamento.status = dados.status
    pagamento.pago_em = dados.pago_em

    session.commit()
    session.refresh(pagamento)

    return pagamento


@router.delete("/{pagamento_id}")
def deletar_pagamento(
    pagamento_id: int,
    session: SessionDep
):

    pagamento = session.get(
        Pagamento,
        pagamento_id
    )

    if not pagamento:
        raise HTTPException(
            404,
            "Pagamento não encontrado"
        )

    session.delete(pagamento)
    session.commit()

    return {"ok": True}