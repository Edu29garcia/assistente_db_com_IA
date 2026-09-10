import os
from dotenv import load_dotenv
from pandasai_litellm.litellm import LiteLLM

# Carregar chave api
def carregar_variaveis_ambiente():
    load_dotenv('chave.env')

# Retornar a chave da API validada
def get_api_key() -> str:
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise ValueError('GROQ_API_KEY não encontrada. Verifique o arquivo chave.env')

    return api_key


# Montar a llm
def get_llm():
    api_key = get_api_key()
    modelo = "groq/openai/gpt-oss-120b"

    return LiteLLM(model=modelo, api_key = api_key)