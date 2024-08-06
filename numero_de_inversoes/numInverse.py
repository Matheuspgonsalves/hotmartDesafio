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

            # Receber e processar a resposta inicial
            response = await websocket.recv()
            print(f"Received message: \n{response}")

            # Enviar "start inversions"
            await websocket.send("start inversions")
            print("Sent message: start inversions")

            while True:
                response = await websocket.recv()
                print(f"Received message: \n{response}")

                # Verificar se a mensagem contém a sequência de números
                match = re.search(r'\[([0-9, ]+)\]', response)
                if match:
                    sequence_str = match.group(1)
                    try:
                        sequence = list(map(int, sequence_str.split(', ')))
                        print(f"Extracted sequence: {sequence}")

                        # Calcular o número de inversões
                        inversions = count_inversions(sequence)
                        print(f"Number of inversions: {inversions}")

                        # Enviar o número de inversões para o servidor
                        await websocket.send(str(inversions))
                        print(f"Sent message: {inversions}")

                    except ValueError as e:
                        print(f"Error converting sequence to integers: {e}")

                elif "start" in response or "echo" in response:
                    # Se a mensagem contiver comandos 'start' ou 'echo', continue
                    print("Received start or echo command. Continuing...")
                    continue

                elif "exit" in response or "stop" in response or "quit" in response:
                    # Se a mensagem contiver 'exit', 'stop', ou 'quit', encerre a conexão
                    print("Received termination command. Exiting...")
                    break

        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

def count_inversions(sequence):
    # Função para contar o número de inversões na sequência
    inversions = 0
    for i in range(len(sequence)):
        for j in range(i + 1, len(sequence)):
            if sequence[i] > sequence[j]:
                inversions += 1
    return inversions

# Executar a função assíncrona
asyncio.run(connect_to_websocket())
