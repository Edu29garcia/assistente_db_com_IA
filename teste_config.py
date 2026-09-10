from config import carregar_variaveis_ambiente, get_llm, get_api_key

carregar_variaveis_ambiente()

api_key = get_api_key()
print('Chave carregada:', api_key[:3] + '......')  #Mostrando só os 3 primeiros digitos da chave

llm = get_llm()
print('LLM configurada:', llm)