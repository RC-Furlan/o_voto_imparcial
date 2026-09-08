from pathlib import Path
import pandas as pd

ARQUIVO = Path(
    "dados/selecionados/tse/consulta_cand_2026_BR.csv"
)

df = pd.read_csv(
    ARQUIVO,
    sep=";",
    encoding="latin1",
    low_memory=False
)

colunas = [
    "SQ_CANDIDATO",
    "NM_CANDIDATO",
    "NM_URNA_CANDIDATO",
    "DS_CARGO",
    "SG_PARTIDO",
    "DS_GENERO",
    "DS_COR_RACA",
    "DS_GRAU_INSTRUCAO",
    "DS_OCUPACAO"
]

print(df[colunas].to_string(index=False))
