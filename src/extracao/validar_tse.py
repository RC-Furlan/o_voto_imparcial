from pathlib import Path
import pandas as pd

ARQUIVO_CANDIDATOS = Path(
    "dados/selecionados/tse/consulta_cand_2026_BR.csv"
)

ARQUIVO_CANDIDATOS_COMPLEMENTAR = Path(
    "dados/selecionados/tse/consulta_cand_complementar_2026_BR.csv"
)

ARQUIVO_BENS = Path(
    "dados/selecionados/tse/bem_candidato_2026_BR.csv"
)

df_candidatos = pd.read_csv(
    ARQUIVO_CANDIDATOS,
    sep=";",
    encoding="latin1",
    low_memory=False
)

df_candidatos_complementar = pd.read_csv(
    ARQUIVO_CANDIDATOS_COMPLEMENTAR,
    sep=";",
    encoding="latin1",
    low_memory=False
)

df_bens = pd.read_csv(
    ARQUIVO_BENS,
    sep=";",
    encoding="latin1",
    low_memory=False
)

print("\n=== CANDIDATOS ===")
print(df_candidatos.shape)
print(df_candidatos.columns.tolist())

print("\n=== CANDIDATOS COMPLEMENTAR ===")
print(df_candidatos_complementar.shape)
print(df_candidatos_complementar.columns.tolist())

print("\n=== BENS ===")
print(df_bens.shape)
print(df_bens.columns.tolist())