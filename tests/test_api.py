from http import HTTPStatus

import pytest
from api_pedidos.api import app, recuperar_itens_por_pedido
from fastapi.testclient import TestClient
from uuid import UUID
from api_pedidos.esquema import Item
from api_pedidos.excecao import PedidoNaoEncontradoError, FalhaDeComunicacaoError


@pytest.fixture
def cliente():
    return TestClient(app)


@pytest.fixture
def sobreescreve_recuperar_itens_por_pedido():
    def _sobreescreve_recuperar_itens_por_pedido(itens_ou_erro):
        def duble(identificacao_do_pedido: UUID) -> list[Item]:
            if isinstance(itens_ou_erro, Exception):
                raise itens_ou_erro
            return itens_ou_erro

        app.dependency_overrides[recuperar_itens_por_pedido] = duble

    yield _sobreescreve_recuperar_itens_por_pedido
    app.dependency_overrides.clear()


class TestHealthCheck:
    def test_devo_ter_como_retorno_codigo_de_status_200(self, cliente):
        resposta = cliente.get("/healthcheck")
        assert resposta.status_code == HTTPStatus.OK

    def test_formato_de_retorno_deve_ser_json(self, cliente):
        resposta = cliente.get("/healthcheck")
        assert resposta.headers["Content-Type"] == "application/json"

    def test_deve_conter_informacoes(self, cliente):
        resposta = cliente.get("/healthcheck")
        assert resposta.json() == {
            "status": "ok",
        }


class TestListarPedidos:
    def test_quando_identificacao_do_pedido_invalido_um_erro_deve_ser_retornado(
        self, cliente
    ):
        resposta = cliente.get("/orders/valor-invalido/items")
        assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_quando_pedido_nao_encontrado_um_erro_deve_ser_retornado(
        self, cliente, sobreescreve_recuperar_itens_por_pedido
    ):
        sobreescreve_recuperar_itens_por_pedido(PedidoNaoEncontradoError())
        resposta = cliente.get("/orders/ea78b59b-885d-4e7b-9cd0-d54acadb4933/items")
        assert resposta.status_code == HTTPStatus.NOT_FOUND

    def test_quando_encontrar_pedido_codigo_ok_deve_ser_retornado(
        self, cliente, sobreescreve_recuperar_itens_por_pedido
    ):
        sobreescreve_recuperar_itens_por_pedido([])
        resposta = cliente.get("/orders/7e290683-d67b-4f96-a940-44bef1f69d21/items")
        assert resposta.status_code == HTTPStatus.OK

    def test_quando_encontrar_pedido_deve_retornar_itens(
        self, cliente, sobreescreve_recuperar_itens_por_pedido
    ):
        itens = [
            Item(
                sku="1",
                description="Item 1",
                image_url="http://url.com/img1",
                reference="ref1",
                quantity=1,
            ),
            Item(
                sku="2",
                description="Item 2",
                image_url="http://url.com/img2",
                reference="ref2",
                quantity=2,
            ),
        ]
        sobreescreve_recuperar_itens_por_pedido(itens)
        resposta = cliente.get("/orders/7e290683-d67b-4f96-a940-44bef1f69d21/items")
        assert resposta.json() == itens

    def test_quando_fonte_de_pedidos_falha_um_erro_deve_ser_retornado(
        self, cliente, sobreescreve_recuperar_itens_por_pedido
    ):
        sobreescreve_recuperar_itens_por_pedido(FalhaDeComunicacaoError())
        resposta = cliente.get("/orders/ea78b59b-885d-4e7b-9cd0-d54acadb4933/items")
        assert resposta.status_code == HTTPStatus.BAD_GATEWAY
