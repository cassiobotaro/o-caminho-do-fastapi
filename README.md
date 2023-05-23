# O caminho do FastAPI

🚀Aprenda a Construir APIs como um Verdadeiro Mandaloriano.

🛍️ O que será desenvolvido?
Será desenvolvido um sistema com objetivo de obter informações a respeito de pedidos.

Os pedidos serão obtidos através de integração com um sistema de pedidos externo.

Vamos fazer o enriquecimento desta informação antes de sua exibição e também iremos prover alguns dados estatísticos sobre o pedido.

Um pedido possui vários pacotes, cada um deles contendo itens.

Este sistema deve seguir as seguintes regras:

- Deve apresentar uma interface que possa ser consumida tanto por um website, quanto por um aplicativo para dispositivos móveis;

- Deve prover um endpoint que indique a saúde do sistema;

- Dado um pedido, retornar os seus itens;

- Os itens de um pedido devem conter um identificador (sku), uma descrição, uma imagem, uma referência e a quantidade;

- Exibir um relatório com o total de métodos de pagamento utilizados nos últimos 30 pedidos;

- Dado um pedido (vários itens), enriquecer a informação com as informações de gtin (global trade item number). Deve ser retornado também a marca, descrição e identificação do produto;

- Como será consumido por terceiros deve apresentar boa documentação;

- O sistema deve estar preparado para receber novas funcionalidades, garantindo qualidade a cada entrega;

- O sistema deve apresentar testes.
