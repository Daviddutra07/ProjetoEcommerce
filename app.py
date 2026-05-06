from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from database import create_db, get_session
from sqlmodel import SQLModel, Session, select
from typing import List, Annotated
import hashlib

from models import Avaliacao, Categoria, Endereco, Estoque, ItemPedido, Pagamento, Pedido, Produto, Usuario, Papel  

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield

app = FastAPI(lifespan=lifespan)

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

# USUÁRIOS

@app.post("/usuarios")
def criar_usuario(usuario: Usuario, session: SessionDep):
    existente = session.exec(
        select(Usuario).where(Usuario.email == usuario.email)
    ).first()

    if existente:
        raise HTTPException(400, "Email já cadastrado")

    usuario.senha_hash = hash_senha(usuario.senha_hash)
    usuario.id = None
    usuario.criado_em = datetime.now()

    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@app.get("/usuarios", response_model=List[Usuario])
def listar_usuarios(session: SessionDep):
    return session.exec(select(Usuario)).all()

@app.get("/usuarios/{usuario_id}")
def buscar_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")

    return usuario

@app.put("/usuarios/{usuario_id}")
def atualizar_usuario(usuario_id: int, dados: Usuario, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)

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


@app.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")

    session.delete(usuario)
    session.commit()
    return {"ok": True}

# PAPÉIS

@app.post("/papeis")
def criar_papel(papel: Papel, session: SessionDep):
    papel.id = None
    session.add(papel)
    session.commit()
    session.refresh(papel)
    return papel


@app.get("/papeis", response_model=List[Papel])
def listar_papeis(session: SessionDep):
    return session.exec(select(Papel)).all()


@app.get("/papeis/{papel_id}")
def buscar_papel(papel_id: int, session: SessionDep):
    papel = session.get(Papel, papel_id)

    if not papel:
        raise HTTPException(404, "Papel não encontrado")

    return papel


@app.delete("/papeis/{papel_id}")
def deletar_papel(papel_id: int, session: SessionDep):
    papel = session.get(Papel, papel_id)

    if not papel:
        raise HTTPException(404, "Papel não encontrado")

    session.delete(papel)
    session.commit()
    return {"ok": True}


@app.post("/usuarios/{usuario_id}/papeis/{papel_id}")
def adicionar_papel(usuario_id: int, papel_id: int, session: SessionDep):
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
def listar_papeis_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")

    return usuario.papeis

# PRODUTOS

@app.post("/produtos")
def criar_produto(produto: Produto, session: SessionDep):
    produto.id = None
    produto.criado_em = datetime.now()

    session.add(produto)
    session.commit()
    session.refresh(produto)
    return produto

@app.get("/produtos", response_model=List[Produto])
def listar_produtos(session: SessionDep):
    return session.exec(select(Produto)).all()

@app.get("/produtos/{produto_id}")
def buscar_produto(produto_id: int, session: SessionDep):
    produto = session.get(Produto, produto_id)

    if not produto:
        raise HTTPException(404, "Usuário não encontrado")

    return produto

@app.put("/produtos/{produto_id}")
def atualizar_produto(produto_id: int, dados: Produto, session: SessionDep):
    produto = session.get(Produto, produto_id)

    if not produto:
        raise HTTPException(404, "Usuário não encontrado")

    produto.nome = dados.nome
    produto.descricao = dados.descricao
    produto.preco = dados.preco

    session.commit()
    session.refresh(produto)
    return produto


@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int, session: SessionDep):
    produto = session.get(Produto, produto_id)

    if not produto:
        raise HTTPException(404, "Usuário não encontrado")

    session.delete(produto)
    session.commit()
    return {"ok": True}

# Categorias

@app.post("/categorias")
def criar_categoria(categoria: Categoria, session: SessionDep):
    categoria.id = None
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


@app.get("/categorias")
def listar_categorias(session: SessionDep):
    return session.exec(select(Categoria)).all()


@app.delete("/categorias/{categoria_id}")
def deletar_categoria(categoria_id: int, session: SessionDep):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(404, "Categoria não encontrada")

    session.delete(categoria)
    session.commit()
    return {"ok": True}

