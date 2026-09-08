from pathlib import Path
import pandas as pd

ARQ_CAND = Path(
    "dados/selecionados/tse/consulta_cand_2026_BR.csv"
)

ARQ_COMP = Path(
    "dados/selecionados/tse/consulta_cand_complementar_2026_BR.csv"
)

ARQ_BENS = Path(
    "dados/selecionados/tse/bem_candidato_2026_BR.csv"
)

SAIDA = Path(
    "dados/processado/candidatos_presidencia.csv"
)

SAIDA.parent.mkdir(parents=True, exist_ok=True)

df_cand = pd.read_csv(
    ARQ_CAND,
    sep=";",
    encoding="latin1",
    low_memory=False
)

df_comp = pd.read_csv(
    ARQ_COMP,
    sep=";",
    encoding="latin1",
    low_memory=False
)

df_bens = pd.read_csv(
    ARQ_BENS,
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

df_presidentes = df_cand[
    df_cand["DS_CARGO"] == "PRESIDENTE"
].copy()

resumo_bens = (
    df_bens
    .groupby("SQ_CANDIDATO")
    .agg(
        quantidade_bens=("NR_ORDEM_BEM_CANDIDATO", "count"),
        patrimonio_total=("VR_BEM_CANDIDATO", "sum")
    )
    .reset_index()
)

df_final = (
    df_presidentes
    .merge(
        df_comp[
            [
                "SQ_CANDIDATO",
                "ST_DECLARAR_BENS"
            ]
        ],
        on="SQ_CANDIDATO",
        how="left"
    )
    .merge(
        resumo_bens,
        on="SQ_CANDIDATO",
        how="left"
    )
)

df_final["quantidade_bens"] = (
    df_final["quantidade_bens"]
    .fillna(0)
    .astype(int)
)

df_final["patrimonio_total"] = (
    df_final["patrimonio_total"]
    .fillna(0)
)

df_final = df_final[
    [
        "SQ_CANDIDATO",
        "NM_CANDIDATO",
        "NM_URNA_CANDIDATO",
        "SG_PARTIDO",
        "DS_GENERO",
        "DS_COR_RACA",
        "DS_GRAU_INSTRUCAO",
        "DS_OCUPACAO",
        "ST_DECLARAR_BENS",
        "quantidade_bens",
        "patrimonio_total"
    ]
]

df_final.to_csv(
    SAIDA,
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print(df_final.shape)
print(SAIDA)