"""API FastAPI para Loja de Pokémon TCG."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routers import cards, vendas

app = FastAPI(
    title="API Loja Pokémon TCG",
    description="API REST para gerenciar loja de Pokémon Trading Card Game",
    version="1.0.0",
)

app.include_router(cards.router)
app.include_router(vendas.router)


@app.get("/", tags=["root"])
def raiz():
    """Informações sobre a API."""
    return {
        "mensagem": "Bem-vindo à API Loja Pokémon TCG",
        "versao": "1.0.0",
        "documentacao": "/docs",
        "endpoints": {"cards": "/cards", "vendas": "/vendas"}
    }


@app.get("/saude", tags=["root"])
def verificar_saude():
    """Health check."""
    return {"status": "operacional"}


@app.exception_handler(Exception)
async def manipulador_excecao_global(request, exc):
    """Manipulador global de exceções."""
    return JSONResponse(status_code=500, content={"detalhe": "Erro interno do servidor"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
