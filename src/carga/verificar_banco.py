import duckdb
from pathlib import Path


ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)


con = duckdb.connect(
    str(ARQUIVO_BANCO)
)

tabelas = con.execute(
    "SHOW TABLES"
).fetchall()

con.close()

print("Tabelas:")
for tabela in tabelas:
    print(tabela[0])