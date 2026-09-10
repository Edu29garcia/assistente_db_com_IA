import pandasai as pai
from config import carregar_variaveis_ambiente, get_llm
from database import get_engine, listar_tabelas, carregar_tabelas

carregar_variaveis_ambiente()
llm = get_llm()
pai.config.set({"llm": llm})

engine = get_engine()
tabelas = carregar_tabelas(engine, listar_tabelas(engine))
dfs = [pai.DataFrame(df) for df in tabelas.values()]

resposta = pai.chat("Mostre apenas o nome e o valor gasto dos 5 clientes que mais gastaram, ordenados do maior para o menor.", *dfs)

if resposta.type == "dataframe":
    resultado_formatado = resposta.value.to_string(index=False)
elif resposta.type == "number":
    resultado_formatado = str(resposta.value)
elif resposta.type == "string":
    resultado_formatado = resposta.value
else:
    resultado_formatado = str(resposta.value)

print("Tipo da resposta:", resposta.type)
print("\nResultado formatado:\n")
print(resultado_formatado)