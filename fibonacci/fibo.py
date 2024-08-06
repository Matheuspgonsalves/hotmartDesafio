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

            # Enviar "start fibonacci" após receber a resposta
            await websocket.send("start fibonacci")
            print("Sent message: start fibonacci")

            while True:
                response = await websocket.recv()
                print(f"Received message: \n{response}")

                # Verificar se a mensagem contém a sequência de Fibonacci
                match = re.search(r'\[([0-9, ]+)\]', response)
                if match:
                    sequence_str = match.group(1)
                    # Converter a string da sequência em uma lista de inteiros
                    try:
                        sequence = list(map(int, sequence_str.split(', ')))
                        print(f"Extracted Fibonacci sequence: {sequence}")

                        # Calcular o próximo número na sequência
                        next_number = calculate_next_fibonacci(sequence)
                        print(f"Next Fibonacci number: {next_number}")

                        # Enviar o próximo número para o servidor
                        await websocket.send(str(next_number))
                        print(f"Sent message: {next_number}")

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

def calculate_next_fibonacci(sequence):
    # Assumir que a sequência está correta e calcular o próximo número
    if len(sequence) < 2:
        return None  # Sequência muito curta para determinar o próximo número
    return sequence[-1] + sequence[-2]

# Executar a função assíncrona
asyncio.run(connect_to_websocket())
