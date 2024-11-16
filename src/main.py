import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, abort
import google.generativeai as genai

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa o aplicativo Flask
app = Flask(__name__)

def get_google_api_key():
    """Obtém a chave de API do Google a partir das variáveis de ambiente."""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("A chave GOOGLE_API_KEY não está definida nas variáveis de ambiente.")
    return api_key

def configure_genai(api_key):
    """Configura a API do Google Generative AI com a chave fornecida e retorna o modelo."""
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

@app.route('/', methods=['POST'])
def home():
    """Rota para processar mensagens e gerar respostas usando o modelo Generative AI."""
    # Obtém os dados JSON enviados na requisição
    data = request.get_json()

    # Verifica se a chave 'message' está presente nos dados
    if not data or 'message' not in data:
        abort(400, description="A chave 'message' está ausente na carga da requisição.")

    # Obtém a chave da API e configura o modelo
    try:
        api_key = get_google_api_key()
        model = configure_genai(api_key)
    except ValueError as e:
        abort(500, description=str(e))

    # Inicia a sessão de chat e envia a mensagem para o modelo
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(data['message'])

    # Retorna a resposta gerada como JSON
    return jsonify(response), 200

if __name__ == "__main__":
    # Inicia o servidor Flask na porta 5001
    app.run(port=5001, debug=True)
