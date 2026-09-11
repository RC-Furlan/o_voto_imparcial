from pathlib import Path

import duckdb
import pandas as pd


ARQUIVO_CSV = Path(
    "dados/processado/propostas_governo.csv"
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


if len(df) != 13:
    raise ValueError(
        f"Esperados 13 candidatos. Encontrados: {len(df)}"
    )


if df["SQ_CANDIDATO"].nunique() != 13:
    raise ValueError(
        "Existem candidatos duplicados."
    )


if df["url_proposta_governo"].isna().any():
    raise ValueError(
        "Existem candidatos sem URL de proposta de governo."
    )


if df["url_proposta_governo"].nunique() != 13:
    raise ValueError(
        "Existem URLs de propostas duplicadas."
    )


con = duckdb.connect(
    str(ARQUIVO_BANCO)
)


con.execute(
    """
    DROP TABLE IF EXISTS propostas_governo
    """
)


con.register(
    "df_propostas",
    df
)


con.execute(
    """
    CREATE TABLE propostas_governo AS
    SELECT
        SQ_CANDIDATO,
        NM_URNA_CANDIDATO,
        codigo_documento_tse,
        url_proposta_governo,
        fonte_proposta_governo,
        url_catalogo_tse,
        tipo_documento,
        acesso_publico
    FROM df_propostas
    """
)


resultado = con.execute(
    """
    SELECT
        COUNT(*) AS candidatos,
        COUNT(DISTINCT SQ_CANDIDATO) AS candidatos_unicos,
        COUNT(DISTINCT url_proposta_governo) AS urls_unicas,
        SUM(
            CASE
                WHEN acesso_publico
                    THEN 1
                ELSE 0
            END
        ) AS documentos_publicos
    FROM propostas_governo
    """
).fetchone()


print(
    f"Registros carregados: {resultado[0]}"
)

print(
    f"Candidatos únicos: {resultado[1]}"
)

print(
    f"URLs únicas: {resultado[2]}"
)

print(
    f"Documentos públicos: {resultado[3]}"
)

print()

print(
    con.execute(
        """
        SELECT
            NM_URNA_CANDIDATO,
            codigo_documento_tse,
            url_proposta_governo
        FROM propostas_governo
        ORDER BY NM_URNA_CANDIDATO
        """
    ).df().to_string(index=False)
)


con.close()