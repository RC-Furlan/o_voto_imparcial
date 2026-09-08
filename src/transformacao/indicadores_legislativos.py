from pathlib import Path

import duckdb


ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)

ARQUIVO_SAIDA = Path(
    "dados/analitico/indicadores_legislativos.csv"
)


con = duckdb.connect(
    str(ARQUIVO_BANCO)
)


consulta = """
WITH camara AS (
    SELECT
        candidato,
        COUNT(DISTINCT idProposicao) AS projetos_camara,
        SUM(
            CASE
                WHEN aprovado THEN 1
                ELSE 0
            END
        ) AS aprovados_camara
    FROM projetos_camara
    GROUP BY candidato
),

senado AS (
    SELECT
        candidato,
        COUNT(DISTINCT codigo_materia) AS materias_senado,
        SUM(
            CASE
                WHEN tramitando = 'S' THEN 1
                ELSE 0
            END
        ) AS tramitando_senado,
        SUM(
            CASE
                WHEN tramitando = 'N' THEN 1
                ELSE 0
            END
        ) AS nao_tramitando_senado
    FROM materias_senado
    GROUP BY candidato
)

SELECT
    c.NM_URNA_CANDIDATO AS candidato,

    COALESCE(
        camara.projetos_camara,
        0
    ) AS projetos_camara,

    COALESCE(
        camara.aprovados_camara,
        0
    ) AS aprovados_camara,

    COALESCE(
        senado.materias_senado,
        0
    ) AS materias_senado,

    COALESCE(
        senado.tramitando_senado,
        0
    ) AS tramitando_senado,

    COALESCE(
        senado.nao_tramitando_senado,
        0
    ) AS nao_tramitando_senado

FROM candidatos AS c

LEFT JOIN camara
    ON c.NM_URNA_CANDIDATO = camara.candidato

LEFT JOIN senado
    ON (
        (
            c.NM_URNA_CANDIDATO = 'FLAVIO BOLSONARO'
            AND senado.candidato = 'FLAVIO_BOLSONARO'
        )
        OR (
            c.NM_URNA_CANDIDATO = 'RONALDO CAIADO'
            AND senado.candidato = 'RONALDO_CAIADO'
        )
        OR (
            c.NM_URNA_CANDIDATO = senado.candidato
        )
    )

WHERE c.NM_URNA_CANDIDATO IN (
    'FLAVIO BOLSONARO',
    'RONALDO CAIADO'
)

ORDER BY
    c.NM_URNA_CANDIDATO
"""


df = con.execute(
    consulta
).df()


ARQUIVO_SAIDA.parent.mkdir(
    parents=True,
    exist_ok=True
)


df.to_csv(
    ARQUIVO_SAIDA,
    sep=";",
    encoding="utf-8-sig",
    index=False
)


print(
    f"Registros gravados: {len(df)}"
)

print(
    f"Arquivo: {ARQUIVO_SAIDA}"
)

print()

print(
    df.to_string(index=False)
)


con.close()