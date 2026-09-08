from pathlib import Path

import duckdb


ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)

ARQUIVO_SAIDA = Path(
    "dados/analitico/perfil_candidatos.csv"
)


con = duckdb.connect(
    str(ARQUIVO_BANCO)
)


df = con.execute(
    """
    SELECT
        *
    FROM perfil_candidatos
    ORDER BY
        NM_URNA_CANDIDATO
    """
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
    f"Colunas: {len(df.columns)}"
)

print(
    f"Arquivo: {ARQUIVO_SAIDA}"
)


con.close()