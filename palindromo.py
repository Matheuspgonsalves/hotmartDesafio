import asyncio
import websockets

async def find_longest_palindrome(word):
    def is_palindrome(s):
        return s == s[::-1]
    
    longest_palindrome = ""
    word_length = len(word)
    
    # Test all substrings
    for i in range(word_length):
        for j in range(i + 1, word_length + 1):
            substring = word[i:j]
            if is_palindrome(substring) and len(substring) > len(longest_palindrome):
                longest_palindrome = substring
    
    # Return "Sem palindromo" if no palindrome is found or the longest palindrome is less than 3 characters
    return longest_palindrome if len(longest_palindrome) >= 3 else "Sem palindromo"

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

            # Enviar "start palindromo"
            await websocket.send("start palindromo")
            print("Sent message: start palindromo")

            while True:
                # Receber a resposta do servidor
                response = await websocket.recv()
                print(f"Received message: \n{response}")

                # Verificar se o servidor enviou uma palavra para processar
                if "[*] Word:" in response:
                    word = response.split(":")[1].strip()
                    print(f"Word to check: {word}")
                    
                    # Encontrar o maior palíndromo na palavra
                    longest_palindrome = await find_longest_palindrome(word)
                    print(f"Longest palindrome: {longest_palindrome}")

                    # Enviar a resposta com o maior palíndromo
                    await websocket.send(longest_palindrome)
                    print(f"Sent message: {longest_palindrome}")

                elif "Correto" in response:
                    print("Received confirmation: Correct")

                elif "Incorreto" in response:
                    print("Received confirmation: Incorrect")

        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Executar a função assíncrona
asyncio.run(connect_to_websocket())
