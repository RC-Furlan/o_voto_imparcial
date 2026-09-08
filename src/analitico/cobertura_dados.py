from pathlib import Path

import duckdb


ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)

ARQUIVO_SAIDA = Path(
    "dados/analitico/cobertura_dados.csv"
)


con = duckdb.connect(
    str(ARQUIVO_BANCO)
)


consulta = """
SELECT
    SQ_CANDIDATO,
    NM_CANDIDATO,
    NM_URNA_CANDIDATO,
    SG_PARTIDO,

    CASE
        WHEN quantidade_bens > 0
            THEN TRUE
        ELSE FALSE
    END AS possui_dados_patrimoniais,

    possui_dados_legislativos,

    status_dados_legislativos,
    fontes_legislativas,

    CASE
        WHEN quantidade_bens > 0
            THEN 'DADOS_DISPONIVEIS'
        ELSE 'SEM_DADOS_NA_BASE_COLETADA'
    END AS status_dados_patrimoniais,

    CASE
        WHEN quantidade_bens > 0
             AND possui_dados_legislativos
            THEN 'PATRIMONIO_E_LEGISLATIVO'

        WHEN quantidade_bens > 0
            THEN 'APENAS_PATRIMONIO'

        WHEN possui_dados_legislativos
            THEN 'APENAS_LEGISLATIVO'

        ELSE 'SEM_DADOS_ANALITICOS'
    END AS cobertura_geral

FROM perfil_candidatos

ORDER BY
    NM_URNA_CANDIDATO
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

print()

print("RESUMO DA COBERTURA")

print(
    df["cobertura_geral"]
    .value_counts()
    .to_string()
)


con.close()