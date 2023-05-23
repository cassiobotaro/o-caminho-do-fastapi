import httpx

httpx.get("https://httpbin.org/delay/1")  # simula a requisição de um pedido
print("pedido recuperado")
for pacote in range(10):  # simula o a iteração sobre os pacotes
    # simula a requisição para buscar os itens de um pacote
    httpx.get("https://httpbin.org/delay/1")
    print(f"Os itens do pacote {pacote} foram recuperados.")
