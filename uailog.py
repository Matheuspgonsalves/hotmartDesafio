import asyncio
import websockets
import re
import heapq

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

            # Enviar "start uailog" após receber a resposta
            await websocket.send("start uailog")
            print("Sent message: start uailog")

            ruas = []
            ponto_inicial = None
            ponto_final = None

            while True:
                # Receber a mensagem contendo as ruas e os pontos de entrega
                response = await websocket.recv()
                print(f"Received message: \n{response}")

                if "Ruas" in response:
                    # Extrair ruas da mensagem
                    ruas = re.findall(r"\('([^'])', '([^'])', (\d+)\)", response)
                    ruas = [(a, b, int(c)) for a, b, c in ruas]
                    print(f"Ruas: {ruas}")

                if "Ponto de Entrega Inicial" in response:
                    ponto_inicial_match = re.search(r"Ponto de Entrega Inicial: ([A-Z])", response)
                    if ponto_inicial_match:
                        ponto_inicial = ponto_inicial_match.group(1)
                        print(f"Ponto Inicial: {ponto_inicial}")

                if "Ponto de Entrega Final" in response:
                    ponto_final_match = re.search(r"Ponto de Entrega Final: ([A-Z])", response)
                    if ponto_final_match:
                        ponto_final = ponto_final_match.group(1)
                        print(f"Ponto Final: {ponto_final}")

                if ruas and ponto_inicial and ponto_final:
                    # Calcular a menor distância usando o algoritmo de Dijkstra
                    menor_distancia = dijkstra(ruas, ponto_inicial, ponto_final)
                    print(f"Menor distância: {menor_distancia}")

                    # Enviar a resposta com a menor distância
                    await websocket.send(str(menor_distancia))
                    print(f"Sent message: {menor_distancia}")

                    # Resetar as variáveis para a próxima rodada
                    ruas = []
                    ponto_inicial = None
                    ponto_final = None

        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

def dijkstra(ruas, inicio, fim):
    graph = {}
    for a, b, dist in ruas:
        if a not in graph:
            graph[a] = []
        if b not in graph:
            graph[b] = []
        graph[a].append((dist, b))
        graph[b].append((dist, a))

    queue = [(0, inicio)]
    distances = {inicio: 0}
    visited = set()

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node in visited:
            continue
        visited.add(current_node)

        if current_node == fim:
            return current_distance

        for distance, neighbor in graph[current_node]:
            if neighbor in visited:
                continue
            new_distance = current_distance + distance
            if new_distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_distance
                heapq.heappush(queue, (new_distance, neighbor))

    return float('inf')

# Executar a função assíncrona
asyncio.run(connect_to_websocket())