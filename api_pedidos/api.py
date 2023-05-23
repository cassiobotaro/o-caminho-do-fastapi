from http import HTTPStatus
from uuid import UUID

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from api_pedidos.esquema import Item
from api_pedidos.excecao import PedidoNaoEncontradoError

app = FastAPI()


def recuperar_itens_por_pedido(identificacao_do_pedido: UUID) -> list[Item]:
    pass


@app.exception_handler(PedidoNaoEncontradoError)
def tratar_erro_pedido_nao_encontrado(request: Request, exc: PedidoNaoEncontradoError):
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND, content={"message": "Pedido não encontrado"}
    )


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


@app.get("/orders/{identificacao_do_pedido}/items")
def listar_itens(itens: list[Item] = Depends(recuperar_itens_por_pedido)):
    return itens
