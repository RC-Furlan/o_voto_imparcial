from pathlib import Path

import duckdb
import pandas as pd

ARQUIVO_CSV = Path(
    "dados/analitico/perfis_candidatos.csv"
)

ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)

ARQUIVO_BANCO.parent.mkdir(
    parents=True,
    exist_ok=True
)

df = pd.read_csv(
    ARQUIVO_CSV,
    sep=";"
)

con = duckdb.connect(
    str(ARQUIVO_BANCO)
)

con.execute(
    """
    DROP TABLE IF EXISTS candidatos
    """
)

con.register(
    "df_candidatos",
    df
)

con.execute(
    """
    CREATE TABLE candidatos AS
    SELECT *
    FROM df_candidatos
    """
)

resultado = con.execute(
    """
    SELECT COUNT(*)
    FROM candidatos
    """
).fetchone()[0]

print(f"Registros carregados: {resultado}")

con.close()