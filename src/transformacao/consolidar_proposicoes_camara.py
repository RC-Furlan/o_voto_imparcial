from pathlib import Path

import pandas as pd


ARQUIVO = Path(
    "dados/processado/projetos_camara_consolidado.csv"
)

ARQUIVO_SAIDA = Path(
    "dados/processado/projetos_camara_final.csv"
)


TIPOS_PROJETO = {
    "PL",
    "PLP",
    "PEC",
    "PDC",
    "PRC",
    "PRN",
    "PLV",
}


df = pd.read_csv(
    ARQUIVO,
    sep=";",
    encoding="utf-8-sig",
    quotechar='"',
    low_memory=False
)


df["siglaTipo"] = (
    df["siglaTipo"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.upper()
)


df["situacao"] = (
    df["ultimoStatus_descricaoSituacao"]
    .fillna("")
    .astype(str)
    .str.strip()
)


df["tramitacao"] = (
    df["ultimoStatus_descricaoTramitacao"]
    .fillna("")
    .astype(str)
    .str.strip()
)


df["aprovado"] = (
    df["situacao"].isin(
        [
            "Transformado em Norma Jurídica",
            "Vetado totalmente",
        ]
    )
    | (
        df["situacao"].eq("Tramitação Finalizada")
        & df["tramitacao"].str.contains(
            "Aprovação",
            case=False,
            regex=False,
            na=False
        )
    )
)


df = df[
    df["siglaTipo"].isin(TIPOS_PROJETO)
].copy()


df.to_csv(
    ARQUIVO_SAIDA,
    sep=";",
    encoding="utf-8-sig",
    index=False
)


print(
    f"Projetos legislativos encontrados: {len(df)}"
)

print(
    f"Projetos aprovados: {df['aprovado'].sum()}"
)

print()

print(
    df.groupby("candidato")
    .agg(
        apresentados=(
            "idProposicao",
            "nunique"
        ),
        aprovados=(
            "aprovado",
            "sum"
        )
    )
    .to_string()
)

print()
print(f"Arquivo: {ARQUIVO_SAIDA}")