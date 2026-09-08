from pathlib import Path

import duckdb


ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)


con = duckdb.connect(
    str(ARQUIVO_BANCO)
)


resultado = con.execute(
    """
    SELECT
        COUNT(*) AS candidatos,

        COUNT(DISTINCT SQ_CANDIDATO)
            AS candidatos_unicos,

        SUM(
            CASE
                WHEN possui_dados_patrimoniais
                    THEN 1
                ELSE 0
            END
        ) AS candidatos_com_patrimonio,

        SUM(
            CASE
                WHEN possui_dados_legislativos
                    THEN 1
                ELSE 0
            END
        ) AS candidatos_com_legislativo,

        SUM(
            CASE
                WHEN cobertura_geral = 'PATRIMONIO_E_LEGISLATIVO'
                    THEN 1
                ELSE 0
            END
        ) AS patrimonio_e_legislativo,

        SUM(
            CASE
                WHEN cobertura_geral = 'APENAS_PATRIMONIO'
                    THEN 1
                ELSE 0
            END
        ) AS apenas_patrimonio,

        SUM(
            CASE
                WHEN cobertura_geral = 'SEM_DADOS_ANALITICOS'
                    THEN 1
                ELSE 0
            END
        ) AS sem_dados_analiticos

    FROM perfil_candidatos
    """
).fetchone()


print("VALIDAÇÃO FINAL DA BASE")
print()

print(
    f"Candidatos: {resultado[0]}"
)

print(
    f"Candidatos únicos: {resultado[1]}"
)

print(
    f"Com patrimônio: {resultado[2]}"
)

print(
    f"Com dados legislativos: {resultado[3]}"
)

print(
    f"Patrimônio + legislativo: {resultado[4]}"
)

print(
    f"Apenas patrimônio: {resultado[5]}"
)

print(
    f"Sem dados analíticos: {resultado[6]}"
)

print()

print("COBERTURA POR CANDIDATO")

print(
    con.execute(
        """
        SELECT
            NM_URNA_CANDIDATO,
            SG_PARTIDO,
            cobertura_geral
        FROM cobertura_dados
        ORDER BY NM_URNA_CANDIDATO
        """
    ).df().to_string(index=False)
)


con.close()