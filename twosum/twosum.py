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

            # Enviar "start twosum" após receber a resposta
            await websocket.send("start twosum")
            print("Sent message: start twosum")

            while True:
                # Receber a mensagem contendo o array e o valor alvo
                response = await websocket.recv()
                print(f"Received message: \n{response}")

                # Checar se a mensagem contém comandos ou dados
                if "start" in response:
                    # Se a mensagem contiver um comando 'start {challenge}', continue
                    match = re.search(r'start \{challenge\}', response)
                    if match:
                        print("Received challenge start command.")
                        # Aqui você pode implementar lógica adicional para processar o desafio
                        continue

                elif "echo" in response:
                    # Se a mensagem contiver 'echo', envie 'start twosum'
                    await websocket.send("start twosum")
                    print("Sent message: start twosum")
                
                elif "exit" in response or "stop" in response or "quit" in response:
                    # Se a mensagem contiver 'exit', 'stop', ou 'quit', encerre a conexão
                    print("Received termination command. Exiting...")
                    break

                else:
                    # Extrair o array e o valor alvo se não for um comando
                    match = re.search(r'\[([^\]]+)\] Target: (\d+)', response)
                    if match:
                        array_str = match.group(1)
                        target = int(match.group(2))

                        # Converter a string do array em uma lista de inteiros
                        array = list(map(int, array_str.split(', ')))
                        print(f"Extracted array: {array}")
                        print(f"Target value: {target}")

                        # Encontrar o par de números cuja soma é igual ao valor alvo
                        result = find_pair_with_sum(array, target)
                        print(f"Resulting pair: {result}")

                        # Enviar a resposta com o par encontrado
                        if result:
                            await websocket.send(str(result))
                            print(f"Sent message: {result}")
                        else:
                            await websocket.send("[]")
                            print("Sent message: []")

        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

def find_pair_with_sum(array, target):
    seen = set()
    for num in array:
        complement = target - num
        if complement in seen:
            return [complement, num]
        seen.add(num)
    return []

# Executar a função assíncrona
asyncio.run(connect_to_websocket())
