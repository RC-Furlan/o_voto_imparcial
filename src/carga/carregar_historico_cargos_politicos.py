from pathlib import Path

import duckdb
import pandas as pd


ARQUIVO_CSV = Path(
    "dados/processado/historico_cargos_politicos.csv"
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


colunas_esperadas = [
    "SQ_CANDIDATO",
    "NM_URNA_CANDIDATO",
    "cargo",
    "esfera",
    "localidade",
    "inicio",
    "fim",
    "situacao",
    "fonte",
    "url_fonte",
]


colunas_faltantes = [
    coluna
    for coluna in colunas_esperadas
    if coluna not in df.columns
]


if colunas_faltantes:
    raise ValueError(
        "Colunas ausentes no arquivo: "
        f"{colunas_faltantes}"
    )


df = df[
    colunas_esperadas
].copy()


df["SQ_CANDIDATO"] = pd.to_numeric(
    df["SQ_CANDIDATO"],
    errors="coerce"
)


if df["SQ_CANDIDATO"].isna().any():
    raise ValueError(
        "Existem candidatos sem SQ_CANDIDATO válido."
    )


if df.empty:
    raise ValueError(
        "O arquivo de cargos está vazio."
    )


df = df.drop_duplicates(
    subset=[
        "SQ_CANDIDATO",
        "cargo",
        "inicio",
        "fim",
    ]
)


con = duckdb.connect(
    str(ARQUIVO_BANCO)
)


con.execute(
    """
    DROP TABLE IF EXISTS historico_cargos_politicos
    """
)


con.register(
    "df_cargos",
    df
)


con.execute(
    """
    CREATE TABLE historico_cargos_politicos AS
    SELECT *
    FROM df_cargos
    """
)


resultado = con.execute(
    """
    SELECT
        COUNT(*) AS registros,
        COUNT(
            DISTINCT SQ_CANDIDATO
        ) AS candidatos
    FROM historico_cargos_politicos
    """
).fetchone()


print(
    f"Registros carregados: {resultado[0]}"
)

print(
    f"Candidatos com cargos: {resultado[1]}"
)

print()

print(
    con.execute(
        """
        SELECT
            NM_URNA_CANDIDATO,
            cargo,
            esfera,
            localidade,
            inicio,
            fim,
            situacao
        FROM historico_cargos_politicos
        ORDER BY
            NM_URNA_CANDIDATO,
            inicio
        """
    ).df().to_string(index=False)
)


con.close()