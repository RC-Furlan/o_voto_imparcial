from pathlib import Path

import pandas as pd


PASTA_AUTORES = Path(
    "dados/bruto/camara/autores"
)

ARQUIVOS = sorted(
    PASTA_AUTORES.glob("proposicoesAutores-*.csv")
)


def normalizar_nome(nome: object) -> str:
    return (
        str(nome)
        .upper()
        .strip()
    )


NOMES_LULA = {
    "LUIZ INACIO LULA DA SILVA",
    "LUIZ INÁCIO LULA DA SILVA",
}

NOMES_CAIADO = {
    "RONALDO CAIADO",
    "RONALDO RAMOS CAIADO",
}


registros = []

for arquivo in ARQUIVOS:

    df = pd.read_csv(
        arquivo,
        sep=";",
        encoding="utf-8",
        quotechar='"',
        low_memory=False
    )

    df["nome_normalizado"] = df["nomeAutor"].map(
        normalizar_nome
    )

    filtro_lula = df["nome_normalizado"].isin(NOMES_LULA)
    filtro_caiado = df["nome_normalizado"].isin(NOMES_CAIADO)

    encontrados = df.loc[
        filtro_lula | filtro_caiado,
        [
            "idProposicao",
            "idDeputadoAutor",
            "nomeAutor",
            "siglaPartidoAutor",
            "siglaUFAutor",
            "ordemAssinatura",
            "proponente",
        ]
    ].copy()

    encontrados["ano"] = arquivo.stem.split("-")[-1]

    encontrados["candidato"] = ""

    encontrados.loc[
        encontrados["nomeAutor"].map(normalizar_nome).isin(NOMES_LULA),
        "candidato"
    ] = "LUIZ INÁCIO LULA DA SILVA"

    encontrados.loc[
        encontrados["nomeAutor"].map(normalizar_nome).isin(NOMES_CAIADO),
        "candidato"
    ] = "RONALDO CAIADO"

    registros.append(encontrados)


resultado = pd.concat(
    registros,
    ignore_index=True
)

resultado = resultado.drop_duplicates(
    subset=[
        "idProposicao",
        "idDeputadoAutor",
        "candidato"
    ]
)

ARQUIVO_SAIDA = Path(
    "dados/processado/autores_camara.csv"
)

ARQUIVO_SAIDA.parent.mkdir(
    parents=True,
    exist_ok=True
)

resultado.to_csv(
    ARQUIVO_SAIDA,
    sep=";",
    encoding="utf-8-sig",
    index=False
)

print(f"Registros gravados: {len(resultado)}")
print(f"Arquivo: {ARQUIVO_SAIDA}")