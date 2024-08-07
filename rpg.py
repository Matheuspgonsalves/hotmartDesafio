import asyncio
import websockets
import re
import json
from itertools import combinations

async def connect_to_websocket():
    uri = "wss://ctf-challenges.devops.hotmart.com/echo"
    async with websockets.connect(uri) as websocket:
        try:
            # Enviar a mensagem inicial "echo"
            await websocket.send("echo")
            print("Sent message: echo")

            # Receber e processar a resposta inicial
            response = await websocket.recv()
            print(f"Received initial message: \n{response}")

            # Enviar "start rpg" após receber a resposta
            await websocket.send("start rpg")
            print("Sent message: start rpg")

            while True:
                # Receber a mensagem do servidor
                response = await websocket.recv()
                print(f"Received message: \n{response}")

                if "Hérois" in response and "Habilidade" in response:
                    # Extrair o array de heróis e o valor da habilidade
                    hero_match = re.search(r'Hérois: \[(.*?)\]', response)
                    skill_match = re.search(r'Habilidade: (\d+)', response)

                    if hero_match and skill_match:
                        heroes = list(map(int, hero_match.group(1).split(', ')))
                        target_skill = int(skill_match.group(1))

                        print(f"Heroes: {heroes}")
                        print(f"Target Skill: {target_skill}")

                        # Encontrar o trio de heróis que somam a habilidade alvo
                        found = False
                        for comb in combinations(range(len(heroes)), 3):
                            i, j, k = comb
                            if heroes[i] + heroes[j] + heroes[k] == target_skill:
                                indices = [i, j, k]
                                print(f"Found indices: {indices} with sum {heroes[i] + heroes[j] + heroes[k]}")

                                # Enviar os índices diretamente como array de inteiros
                                indices_str = json.dumps(indices)
                                await websocket.send(indices_str)
                                print(f"Sent indices: {indices}")
                                found = True
                                break

                        if not found:
                            print("No valid trio found.")
                            # Se não encontrar um trio, envie uma mensagem padrão ou um aviso
                            # await websocket.send("No valid trio found")  # Dependendo da política do servidor

                    else:
                        print("Failed to extract heroes or skill.")

                elif "Informe o ID dos hérois:" in response:
                    print("Prompt received, processing...")
                    # Enviar uma mensagem padrão ou uma resposta vazia após o prompt
                    # await websocket.send("No valid trio found")  # Exemplo de mensagem padrão

                else:
                    print("Unexpected message received.")

        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Executar a função assíncrona
asyncio.run(connect_to_websocket())