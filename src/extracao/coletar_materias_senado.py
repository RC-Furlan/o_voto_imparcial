from pathlib import Path

import json

import requests


URL = (
    "https://legis.senado.leg.br/dadosabertos/"
    "senador/{codigo}/autorias.json"
)


PARLAMENTARES = {
    "FLAVIO_BOLSONARO": 5894,
    "RONALDO_CAIADO": 456,
}


ARQUIVO_SAIDA = Path(
    "dados/processado/materias_senado_status.json"
)


resultados = []


for candidato, codigo in PARLAMENTARES.items():

    print(
        f"\nConsultando {candidato}..."
    )

    for tramitando in ["S", "N"]:

        print(
            f"  tramitando={tramitando}"
        )

        resposta = requests.get(
            URL.format(codigo=codigo),
            params={
                "tramitando": tramitando,
                "primeiro": "T",
            },
            timeout=60
        )

        resposta.raise_for_status()

        dados = resposta.json()

        autorias = (
            dados
            .get("MateriasAutoriaParlamentar", {})
            .get("Parlamentar", {})
            .get("Autorias", {})
            .get("Autoria", [])
        )

        if isinstance(autorias, dict):
            autorias = [autorias]

        resultados.append(
            {
                "candidato": candidato,
                "codigoParlamentar": codigo,
                "tramitando": tramitando,
                "quantidade": len(autorias),
                "dados": dados,
            }
        )


ARQUIVO_SAIDA.parent.mkdir(
    parents=True,
    exist_ok=True
)


with ARQUIVO_SAIDA.open(
    "w",
    encoding="utf-8"
) as arquivo:

    json.dump(
        resultados,
        arquivo,
        ensure_ascii=False,
        indent=2
    )


print("\nRESULTADO")

for resultado in resultados:

    print(
        f"{resultado['candidato']} | "
        f"tramitando={resultado['tramitando']} | "
        f"{resultado['quantidade']} matérias"
    )

print()
print(
    f"Arquivo: {ARQUIVO_SAIDA}"
)