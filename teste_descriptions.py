from config import carregar_variaveis_ambiente
from database import get_engine, listar_tabelas, carregar_tabelas
from descriptions import gerar_descricoes
import os

carregar_variaveis_ambiente()
api_key = os.getenv("API_KEY_GROQ")

engine = get_engine()
nomes = listar_tabelas(engine)
tabelas = carregar_tabelas(engine, nomes)

descricoes = gerar_descricoes(tabelas, api_key)
for nome, desc in descricoes.items():
    print(f"\n=== {nome} ===\n{desc}")