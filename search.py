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

            # Enviar "start search" após receber a resposta
            await websocket.send("start search")
            print("Sent message: start search")

            buffer = ""

            while True:
                # Receber a mensagem do servidor
                message = await websocket.recv()
                buffer += message
                print(f"Received message part: \n{message}")

                # Verificar se a mensagem acumulada contém as partes esperadas
                if "Array" in buffer and "Target" in buffer:
                    # Extrair o array e o número alvo da mensagem
                    target_match = re.search(r'Target: (\d+)', buffer)
                    array_match = re.search(r'Array: \[(.*?)\]', buffer)

                    if target_match and array_match:
                        target = int(target_match.group(1))
                        array = list(map(int, array_match.group(1).split(', ')))

                        print(f"Target: {target}")
                        print(f"Array: {array}")

                        # Encontrar o índice do número alvo no array
                        if target in array:
                            index = array.index(target)
                            print(f"Index of {target}: {index}")

                            # Enviar o índice encontrado para o servidor
                            await websocket.send(str(index))
                            print(f"Sent index: {index}")

                        else:
                            print(f"Target {target} not found in the array.")

                        # Limpar o buffer após processar a mensagem
                        buffer = ""

                    else:
                        print("Failed to extract target or array.")

                # Opcional: você pode querer processar outros tipos de mensagens ou comandos
                # conforme necessário. Adicione lógica aqui se necessário.

        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Executar a função assíncrona
asyncio.run(connect_to_websocket())