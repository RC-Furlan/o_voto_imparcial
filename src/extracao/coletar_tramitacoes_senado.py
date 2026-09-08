from pathlib import Path

import json
import time

import pandas as pd
import requests


ARQUIVO_ENTRADA = Path(
    "dados/processado/materias_senado.csv"
)

ARQUIVO_SAIDA = Path(
    "dados/processado/materias_senado_situacao.csv"
)

URL_SITUACAO = (
    "https://legis.senado.leg.br/dadosabertos/"
    "materia/situacaoatual/{codigo}.json"
)


df = pd.read_csv(
    ARQUIVO_ENTRADA,
    sep=";",
    encoding="utf-8-sig",
    low_memory=False
)


sessao = requests.Session()

registros = []

total = len(df)

for indice, linha in df.iterrows():

    codigo = int(linha["codigo_materia"])

    print(
        f"Consultando matéria "
        f"{indice + 1}/{total}: {codigo}"
    )

    url = URL_SITUACAO.format(
        codigo=codigo
    )

    resposta = sessao.get(
        url,
        timeout=60
    )

    if resposta.status_code == 404:
        registros.append(
            {
                "candidato": linha["candidato"],
                "codigo_materia": codigo,
                "dados_situacao": "",
            }
        )

        time.sleep(1)
        continue

    if resposta.status_code == 429:
        print(
            "Limite da API atingido. "
            "Aguardando 30 segundos..."
        )

        time.sleep(30)

        resposta = sessao.get(
            url,
            timeout=60
        )

    resposta.raise_for_status()

    dados = resposta.json()

    registros.append(
        {
            "candidato": linha["candidato"],
            "codigo_materia": codigo,
            "dados_situacao": json.dumps(
                dados,
                ensure_ascii=False
            ),
        }
    )

    time.sleep(1)


resultado = pd.DataFrame(
    registros
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


print()
print(
    f"Registros gravados: {len(resultado)}"
)

print(
    f"Matérias com situação: "
    f"{(resultado['dados_situacao'].str.len() > 0).sum()}"
)

print(
    f"Arquivo: {ARQUIVO_SAIDA}"
)