# api.py
import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# # Configuração da API da Groq
# API_KEY = ""
# client = Groq(api_key=API_KEY)

# Carrega o .env
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY não encontrada")

client = Groq(api_key=API_KEY)

# Inicializa o FastAPI
app = FastAPI()

# Habilita CORS para permitir requisições do Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Altere para o domínio do seu frontend em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Classe para validar o request
class MensagemRequest(BaseModel):
    mensagem: str
    historico: list  # Lista de mensagens anteriores para manter o contexto

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao RISOFLORAI"}

@app.post("/chat")
def chat(mensagem_request: MensagemRequest):
    """ Rota para enviar mensagens ao chatbot """
    historico = mensagem_request.historico

    # Adiciona a nova mensagem ao histórico
    historico.append({"role": "user", "content": mensagem_request.mensagem})

    # Chamada para a API da Groq
    resposta = client.chat.completions.create(
        messages=historico,
        model="llama-3.3-70b-versatile"
    )

    resposta_texto = resposta.choices[0].message.content

    # Adiciona a resposta do chatbot ao histórico
    historico.append({"role": "assistant", "content": resposta_texto})

    return {"resposta": resposta_texto, "historico": historico}

# @app.post("/chat")
# def chat(mensagem_request: MensagemRequest):
#     """ Rota para enviar mensagens ao chatbot """
#     historico = mensagem_request.historico
#     historico.append({"role": "user", "content": mensagem_request.mensagem})

#     resposta = client.chat.completions.create(
#         messages=historico,
#         model="llama3-8b-8192"
#     )

#     resposta_texto = resposta.choices[0].message.content
#     historico.append({"role": "assistant", "content": resposta_texto})

#     response = JSONResponse(content={"resposta": resposta_texto, "historico": historico})
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
#     response.headers["Access-Control-Allow-Headers"] = "*"

#     return response

# Inicia o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
