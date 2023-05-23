import asyncio

import httpx


async def recupera_itens(id_pacote, cliente):
    # simula a requisição para buscar os itens de um pacote
    await cliente.get("https://httpbin.org/delay/1")
    print(f"Os itens do pacote {id_pacote} foram recuperados.")


async def main():
    async with httpx.AsyncClient() as cliente:
        await cliente.get(
            "https://httpbin.org/delay/1"
        )  # simula a requisição de um pedido
        print("pedido recuperado")
        await asyncio.gather(
            *(recupera_itens(id_pacote, cliente) for id_pacote in range(10))
        )


asyncio.run(main())
