from pathlib import Path

import duckdb


ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)


con = duckdb.connect(
    str(ARQUIVO_BANCO)
)


con.execute(
    """
    DROP TABLE IF EXISTS bens_candidatos_detalhados
    """
)


con.execute(
    """
    CREATE TABLE bens_candidatos_detalhados AS

    SELECT
        b.SQ_CANDIDATO,
        c.NM_CANDIDATO,
        c.NM_URNA_CANDIDATO,
        c.SG_PARTIDO,

        b.NR_ORDEM_BEM_CANDIDATO,
        b.CD_TIPO_BEM_CANDIDATO,
        b.DS_TIPO_BEM_CANDIDATO,
        b.DS_BEM_CANDIDATO,
        b.VR_BEM_CANDIDATO,
        b.categoria

    FROM bens_candidatos AS b

    INNER JOIN candidatos AS c
        ON b.SQ_CANDIDATO = c.SQ_CANDIDATO
    """
)


registros = con.execute(
    """
    SELECT COUNT(*)
    FROM bens_candidatos_detalhados
    """
).fetchone()[0]


candidatos = con.execute(
    """
    SELECT COUNT(DISTINCT SQ_CANDIDATO)
    FROM bens_candidatos_detalhados
    """
).fetchone()[0]


print(
    f"Registros: {registros}"
)

print(
    f"Candidatos: {candidatos}"
)


con.close()