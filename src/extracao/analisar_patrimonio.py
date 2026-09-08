from pathlib import Path
import pandas as pd

ARQUIVO_CANDIDATOS = Path(
    "dados/selecionados/tse/consulta_cand_2026_BR.csv"
)

ARQUIVO_BENS = Path(
    "dados/selecionados/tse/bem_candidato_2026_BR.csv"
)

df_candidatos = pd.read_csv(
    ARQUIVO_CANDIDATOS,
    sep=";",
    encoding="latin1",
    low_memory=False
)

df_bens = pd.read_csv(
    ARQUIVO_BENS,
    sep=";",
    encoding="latin1",
    low_memory=False
)

df_bens["VR_BEM_CANDIDATO"] = (
    df_bens["VR_BEM_CANDIDATO"]
    .astype(str)
    .str.replace(",", ".", regex=False)
)

df_bens["VR_BEM_CANDIDATO"] = pd.to_numeric(
    df_bens["VR_BEM_CANDIDATO"],
    errors="coerce"
).fillna(0)

df_presidentes = df_candidatos[
    df_candidatos["DS_CARGO"] == "PRESIDENTE"
].copy()

resumo = (
    df_bens
    .groupby("SQ_CANDIDATO")
    .agg(
        quantidade_bens=("NR_ORDEM_BEM_CANDIDATO", "count"),
        patrimonio_total=("VR_BEM_CANDIDATO", "sum")
    )
    .reset_index()
)

resultado = df_presidentes.merge(
    resumo,
    on="SQ_CANDIDATO",
    how="left"
)

resultado["quantidade_bens"] = resultado["quantidade_bens"].fillna(0)
resultado["patrimonio_total"] = resultado["patrimonio_total"].fillna(0)

resultado = resultado[
    [
        "NM_URNA_CANDIDATO",
        "SG_PARTIDO",
        "quantidade_bens",
        "patrimonio_total"
    ]
]

resultado = resultado.sort_values(
    "patrimonio_total",
    ascending=False
)

print(resultado.to_string(index=False))