# PEDIDOS

@app.post("/pedidos")
def criar_pedido(pedido: Pedido, session: SessionDep):
    pedido.id = None
    pedido.criado_em = datetime.now()
    session.add(pedido)
    session.commit()
    session.refresh(pedido)
    return pedido


@app.get("/pedidos")
def listar_pedidos(session: SessionDep):
    return session.exec(select(Pedido)).all()


@app.get("/pedidos/{pedido_id}")
def buscar_pedido(pedido_id: int, session: SessionDep):
    pedido = session.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(404, "Pedido não encontrado")
    return pedido


@app.delete("/pedidos/{pedido_id}")
def deletar_pedido(pedido_id: int, session: SessionDep):
    pedido = session.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(404, "Pedido não encontrado")

    session.delete(pedido)
    session.commit()
    return {"ok": True}

# PAGAMENTOS

@app.post("/pagamentos")
def criar_pagamento(pagamento: Pagamento, session: SessionDep):
    pagamento.id = None
    session.add(pagamento)
    session.commit()
    session.refresh(pagamento)
    return pagamento


@app.get("/pagamentos")
def listar_pagamentos(session: SessionDep):
    return session.exec(select(Pagamento)).all()

@app.get("/pagamentos/{pagamento_id}")
def buscar_pagamento(pagamento_id: int, session: SessionDep):
    pagamento = session.get(Pagamento, pagamento_id)
    if not pagamento:
        raise HTTPException(404, "Pagamento não encontrado")
    return pagamento


@app.put("/pagamentos/{pagamento_id}")
def atualizar_pagamento(pagamento_id: int, dados: Pagamento, session: SessionDep):
    pagamento = session.get(Pagamento, pagamento_id)

    if not pagamento:
        raise HTTPException(404, "Pagamento não encontrado")

    pagamento.valor = dados.valor
    pagamento.metodo = dados.metodo
    pagamento.status = dados.status
    pagamento.pago_em = dados.pago_em

    session.commit()
    session.refresh(pagamento)
    return pagamento


@app.delete("/pagamentos/{pagamento_id}")
def deletar_pagamento(pagamento_id: int, session: SessionDep):
    pagamento = session.get(Pagamento, pagamento_id)

    if not pagamento:
        raise HTTPException(404, "Pagamento não encontrado")

    session.delete(pagamento)
    session.commit()
    return {"ok": True}

# ENDEREÇOS

@app.post("/enderecos")
def criar_endereco(endereco: Endereco, session: SessionDep):
    endereco.id = None
    session.add(endereco)
    session.commit()
    session.refresh(endereco)
    return endereco


@app.get("/enderecos")
def listar_enderecos(session: SessionDep):
    return session.exec(select(Endereco)).all()

@app.get("/enderecos/{endereco_id}")
def buscar_endereco(endereco_id: int, session: SessionDep):
    endereco = session.get(Endereco, endereco_id)

    if not endereco:
        raise HTTPException(404, "Endereço não encontrado")

    return endereco


@app.put("/enderecos/{endereco_id}")
def atualizar_endereco(endereco_id: int, dados: Endereco, session: SessionDep):
    endereco = session.get(Endereco, endereco_id)

    if not endereco:
        raise HTTPException(404, "Endereço não encontrado")

    endereco.rua = dados.rua
    endereco.cidade = dados.cidade
    endereco.estado = dados.estado
    endereco.cep = dados.cep

    session.commit()
    session.refresh(endereco)
    return endereco


@app.delete("/enderecos/{endereco_id}")
def deletar_endereco(endereco_id: int, session: SessionDep):
    endereco = session.get(Endereco, endereco_id)

    if not endereco:
        raise HTTPException(404, "Endereço não encontrado")

    session.delete(endereco)
    session.commit()
    return {"ok": True}

# AVALIAÇÕES

@app.post("/avaliacoes")
def criar_avaliacao(avaliacao: Avaliacao, session: SessionDep):
    avaliacao.id = None
    avaliacao.criado_em = datetime.now()
    session.add(avaliacao)
    session.commit()
    session.refresh(avaliacao)
    return avaliacao


