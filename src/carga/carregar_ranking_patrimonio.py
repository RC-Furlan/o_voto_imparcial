from pathlib import Path

import duckdb
import pandas as pd


ARQUIVO_CSV = Path(
    "dados/analitico/ranking_patrimonio.csv"
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
    DROP TABLE IF EXISTS ranking_patrimonio
    """
)


con.register(
    "df_ranking",
    df
)


con.execute(
    """
    CREATE TABLE ranking_patrimonio AS
    SELECT *
    FROM df_ranking
    """
)


registros = con.execute(
    """
    SELECT COUNT(*)
    FROM ranking_patrimonio
    """
).fetchone()[0]


con.close()


print(
    f"Registros carregados: {registros}"
)