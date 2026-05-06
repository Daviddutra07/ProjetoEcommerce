from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List


class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(index=False)
    email: str = Field(index=False)
    senha_hash: str = Field(index=False)
    criado_em: datetime = Field(default_factory=datetime.now)

    papeis: List["Papel"] = Relationship(
        back_populates="usuarios",
        link_model="UsuarioPapel"
    )

    pedidos: List["Pedido"] = Relationship(back_populates="usuario")
    enderecos: List["Endereco"] = Relationship(back_populates="usuario")
    avaliacoes: List["Avaliacao"] = Relationship(back_populates="usuario")


class Papel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(index=False)

    usuarios: List["Usuario"] = Relationship(
        back_populates="papeis",
        link_model="UsuarioPapel"
    )

class UsuarioPapel(SQLModel, table=True):
    usuario_id: int = Field(foreign_key="usuario.id", primary_key=True)
    papel_id: int = Field(foreign_key="papel.id", primary_key=True)

class Produto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(index=False)
    descricao: str = Field(index=False)
    preco: float = Field(index=False)
    criado_em: datetime = Field(default_factory=datetime.now)

    categorias: List["Categoria"] = Relationship(
        back_populates="produtos",
        link_model="ProdutoCategoria"
    )

    itens: List["ItemPedido"] = Relationship(back_populates="produto")
    avaliacoes: List["Avaliacao"] = Relationship(back_populates="produto")
    estoque: Optional["Estoque"] = Relationship(back_populates="produto")


class Categoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(index=False)

    produtos: List["Produto"] = Relationship(
        back_populates="categorias",
        link_model="ProdutoCategoria"
    )

class ProdutoCategoria(SQLModel, table=True):
    produto_id: int = Field(foreign_key="produto.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categoria.id", primary_key=True)


class Pedido(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    total: float = Field(index=False)
    status: str = Field(index=False)
    criado_em: datetime = Field(default_factory=datetime.now)

    usuario: Optional["Usuario"] = Relationship(back_populates="pedidos")
    itens: List["ItemPedido"] = Relationship(back_populates="pedido")
    pagamentos: List["Pagamento"] = Relationship(back_populates="pedido")


class ItemPedido(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedido.id")
    produto_id: int = Field(foreign_key="produto.id")
    quantidade: int = Field(index=False)
    preco: float = Field(index=False)

    pedido: Optional["Pedido"] = Relationship(back_populates="itens")
    produto: Optional["Produto"] = Relationship(back_populates="itens")


class Pagamento(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedido.id")
    valor: float = Field(index=False)
    metodo: str = Field(index=False)
    status: str = Field(index=False)
    pago_em: Optional[datetime] = None

    pedido: Optional["Pedido"] = Relationship(back_populates="pagamentos")


class Endereco(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    rua: str
    cidade: str
    estado: str
    cep: str

    usuario: Optional["Usuario"] = Relationship(back_populates="enderecos")

class Avaliacao(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    produto_id: int = Field(foreign_key="produto.id")
    nota: int
    comentario: str
    criado_em: datetime = Field(default_factory=datetime.now)

    usuario: Optional["Usuario"] = Relationship(back_populates="avaliacoes")
    produto: Optional["Produto"] = Relationship(back_populates="avaliacoes")


class Estoque(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    produto_id: int = Field(foreign_key="produto.id", unique=True)
    quantidade: int
    atualizado_em: datetime = Field(default_factory=datetime.now)

    produto: Optional["Produto"] = Relationship(back_populates="estoque")