@app.get("/avaliacoes")
def listar_avaliacoes(session: SessionDep):
    return session.exec(select(Avaliacao)).all()

@app.get("/avaliacoes/{avaliacao_id}")
def buscar_avaliacao(avaliacao_id: int, session: SessionDep):
    avaliacao = session.get(Avaliacao, avaliacao_id)

    if not avaliacao:
        raise HTTPException(404, "Avaliação não encontrada")

    return avaliacao


@app.put("/avaliacoes/{avaliacao_id}")
def atualizar_avaliacao(avaliacao_id: int, dados: Avaliacao, session: SessionDep):
    avaliacao = session.get(Avaliacao, avaliacao_id)

    if not avaliacao:
        raise HTTPException(404, "Avaliação não encontrada")

    avaliacao.nota = dados.nota
    avaliacao.comentario = dados.comentario

    session.commit()
    session.refresh(avaliacao)
    return avaliacao


@app.delete("/avaliacoes/{avaliacao_id}")
def deletar_avaliacao(avaliacao_id: int, session: SessionDep):
    avaliacao = session.get(Avaliacao, avaliacao_id)

    if not avaliacao:
        raise HTTPException(404, "Avaliação não encontrada")

    session.delete(avaliacao)
    session.commit()
    return {"ok": True}

# ESTOQUE

@app.post("/estoque")
def criar_estoque(estoque: Estoque, session: SessionDep):
    estoque.id = None
    estoque.atualizado_em = datetime.now()
    session.add(estoque)
    session.commit()
    session.refresh(estoque)
    return estoque


@app.get("/estoque")
def listar_estoque(session: SessionDep):
    return session.exec(select(Estoque)).all()

@app.get("/estoque/{estoque_id}")
def buscar_estoque(estoque_id: int, session: SessionDep):
    estoque = session.get(Estoque, estoque_id)

    if not estoque:
        raise HTTPException(404, "Estoque não encontrado")

    return estoque


@app.put("/estoque/{estoque_id}")
def atualizar_estoque(estoque_id: int, dados: Estoque, session: SessionDep):
    estoque = session.get(Estoque, estoque_id)

    if not estoque:
        raise HTTPException(404, "Estoque não encontrado")

    estoque.quantidade = dados.quantidade
    estoque.atualizado_em = datetime.now()

    session.commit()
    session.refresh(estoque)
    return estoque


@app.delete("/estoque/{estoque_id}")
def deletar_estoque(estoque_id: int, session: SessionDep):
    estoque = session.get(Estoque, estoque_id)

    if not estoque:
        raise HTTPException(404, "Estoque não encontrado")

    session.delete(estoque)
    session.commit()
    return {"ok": True}

# ITEM DO PEDIDO

@app.post("/itens-pedido")
def criar_item(item: ItemPedido, session: SessionDep):
    item.id = None

    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.get("/itens-pedido")
def listar_itens(session: SessionDep):
    return session.exec(select(ItemPedido)).all()

@app.get("/itens-pedido/{item_id}")
def buscar_item(item_id: int, session: SessionDep):
    item = session.get(ItemPedido, item_id)

    if not item:
        raise HTTPException(404, "Item não encontrado")

    return item

@app.put("/itens-pedido/{item_id}")
def atualizar_item(item_id: int, dados: ItemPedido, session: SessionDep):
    item = session.get(ItemPedido, item_id)

    if not item:
        raise HTTPException(404, "Item não encontrado")

    item.quantidade = dados.quantidade
    item.preco = dados.preco

    session.commit()
    session.refresh(item)
    return item

@app.delete("/itens-pedido/{item_id}")
def deletar_item(item_id: int, session: SessionDep):
    item = session.get(ItemPedido, item_id)

    if not item:
        raise HTTPException(404, "Item não encontrado")

    session.delete(item)
    session.commit()
    return {"ok": True}

@app.get("/pedidos/{pedido_id}/itens")
def listar_itens_pedido(pedido_id: int, session: SessionDep):
    pedido = session.get(Pedido, pedido_id)

    if not pedido:
        raise HTTPException(404, "Pedido não encontrado")

    return pedido.itens