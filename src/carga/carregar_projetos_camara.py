from pathlib import Path

import duckdb
import pandas as pd


ARQUIVO_CSV = Path(
    "dados/processado/projetos_camara_final.csv"
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
    DROP TABLE IF EXISTS projetos_camara
    """
)


con.register(
    "df_projetos",
    df
)


con.execute(
    """
    CREATE TABLE projetos_camara AS
    SELECT *
    FROM df_projetos
    """
)


registros = con.execute(
    """
    SELECT COUNT(*)
    FROM projetos_camara
    """
).fetchone()[0]


proposicoes = con.execute(
    """
    SELECT COUNT(DISTINCT idProposicao)
    FROM projetos_camara
    """
).fetchone()[0]


con.close()


print(f"Registros carregados: {registros}")
print(f"Proposições únicas: {proposicoes}")