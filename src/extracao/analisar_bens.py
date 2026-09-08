from pathlib import Path
import pandas as pd

ARQUIVO_BENS = Path(
    "dados/selecionados/tse/bem_candidato_2026_BR.csv"
)

df = pd.read_csv(
    ARQUIVO_BENS,
    sep=";",
    encoding="latin1",
    low_memory=False
)

print("\nTIPOS DE BENS\n")
print(
    df["DS_TIPO_BEM_CANDIDATO"]
    .value_counts()
    .sort_values(ascending=False)
    .to_string()
)