import asyncio
import os

import httpx
from aiocache import Cache
from lasier.adapters.caches import AiocacheAdapter
from lasier.circuit_breaker.asyncio import circuit_breaker
from lasier.circuit_breaker.rules import PercentageFailuresRule

APIKEY = os.environ.get("APIKEY", "5734143a-595d-405d-9c97-6c198537108f")


# A regra é: Caso a função tenha sido chamada mais de 10 vezes, com 50% de erro
rule = PercentageFailuresRule(
    # Numero escolhido para facilitar
    # a visualização da solução do problema
    max_failures_percentage=50,
    failure_cache_key="my_cb",
    min_accepted_requests=10,
    request_cache_key="my_cb_request",
)

# cache em memória
cache = AiocacheAdapter(Cache(Cache.MEMORY))


# Exceção lançada quando o circuito está aberto
class OpenCircuitError(Exception):
    pass


async def recupera_produto2(codigo):
    print(f"Recuperando produto de código {codigo}")
    try:
        async with (
            circuit_breaker(
                rule,
                cache,
                failure_exception=OpenCircuitError,
                catch_exceptions=(httpx.HTTPStatusError,),
            ),
            httpx.AsyncClient() as cliente,
        ):
            resposta = await cliente.get(
                f"http://localhost:8080/catalogs/{codigo}",
                headers={"X-API-KEY": APIKEY},
            )
            resposta.raise_for_status()
            print(resposta.json())
    except httpx.HTTPStatusError as e:
        print(f"Erro ao recuperar produto de código {codigo}: {e!r}")
    except OpenCircuitError as e:
        # outras ações poderiam ser tomadas aqui
        print(f"Erro ao recuperar produto de código {codigo}: {e!r}")


async def main():
    codigo_produtos = [
        "155568600",
        "jj2a97g940",
        "cb9a1801k9",
        "224722100",
        "702915400",
    ] * 4

    # simulação de várias requisições simultâneas
    await asyncio.gather(
        *(recupera_produto2(codigo) for codigo in codigo_produtos),
    )


asyncio.run(main())
