from contextlib import asynccontextmanager
from fastapi import FastAPI

from database.database import create_db

from routes import (
    usuario_routes,
    papel_routes,
    produtos_routes,
    categoria_routes,
    pedido_routes,
    pagamento_routes,
    endereco_routes,
    avaliacao_routes,
    estoque_routes,
    item_pedido_routes,
    produto_categoria_routes
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(usuario_routes.router)
app.include_router(papel_routes.router)
app.include_router(produtos_routes.router)
app.include_router(categoria_routes.router)
app.include_router(produto_categoria_routes.router)
app.include_router(pedido_routes.router)
app.include_router(pagamento_routes.router)
app.include_router(endereco_routes.router)
app.include_router(avaliacao_routes.router)
app.include_router(estoque_routes.router)
app.include_router(item_pedido_routes.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )