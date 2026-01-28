# main.py
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Lê a variável do ambiente
API_KEY = os.getenv("GROQ_API_KEY")

# Verifica se existe
if not API_KEY:
    raise ValueError("A chave GROQ_API_KEY não foi encontrada!")

# Inicializa o cliente da Groq
client = Groq(api_key=API_KEY)

# Lista para armazenar o histórico da conversa
historico = []

def enviar_mensagem(mensagem):
    """ Envia a mensagem do usuário para a API, mantendo o histórico da conversa """
    
    # Adiciona a mensagem do usuário ao histórico
    historico.append({"role": "user", "content": mensagem})

    # Chama a API da Groq com o histórico completo
    resposta = client.chat.completions.create(
        messages=historico,  # Envia o histórico acumulado
        model="llama3-8b-8192"
    )

    # Obtém a resposta do chatbot
    resposta_texto = resposta.choices[0].message.content

    # Adiciona a resposta do chatbot ao histórico
    historico.append({"role": "assistant", "content": resposta_texto})

    return resposta_texto

# Loop de interação com o usuário
print("Digite 'sair' para encerrar o chat.")
while True:
    mensagem_usuario = input("Você: ")
    
    if mensagem_usuario.lower() == "sair":
        print("Chat encerrado.")
        break

    resposta_chatbot = enviar_mensagem(mensagem_usuario)
    print(f"Chatbot: {resposta_chatbot}")