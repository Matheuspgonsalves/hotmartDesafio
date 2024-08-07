import asyncio
import websockets
import re

async def connect_to_websocket():
    uri = "wss://ctf-challenges.devops.hotmart.com/echo"
    async with websockets.connect(uri) as websocket:
        try:
            # Enviar a mensagem inicial "echo"
            await websocket.send("echo")
            print("Sent message: echo")

            # Receber e processar a resposta
            response = await websocket.recv()
            print(f"Received message: \n{response}")

            # Enviar "start organizer" após receber a resposta
            await websocket.send("start organizer")
            print("Sent message: start organizer")

            while True:
                # Receber a mensagem contendo a lista de inteiros
                response = await websocket.recv()
                print(f"Received message: \n{response}")

                if "Lista" in response:
                    # Extrair a lista da mensagem
                    match = re.search(r'\[([^\]]+)\]', response)
                    if match:
                        lista_str = match.group(1)
                        lista = list(map(int, lista_str.split(', ')))
                        print(f"Received list: {lista}")

                        # Reorganizar a lista: pares antes dos ímpares
                        nova_lista = reorganizar_lista(lista)
                        print(f"Reorganized list: {nova_lista}")

                        # Enviar a nova lista para o servidor
                        await websocket.send(str(nova_lista))
                        print(f"Sent message: {nova_lista}")

        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

def reorganizar_lista(lista):
    pares = [num for num in lista if num % 2 == 0]
    impares = [num for num in lista if num % 2 != 0]
    return pares + impares

# Executar a função assíncrona
asyncio.run(connect_to_websocket())