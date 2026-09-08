from pathlib import Path

import duckdb
import pandas as pd


ARQUIVO_CSV = Path(
    "dados/processado/materias_senado_final.csv"
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
    DROP TABLE IF EXISTS materias_senado
    """
)


con.register(
    "df_materias_senado",
    df
)


con.execute(
    """
    CREATE TABLE materias_senado AS
    SELECT *
    FROM df_materias_senado
    """
)


registros = con.execute(
    """
    SELECT COUNT(*)
    FROM materias_senado
    """
).fetchone()[0]


materias_unicas = con.execute(
    """
    SELECT COUNT(DISTINCT codigo_materia)
    FROM materias_senado
    """
).fetchone()[0]


con.close()


print(f"Registros carregados: {registros}")
print(f"Matérias únicas: {materias_unicas}")