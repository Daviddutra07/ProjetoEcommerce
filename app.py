from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, create_engine, select
from typing import List
import hashlib

from models import Usuario, Papel  

DATABASE_URL = "sqlite:///database.db"  
engine = create_engine(DATABASE_URL, echo=True)

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

@app.post("/usuarios")
def criar_usuario(nome: str, email: str, senha: str, session: Session = Depends(get_session)):
    existente = session.exec(
        select(Usuario).where(Usuario.email == email)
    ).first()

    if existente:
        raise HTTPException(400, "Email já cadastrado")

    usuario = Usuario(
        nome=nome,
        email=email,
        senha_hash=hash_senha(senha)
    )

    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@app.get("/usuarios", response_model=List[Usuario])
def listar_usuarios(session: Session = Depends(get_session)):
    return session.exec(select(Usuario)).all()


@app.get("/usuarios/{usuario_id}")
def buscar_usuario(usuario_id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")

    return usuario

@app.put("/usuarios/{usuario_id}")
def atualizar_usuario(usuario_id: int, nome: str, email: str, senha: str, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")

    usuario.nome = nome
    usuario.email = email
    usuario.senha_hash = hash_senha(senha)

    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@app.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")

    session.delete(usuario)
    session.commit()
    return {"ok": True}


@app.post("/papeis")
def criar_papel(nome: str, session: Session = Depends(get_session)):
    papel = Papel(nome=nome)

    session.add(papel)
    session.commit()
    session.refresh(papel)
    return papel


@app.get("/papeis", response_model=List[Papel])
def listar_papeis(session: Session = Depends(get_session)):
    return session.exec(select(Papel)).all()


@app.get("/papeis/{papel_id}")
def buscar_papel(papel_id: int, session: Session = Depends(get_session)):
    papel = session.get(Papel, papel_id)

    if not papel:
        raise HTTPException(404, "Papel não encontrado")

    return papel


@app.delete("/papeis/{papel_id}")
def deletar_papel(papel_id: int, session: Session = Depends(get_session)):
    papel = session.get(Papel, papel_id)

    if not papel:
        raise HTTPException(404, "Papel não encontrado")

    session.delete(papel)
    session.commit()
    return {"ok": True}


@app.post("/usuarios/{usuario_id}/papeis/{papel_id}")
def adicionar_papel(usuario_id: int, papel_id: int, session: Session = Depends(get_session)):
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

@app.get("/usuarios/{usuario_id}/papeis")
def listar_papeis_usuario(usuario_id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")

    return usuario.papeis