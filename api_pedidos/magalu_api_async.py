import asyncio
import os
from http import HTTPStatus
from itertools import chain
from uuid import UUID

import httpx

from api_pedidos.esquema import Item
from api_pedidos.excecao import (
    FalhaDeComunicacaoError,
    PedidoNaoEncontradoError,
)

# tenant e apikey fixos somente para demonstrações
APIKEY = os.environ.get("APIKEY", "5734143a-595d-405d-9c97-6c198537108f")
TENANT_ID = os.environ.get("TENANT_ID", "21fea73c-e244-497a-8540-be0d3c583596")
MAGALU_API_URL = "http://127.0.0.1:8080"
MAESTRO_SERVICE_URL = f"{MAGALU_API_URL}/maestro/v1"


async def _recupera_itens_por_pacote(cliente, uuid_do_pedido, uuid_do_pacote):
    response = await cliente.get(
        f"{MAESTRO_SERVICE_URL}"
        f"/orders/{uuid_do_pedido}/packages/{uuid_do_pacote}/items",
        headers={"X-Api-Key": APIKEY, "X-Tenant-Id": TENANT_ID},
    )
    response.raise_for_status()
    return [
        Item(
            sku=item["product"]["code"],
            description=item["product"].get("description", ""),
            image_url=item["product"].get("image_url", ""),
            reference=item["product"].get("reference", ""),
            quantity=item["quantity"],
        )
        for item in response.json()
    ]


async def recuperar_itens_por_pedido(
    identificacao_do_pedido: UUID,
) -> list[Item]:
    async with httpx.AsyncClient() as cliente:
        try:
            response = await cliente.get(
                f"{MAESTRO_SERVICE_URL}/orders/{identificacao_do_pedido}",
                headers={"X-Api-Key": APIKEY, "X-Tenant-Id": TENANT_ID},
            )
            response.raise_for_status()
            pacotes = response.json()["packages"]
            itens = await asyncio.gather(
                *(
                    _recupera_itens_por_pacote(
                        cliente, identificacao_do_pedido, pacote["uuid"]
                    )
                    for pacote in pacotes
                )
            )
            # truque para unir as listas em uma única lista
            return list(chain.from_iterable(itens))
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == HTTPStatus.NOT_FOUND:
                raise PedidoNaoEncontradoError() from exc
            raise exc
        except httpx.HTTPError as exc:
            # aqui poderiam ser tratados outros erros como autenticação
            raise FalhaDeComunicacaoError() from exc
