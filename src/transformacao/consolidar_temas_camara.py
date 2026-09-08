from pathlib import Path

import pandas as pd


ARQUIVO_PROJETOS = Path(
    "dados/processado/projetos_camara.csv"
)

ARQUIVO_SAIDA = Path(
    "dados/processado/projetos_camara_consolidado.csv"
)


def main() -> None:
    df = pd.read_csv(
        ARQUIVO_PROJETOS,
        sep=";",
        encoding="utf-8-sig",
        quotechar='"',
        low_memory=False
    )

    df["tema"] = (
        df["tema"]
        .fillna("Sem classificação temática")
        .astype(str)
        .str.strip()
    )

    df["relevancia"] = pd.to_numeric(
        df["relevancia"],
        errors="coerce"
    )

    df = df.sort_values(
        [
            "idProposicao",
            "relevancia"
        ],
        ascending=[
            True,
            False
        ],
        na_position="last"
    )

    df["tema_principal"] = (
        df.groupby("idProposicao")["tema"]
        .transform("first")
    )

    temas = (
        df.groupby("idProposicao")["tema"]
        .agg(
            lambda valores: " | ".join(
                pd.unique(valores.astype(str))
            )
        )
        .rename("temas")
        .reset_index()
    )

    df_final = (
        df.drop_duplicates(
            subset=["idProposicao"]
        )
        .drop(
            columns=[
                "tema",
                "relevancia"
            ],
            errors="ignore"
        )
        .merge(
            temas,
            on="idProposicao",
            how="left"
        )
    )

    df_final.to_csv(
        ARQUIVO_SAIDA,
        sep=";",
        encoding="utf-8-sig",
        index=False
    )

    print(f"Registros gravados: {len(df_final)}")
    print(
        f"Proposições únicas: "
        f"{df_final['idProposicao'].nunique()}"
    )
    print(f"Arquivo: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    main()