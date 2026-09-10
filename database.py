import pandas as pd
from sqlalchemy import create_engine, inspect

# Criar e retornar a engine de conexão com o db sqlite
def get_engine( caminho_db: str = 'ecommerce.db' ):
    return create_engine(f'sqlite:///{caminho_db}')


# Listar as tebelas que tenho no db
def listar_tabelas(engine) -> list[str]:
    inspector = inspect(engine)
    return inspector.get_table_names()

# Ler cada tabela do db e retornar um dicionario delas
def carregar_tabelas(engine, nomes_tabelas: list[str]) -> dict[str, pd.DataFrame]:

    if nomes_tabelas is None:
        nomes_tabelas = listar_tabelas(engine)

    tabelas = {}

    with engine.connect() as conexao:
        for nome in nomes_tabelas:
            tabelas[nome] = pd.read_sql_table(nome, conexao)

    return tabelas

