from pathlib import Path

import pandas as pd


ARQUIVO = Path(
    "dados/bruto/camara/temas/proposicoesTemas-2026.csv"
)


df = pd.read_csv(
    ARQUIVO,
    sep=";",
    encoding="utf-8",
    quotechar='"',
    low_memory=False
)


temas = (
    df["tema"]
    .dropna()
    .drop_duplicates()
    .sort_values()
)


print(f"Quantidade de temas: {len(temas)}")
print()

for tema in temas:
    print(tema)