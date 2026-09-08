from pathlib import Path

import pandas as pd

ARQUIVO_CANDIDATOS = Path(
    "dados/processado/candidatos_presidencia.csv"
)

ARQUIVO_BENS = Path(
    "dados/selecionados/tse/bem_candidato_2026_BR.csv"
)

ARQUIVO_SAIDA = Path(
    "dados/analitico/perfis_candidatos.csv"
)

ARQUIVO_SAIDA.parent.mkdir(parents=True, exist_ok=True)

MAPEAMENTO_CATEGORIAS = {
    "IMOVEIS": [
        "Apartamento",
        "Casa",
        "Construção",
        "Outros bens imóveis",
        "Prédio comercial",
        "Prédio residencial",
        "Sala ou conjunto",
        "Terreno"
    ],
    "VEICULOS": [
        "Veículo automotor terrestre: caminhão, automóvel, moto, etc."
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
        "VGBL - Vida Gerador de Benefício Livre"
    ],
    "PARTICIPACOES_EMPRESARIAIS": [
        "Outras participações societárias",
        "Quotas ou quinhões de capital"
    ],
    "CONTAS_E_DISPONIBILIDADES": [
        "Crédito decorrente de alienação",
        "Depósito bancário em conta corrente no País",
        "Depósito bancário em conta corrente no exterior",
        "Outros créditos e poupança vinculados"
    ],
    "BENS_DE_VALOR": [
        "Jóia, quadro, objeto de arte, de coleção, antiguidade, etc.",
        "Título de clube e assemelhado"
    ],
    "OUTROS": [
        "Bem relacionado com o exercício da atividade autônoma",
        "OUTROS BENS E DIREITOS",
        "Outros bens móveis"
    ]
}

COLUNAS_CATEGORIAS = {
    "IMOVEIS": ("qtd_imoveis", "valor_imoveis"),
    "VEICULOS": ("qtd_veiculos", "valor_veiculos"),
    "INVESTIMENTOS": ("qtd_investimentos", "valor_investimentos"),
    "PARTICIPACOES_EMPRESARIAIS": ("qtd_participacoes", "valor_participacoes"),
    "CONTAS_E_DISPONIBILIDADES": ("qtd_contas", "valor_contas"),
    "BENS_DE_VALOR": ("qtd_bens_valor", "valor_bens_valor"),
    "OUTROS": ("qtd_outros", "valor_outros")
}

df_candidatos = pd.read_csv(
    ARQUIVO_CANDIDATOS,
    sep=";",
    encoding="utf-8-sig"
)

df_bens = pd.read_csv(
    ARQUIVO_BENS,
    sep=";",
    encoding="latin1",
    low_memory=False
)

df_bens["VR_BEM_CANDIDATO"] = (
    df_bens["VR_BEM_CANDIDATO"]
    .astype(str)
    .str.replace(",", ".", regex=False)
)

df_bens["VR_BEM_CANDIDATO"] = pd.to_numeric(
    df_bens["VR_BEM_CANDIDATO"],
    errors="coerce"
).fillna(0)

for categoria, tipos in MAPEAMENTO_CATEGORIAS.items():

    qtd_coluna, valor_coluna = COLUNAS_CATEGORIAS[categoria]

    resumo = (
        df_bens[
            df_bens["DS_TIPO_BEM_CANDIDATO"].isin(tipos)
        ]
        .groupby("SQ_CANDIDATO")
        .agg(
            **{
                qtd_coluna: ("NR_ORDEM_BEM_CANDIDATO", "count"),
                valor_coluna: ("VR_BEM_CANDIDATO", "sum")
            }
        )
        .reset_index()
    )

    df_candidatos = df_candidatos.merge(
        resumo,
        on="SQ_CANDIDATO",
        how="left"
    )

for _, (qtd_coluna, valor_coluna) in COLUNAS_CATEGORIAS.items():

    df_candidatos[qtd_coluna] = (
        df_candidatos[qtd_coluna]
        .fillna(0)
        .astype(int)
    )

    df_candidatos[valor_coluna] = (
        df_candidatos[valor_coluna]
        .fillna(0)
    )

df_candidatos.to_csv(
    ARQUIVO_SAIDA,
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print(f"Arquivo gerado: {ARQUIVO_SAIDA}")
print(f"Quantidade de registros: {len(df_candidatos)}")
print(f"Quantidade de colunas: {len(df_candidatos.columns)}")