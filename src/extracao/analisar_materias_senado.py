from pathlib import Path

import json
import pandas as pd


ARQUIVO_MATERIAS = Path(
    "dados/processado/materias_senado_detalhado.csv"
)

ARQUIVO_STATUS = Path(
    "dados/processado/materias_senado_status.json"
)

ARQUIVO_SAIDA = Path(
    "dados/processado/materias_senado_final.csv"
)


df_materias = pd.read_csv(
    ARQUIVO_MATERIAS,
    sep=";",
    encoding="utf-8-sig",
    low_memory=False
)


with ARQUIVO_STATUS.open(
    "r",
    encoding="utf-8"
) as arquivo:
    dados_status = json.load(arquivo)


status_registros = []


for registro in dados_status:

    candidato = registro["candidato"]
    tramitando = registro["tramitando"]

    autorias = (
        registro["dados"]
        .get("MateriasAutoriaParlamentar", {})
        .get("Parlamentar", {})
        .get("Autorias", {})
        .get("Autoria", [])
    )

    if isinstance(autorias, dict):
        autorias = [autorias]

    for autoria in autorias:

        materia = autoria.get(
            "Materia",
            {}
        )

        status_registros.append(
            {
                "candidato": candidato,
                "codigo_materia": materia.get("Codigo"),
                "tramitando": tramitando,
            }
        )


df_status = pd.DataFrame(
    status_registros
)


df_status = df_status.drop_duplicates(
    subset=[
        "candidato",
        "codigo_materia",
        "tramitando"
    ]
)


df_status["codigo_materia"] = pd.to_numeric(
    df_status["codigo_materia"],
    errors="coerce"
)

df_materias["codigo_materia"] = pd.to_numeric(
    df_materias["codigo_materia"],
    errors="coerce"
)


df_status = (
    df_status
    .sort_values(
        ["candidato", "codigo_materia", "tramitando"]
    )
    .drop_duplicates(
        subset=[
            "candidato",
            "codigo_materia"
        ],
        keep="first"
    )
)


df_final = df_materias.merge(
    df_status,
    on=[
        "candidato",
        "codigo_materia"
    ],
    how="left"
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
    f"Matérias únicas: "
    f"{df_final['codigo_materia'].nunique()}"
)

print()
print(
    df_final.groupby(
        ["candidato", "tramitando"],
        dropna=False
    )
    .size()
    .to_string()
)

print()
print(
    f"Arquivo: {ARQUIVO_SAIDA}"
)