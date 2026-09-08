from pathlib import Path

import duckdb
import pandas as pd


ARQUIVO_CSV = Path(
    "dados/analitico/indicadores_legislativos.csv"
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
    DROP TABLE IF EXISTS indicadores_legislativos
    """
)


con.register(
    "df_indicadores",
    df
)


con.execute(
    """
    CREATE TABLE indicadores_legislativos AS
    SELECT *
    FROM df_indicadores
    """
)


registros = con.execute(
    """
    SELECT COUNT(*)
    FROM indicadores_legislativos
    """
).fetchone()[0]


con.close()


print(
    f"Registros carregados: {registros}"
)