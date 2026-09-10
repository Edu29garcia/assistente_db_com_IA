import pandas as pd
from litellm import completion

# Descrever as tabelas usando um llm
def gerar_descricao_tabela(nome_tabela: str, df: pd.DataFrame, api_key: str):
    amostra = df.head().to_string()
    colunas = ', '.join(df.columns)
    prompt = (
        f"Você é um assistente que documenta bancos de dados.\n"
        f"Tabela: {nome_tabela}\n"
        f"Colunas: {colunas}\n"
        f"Amostra de dados:\n{amostra}\n\n"
        f"Escreva uma descrição curta (2-3 frases) explicando o que essa tabela "
        f"representa e que tipo de perguntas ela pode responder."
    )
    resposta = completion(
        model="groq/openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        api_key=api_key,
    )
    return resposta.choices[0].message.content

def gerar_descricoes(tabelas: dict, llm):
    descricoes = {}
    for nome, df in tabelas.items():
        descricoes[nome] = gerar_descricao_tabela(nome, df, llm)

    return descricoes

 