from pathlib import Path

import duckdb
import pandas as pd


ARQUIVO_CSV = Path(
    "dados/analitico/cobertura_dados.csv"
)

ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)


df = pd.read_csv(
    ARQUIVO_CSV,
    sep=";",
    encoding="utf-8-sig",
    low_memory=False
)


con = duckdb.connect(
    str(ARQUIVO_BANCO)
)


con.execute(
    """
    DROP TABLE IF EXISTS cobertura_dados
    """
)


con.register(
    "df_cobertura",
    df
)


con.execute(
    """
    CREATE TABLE cobertura_dados AS
    SELECT *
    FROM df_cobertura
    """
)


registros = con.execute(
    """
    SELECT COUNT(*)
    FROM cobertura_dados
    """
).fetchone()[0]


con.close()


print(
    f"Registros carregados: {registros}"
)