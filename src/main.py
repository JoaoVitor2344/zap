import os
from dotenv import load_dotenv
from requests.models import Response
import google.generativeai as genai
import json

load_dotenv()


def get_google_api_key():
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("A chave GOOGLE_API_KEY não está definida nas variáveis de ambiente.")
    return api_key


def configure_genai(api_key):
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


def generate_response(request_data):
    if 'message' not in request_data:
        raise ValueError("A chave 'message' está ausente nos dados da requisição.")

    message = request_data['message']
    if not message:
        raise ValueError("A mensagem não pode estar vazia.")

    api_key = get_google_api_key()
    model = configure_genai(api_key)

    chat_session = model.start_chat(history=[])

    return chat_session.send_message(message)


def extract_response_text(response):
    try:
        text = response._result.candidates[0].content.parts[0].text
        return text
    except (KeyError, IndexError, AttributeError) as e:
        raise ValueError("Erro ao extrair o texto da resposta: ", e)


def main(context):
    user_message = 'Oq é a vida?'
    request = {
        "message": user_message
    }

    response_text = extract_response_text(generate_response(request))

    response = Response()
    response._content = json.dumps({"message": response_text}).encode('utf-8')

    response_dict = {
        "status_code": 200,
        "body": json.dumps(response.json())
    }

    # return response_dict
    return context.log('')
