from pathlib import Path

import duckdb
import pandas as pd


ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)


CORES_CARDS = [
    "#264653",
    "#2A9D8F",
    "#E9C46A",
    "#F4A261",
    "#E76F51",
    "#277DA1",
    "#577590",
    "#F94144",
    "#F3722C",
    "#F8961E",
    "#90BE6D",
    "#43AA8B",
    "#6D597A",
]


con = duckdb.connect(
    str(ARQUIVO_BANCO)
)


df = con.execute(
    """
    SELECT
        SQ_CANDIDATO
    FROM candidatos
    ORDER BY
        SQ_CANDIDATO
    """
).df()


con.close()


if len(df) != 13:
    raise ValueError(
        f"Esperados 13 candidatos. "
        f"Encontrados: {len(df)}"
    )


if df["SQ_CANDIDATO"].nunique() != 13:
    raise ValueError(
        "Existem candidatos duplicados."
    )


if len(CORES_CARDS) != 13:
    raise ValueError(
        "A paleta deve conter exatamente 13 cores."
    )


df["indice_anonimo"] = range(
    100,
    113
)


df["rotulo_anonimo"] = (
    "Candidato "
    + df["indice_anonimo"].astype(str)
)


df["cor_card"] = CORES_CARDS


df = df[
    [
        "SQ_CANDIDATO",
        "indice_anonimo",
        "rotulo_anonimo",
        "cor_card",
    ]
].copy()


con = duckdb.connect(
    str(ARQUIVO_BANCO)
)


con.execute(
    """
    DROP TABLE IF EXISTS candidatos_anonimos
    """
)


con.register(
    "df_anonimos",
    df
)


con.execute(
    """
    CREATE TABLE candidatos_anonimos AS
    SELECT
        SQ_CANDIDATO,
        indice_anonimo,
        rotulo_anonimo,
        cor_card
    FROM df_anonimos
    """
)


resultado = con.execute(
    """
    SELECT
        COUNT(*) AS registros,
        COUNT(DISTINCT SQ_CANDIDATO)
            AS candidatos_unicos,
        COUNT(DISTINCT indice_anonimo)
            AS identificadores_unicos,
        COUNT(DISTINCT cor_card)
            AS cores_unicas
    FROM candidatos_anonimos
    """
).fetchone()


print(
    f"Registros criados: {resultado[0]}"
)

print(
    f"Candidatos únicos: {resultado[1]}"
)

print(
    f"Identificadores únicos: {resultado[2]}"
)

print(
    f"Cores únicas: {resultado[3]}"
)

print()

print(
    con.execute(
        """
        SELECT
            indice_anonimo,
            rotulo_anonimo,
            cor_card
        FROM candidatos_anonimos
        ORDER BY
            indice_anonimo
        """
    ).df().to_string(index=False)
)


con.close()