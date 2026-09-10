from database import get_engine, listar_tabelas, carregar_tabelas

engine = get_engine()
nomes = listar_tabelas(engine)
print("Tabelas encontradas:", nomes)

tabelas = carregar_tabelas(engine, nomes)
for nome, df in tabelas.items():
    print(f"\n{nome} — {len(df)} linhas")
    print(df.head(3))