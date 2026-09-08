from pathlib import Path

import duckdb
import pandas as pd


ARQUIVO_CSV = Path(
    "dados/selecionados/tse/bem_candidato_2026_BR.csv"
)

ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)


df = pd.read_csv(
    ARQUIVO_CSV,
    sep=";",
    encoding="latin1",
    low_memory=False
)


df = df[
    [
        "SQ_CANDIDATO",
        "NR_ORDEM_BEM_CANDIDATO",
        "CD_TIPO_BEM_CANDIDATO",
        "DS_TIPO_BEM_CANDIDATO",
        "DS_BEM_CANDIDATO",
        "VR_BEM_CANDIDATO",
    ]
].copy()


df["VR_BEM_CANDIDATO"] = (
    df["VR_BEM_CANDIDATO"]
    .astype(str)
    .str.replace(",", ".", regex=False)
)

df["VR_BEM_CANDIDATO"] = pd.to_numeric(
    df["VR_BEM_CANDIDATO"],
    errors="coerce"
).fillna(0)


mapa_categorias = {
    "IMOVEIS": [
        "Apartamento",
        "Casa",
        "Construção",
        "Outros bens imóveis",
        "Prédio comercial",
        "Prédio residencial",
        "Sala ou conjunto",
        "Terreno",
    ],
    "VEICULOS": [
        "Veículo automotor terrestre: caminhão, automóvel, moto, etc.",
    ],
    "INVESTIMENTOS": [
        "Aplicação de renda fixa (CDB, RDB e outros)",
        "Ações (inclusive as provenientes de linha telefônica)",
        "Caderneta de poupança",
        "Fundo de Curto Prazo",
        "Fundo de Investimento Imobiliário",
        "Fundo de Longo Prazo e Fundo de Investimentos em Direitos Creditórios (FIDC)",
        "Fundos: Ações, Mútuos de Privatização, Invest. Empresas Emergentes, Invest.Participação e Invest. Índice Mercado",
        "Outras aplicações e Investimentos",
        "Outros fundos",
        "VGBL - Vida Gerador de Benefício Livre",
    ],
    "PARTICIPACOES_EMPRESARIAIS": [
        "Outras participações societárias",
        "Quotas ou quinhões de capital",
    ],
    "CONTAS_E_DISPONIBILIDADES": [
        "Crédito decorrente de alienação",
        "Depósito bancário em conta corrente no País",
        "Depósito bancário em conta corrente no exterior",
        "Outros créditos e poupança vinculados",
    ],
    "BENS_DE_VALOR": [
        "Jóia, quadro, objeto de arte, de coleção, antiguidade, etc.",
        "Título de clube e assemelhado",
    ],
    "OUTROS": [
        "Bem relacionado com o exercício da atividade autônoma",
        "OUTROS BENS E DIREITOS",
        "Outros bens móveis",
    ],
}


tipo_para_categoria = {
    tipo: categoria
    for categoria, tipos in mapa_categorias.items()
    for tipo in tipos
}


df["categoria"] = df["DS_TIPO_BEM_CANDIDATO"].map(
    tipo_para_categoria
)

df["categoria"] = df["categoria"].fillna("OUTROS")


con = duckdb.connect(
    str(ARQUIVO_BANCO)
)


con.execute(
    """
    DROP TABLE IF EXISTS bens_candidatos
    """
)


con.register(
    "df_bens",
    df
)


con.execute(
    """
    CREATE TABLE bens_candidatos AS
    SELECT *
    FROM df_bens
    """
)


registros = con.execute(
    """
    SELECT COUNT(*)
    FROM bens_candidatos
    """
).fetchone()[0]


candidatos = con.execute(
    """
    SELECT COUNT(DISTINCT SQ_CANDIDATO)
    FROM bens_candidatos
    """
).fetchone()[0]


con.close()


print(
    f"Registros carregados: {registros}"
)

print(
    f"Candidatos com bens: {candidatos}"
)