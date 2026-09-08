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

print(df.shape)
print(df.columns.tolist())