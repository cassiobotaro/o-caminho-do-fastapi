from http import HTTPStatus

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from api_pedidos.esquema import ErrorResponse, HealthCheckResponse, Item
from api_pedidos.excecao import (
    FalhaDeComunicacaoError,
    PedidoNaoEncontradoError,
)
from api_pedidos.magalu_api import recuperar_itens_por_pedido

app = FastAPI()


@app.exception_handler(PedidoNaoEncontradoError)
def tratar_erro_pedido_nao_encontrado(
    request: Request, exc: PedidoNaoEncontradoError
):
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={"message": "Pedido não encontrado"},
    )


@app.exception_handler(FalhaDeComunicacaoError)
def tratar_erro_falha_de_comunicacao(
    request: Request, exc: FalhaDeComunicacaoError
):
    return JSONResponse(
        status_code=HTTPStatus.BAD_GATEWAY,
        content={"message": "Falha de comunicação com o servidor remoto"},
    )


@app.get(
    "/healthcheck",
    tags=["healthcheck"],
    summary="Integridade do sistema",
    description="Checa se o servidor está online",
    response_model=HealthCheckResponse,
)
def healthcheck():
    return HealthCheckResponse(status="ok")


@app.get(
    "/orders/{identificacao_do_pedido}/items",
    responses={
        HTTPStatus.NOT_FOUND.value: {
            "description": "Pedido não encontrado",
            "model": ErrorResponse,
        },
        HTTPStatus.BAD_GATEWAY.value: {
            "description": "Falha de comunicação com o servidor remoto",
            "model": ErrorResponse,
        },
    },
    summary="Itens de um pedido",
    tags=["pedidos"],
    description="Retorna todos os itens de um determinado pedido",
    response_model=list[Item],
)
def listar_itens(itens: list[Item] = Depends(recuperar_itens_por_pedido)):
    return itens
