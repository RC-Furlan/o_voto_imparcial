from pathlib import Path

import duckdb
import pandas as pd


ARQUIVO_CSV = Path(
    "dados/analitico/comparativo_patrimonio.csv"
)

ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)


df = pd.read_csv(
    ARQUIVO_CSV,
    sep=";",
    encoding="utf-8-sig"
)


con = duckdb.connect(
    str(ARQUIVO_BANCO)
)


con.execute(
    """
    DROP TABLE IF EXISTS comparativo_patrimonio
    """
)


con.register(
    "df_patrimonio",
    df
)


con.execute(
    """
    CREATE TABLE comparativo_patrimonio AS
    SELECT *
    FROM df_patrimonio
    """
)


registros = con.execute(
    """
    SELECT COUNT(*)
    FROM comparativo_patrimonio
    """
).fetchone()[0]


con.close()


print(
    f"Registros carregados: {registros}"
)