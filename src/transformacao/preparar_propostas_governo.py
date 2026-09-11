from pathlib import Path

import duckdb
import pandas as pd


ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)

ARQUIVO_SAIDA = Path(
    "dados/processado/propostas_governo.csv"
)

URL_CATALOGO_TSE = (
    "https://dadosabertos.tse.jus.br/pt_BR/dataset/candidatos-2026"
)

URL_BASE_TSE = (
    "https://divulgacandcontas.tse.jus.br/"
    "divulga/rest/arquivo/doc/"
)


PROPOSTAS = {
    "CLARIANA BARAO": "280017113380",
    "EDMILSON COSTA": "280017107286",
    "ESCRITOR AUGUSTO CURY": "280017125643",
    "FLAVIO BOLSONARO": "280017104726",
    "HERTZ DIAS": "280016998007",
    "LULA": "280017016005",
    "PABLO MARÇAL": "280017134368",
    "RENAN SANTOS": "280017002789",
    "RONALDO CAIADO": "280017106566",
    "RUI COSTA PIMENTA": "280017113417",
    "SAMARA": "280017119534",
    "VETERINÁRIO WILSON GRASSI": "280017075366",
    "ZEMA": "280016919931",
}


def main() -> None:
    if len(PROPOSTAS) != 13:
        raise ValueError(
            "A configuração das propostas deve conter "
            "exatamente 13 candidatos."
        )

    if len(set(PROPOSTAS.values())) != 13:
        raise ValueError(
            "Existem códigos de propostas duplicados."
        )

    con = duckdb.connect(
        str(ARQUIVO_BANCO),
        read_only=True
    )

    candidatos = con.execute(
        """
        SELECT
            SQ_CANDIDATO,
            NM_URNA_CANDIDATO
        FROM candidatos
        WHERE NM_URNA_CANDIDATO IN (
            'CLARIANA BARAO',
            'EDMILSON COSTA',
            'ESCRITOR AUGUSTO CURY',
            'FLAVIO BOLSONARO',
            'HERTZ DIAS',
            'LULA',
            'PABLO MARÇAL',
            'RENAN SANTOS',
            'RONALDO CAIADO',
            'RUI COSTA PIMENTA',
            'SAMARA',
            'VETERINÁRIO WILSON GRASSI',
            'ZEMA'
        )
        ORDER BY
            NM_URNA_CANDIDATO
        """
    ).df()

    con.close()

    if len(candidatos) != 13:
        raise ValueError(
            f"Foram encontrados {len(candidatos)} candidatos "
            "na tabela candidatos. Esperado: 13."
        )

    df_propostas = pd.DataFrame(
        [
            {
                "NM_URNA_CANDIDATO": nome,
                "codigo_documento_tse": codigo,
                "url_proposta_governo": (
                    URL_BASE_TSE + codigo
                ),
                "fonte_proposta_governo": (
                    "Tribunal Superior Eleitoral "
                    "— DivulgaCandContas"
                ),
                "url_catalogo_tse": URL_CATALOGO_TSE,
                "tipo_documento": "PDF",
                "acesso_publico": True,
            }
            for nome, codigo in PROPOSTAS.items()
        ]
    )

    df_final = candidatos.merge(
        df_propostas,
        on="NM_URNA_CANDIDATO",
        how="left",
        validate="one_to_one"
    )

    if df_final["url_proposta_governo"].isna().any():
        faltantes = (
            df_final.loc[
                df_final["url_proposta_governo"].isna(),
                "NM_URNA_CANDIDATO"
            ]
            .tolist()
        )

        raise ValueError(
            "Existem candidatos sem proposta associada: "
            f"{faltantes}"
        )

    if df_final["url_proposta_governo"].duplicated().any():
        raise ValueError(
            "Existem URLs de propostas duplicadas."
        )

    df_final = df_final[
        [
            "SQ_CANDIDATO",
            "NM_URNA_CANDIDATO",
            "codigo_documento_tse",
            "url_proposta_governo",
            "fonte_proposta_governo",
            "url_catalogo_tse",
            "tipo_documento",
            "acesso_publico",
        ]
    ].copy()

    ARQUIVO_SAIDA.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df_final.to_csv(
        ARQUIVO_SAIDA,
        sep=";",
        encoding="utf-8-sig",
        index=False
    )

    print(
        f"Registros gravados: {len(df_final)}"
    )

    print(
        f"Propostas públicas: "
        f"{df_final['acesso_publico'].sum()}"
    )

    print(
        f"URLs únicas: "
        f"{df_final['url_proposta_governo'].nunique()}"
    )

    print(
        f"Arquivo: {ARQUIVO_SAIDA}"
    )

    print()

    print(
        df_final[
            [
                "NM_URNA_CANDIDATO",
                "codigo_documento_tse",
                "url_proposta_governo",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()