import asyncio
import os

import httpx

APIKEY = os.environ.get("APIKEY", "5734143a-595d-405d-9c97-6c198537108f")


async def recupera_produto(codigo):
    print(f"Recuperando produto de código {codigo}")
    try:
        async with httpx.AsyncClient() as cliente:
            resposta = await cliente.get(
                f"http://localhost:8080/catalogs/{codigo}",
                headers={"X-API-KEY": APIKEY},
            )
            resposta.raise_for_status()
            print(resposta.json())
    except httpx.HTTPStatusError as e:
        print(f"Erro ao recuperar produto de código {codigo}: {e}")


async def main():
    codigo_produtos = [
        "155568600",
        "jj2a97g940",
        "cb9a1801k9",
        "224722100",
        "702915400",
    ] * 20
    await asyncio.gather(
        *(recupera_produto(codigo) for codigo in codigo_produtos),
    )


asyncio.run(main())
