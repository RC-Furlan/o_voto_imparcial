from pathlib import Path

import duckdb


ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)

ARQUIVO_SAIDA = Path(
    "dados/analitico/comparativo_patrimonio.csv"
)


con = duckdb.connect(
    str(ARQUIVO_BANCO)
)


df = con.execute(
    """
    SELECT
        SQ_CANDIDATO,
        NM_CANDIDATO,
        NM_URNA_CANDIDATO,
        SG_PARTIDO,

        ST_DECLARAR_BENS,
        quantidade_bens,
        patrimonio_total,

        qtd_imoveis,
        valor_imoveis,

        qtd_veiculos,
        valor_veiculos,

        qtd_investimentos,
        valor_investimentos,

        qtd_participacoes,
        valor_participacoes,

        qtd_contas,
        valor_contas,

        qtd_bens_valor,
        valor_bens_valor,

        qtd_outros,
        valor_outros

    FROM perfil_candidatos

    ORDER BY
        patrimonio_total DESC,
        NM_URNA_CANDIDATO
    """
).df()


df["participacao_patrimonio_pct"] = (
    df["patrimonio_total"]
    / df["patrimonio_total"].sum()
    * 100
)


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

print()

print(
    df[
        [
            "NM_URNA_CANDIDATO",
            "SG_PARTIDO",
            "quantidade_bens",
            "patrimonio_total",
            "participacao_patrimonio_pct"
        ]
    ].to_string(index=False)
)


con.close()