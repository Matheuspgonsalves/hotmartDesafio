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

            # Enviar "start behappy" após receber a resposta
            await websocket.send("start behappy")
            print("Sent message: start behappy")

            while True:
                # Receber a mensagem contendo o número
                response = await websocket.recv()
                print(f"Received message: \n{response}")

                if "Number" in response:
                    # Extrair o número da mensagem
                    match = re.search(r'Number: (\d+)', response)
                    if match:
                        number = int(match.group(1))
                        print(f"Received number: {number}")

                        # Determinar se o número é feliz
                        resultado = "Feliz" if is_happy(number) else "Infeliz"
                        print(f"Result: {resultado}")

                        # Enviar o resultado para o servidor
                        await websocket.send(resultado)
                        print(f"Sent message: {resultado}")

        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

def is_happy(n):
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(char) ** 2 for char in str(n))
    return n == 1

# Executar a função assíncrona
asyncio.run(connect_to_websocket())