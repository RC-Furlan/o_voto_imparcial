from pathlib import Path

import duckdb
import pandas as pd


ARQUIVO_CSV = Path(
    "dados/analitico/indicadores_camara.csv"
)

ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)


df = pd.read_csv(
    ARQUIVO_CSV,
    sep=";",
    encoding="utf-8-sig",
)


con = duckdb.connect(
    str(ARQUIVO_BANCO)
)


con.execute(
    """
    DROP TABLE IF EXISTS indicadores_camara
    """
)


con.register(
    "df_indicadores",
    df
)


con.execute(
    """
    CREATE TABLE indicadores_camara AS
    SELECT
        *
    FROM df_indicadores
    """
)


registros = con.execute(
    """
    SELECT COUNT(*)
    FROM indicadores_camara
    """
).fetchone()[0]


con.close()


print(
    f"Registros carregados: {registros}"
)