from pathlib import Path
import pandas as pd

arquivo = Path(
    "dados/selecionados/tse/bem_candidato_2026_BR.csv"
)

df = pd.read_csv(
    arquivo,
    sep=";",
    encoding="latin1",
    low_memory=False
)

tipos = (
    df["DS_TIPO_BEM_CANDIDATO"]
    .drop_duplicates()
    .sort_values()
)

for tipo in tipos:
    print(tipo)