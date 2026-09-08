from pathlib import Path

import pandas as pd


ARQUIVO_PROJETOS = Path(
    "dados/processado/projetos_camara_final.csv"
)

ARQUIVO_SAIDA = Path(
    "dados/analitico/indicadores_camara.csv"
)


MAPEAMENTO_TEMAS = {
    "ADMINISTRACAO_PUBLICA": [
        "Administração Pública",
        "Processo Legislativo e Atuação Parlamentar",
    ],
    "AGRICULTURA": [
        "Agricultura, Pecuária, Pesca e Extrativismo",
        "Estrutura Fundiária",
    ],
    "CULTURA": [
        "Arte, Cultura e Religião",
        "Esporte e Lazer",
        "Turismo",
    ],
    "DESENVOLVIMENTO_URBANO": [
        "Cidades e Desenvolvimento Urbano",
    ],
    "CIENCIA_E_TECNOLOGIA": [
        "Ciência, Tecnologia e Inovação",
        "Ciências Exatas e da Terra",
    ],
    "CIENCIAS_HUMANAS": [
        "Ciências Sociais e Humanas",
    ],
    "COMUNICACOES": [
        "Comunicações",
    ],
    "DEFESA_E_SEGURANCA": [
        "Defesa e Segurança",
    ],
    "DIREITO": [
        "Direito Civil e Processual Civil",
        "Direito Constitucional",
        "Direito Penal e Processual Penal",
        "Direito e Defesa do Consumidor",
        "Direito e Justiça",
    ],
    "DIREITOS_HUMANOS": [
        "Direitos Humanos e Minorias",
    ],
    "ECONOMIA": [
        "Economia",
        "Indústria, Comércio e Serviços",
    ],
    "EDUCACAO": [
        "Educação",
    ],
    "ENERGIA_E_RECURSOS": [
        "Energia, Recursos Hídricos e Minerais",
    ],
    "FINANCAS_PUBLICAS": [
        "Finanças Públicas e Orçamento",
    ],
    "MEIO_AMBIENTE": [
        "Meio Ambiente e Desenvolvimento Sustentável",
    ],
    "POLITICA_E_ELEICOES": [
        "Política, Partidos e Eleições",
    ],
    "PREVIDENCIA_E_ASSISTENCIA": [
        "Previdência e Assistência Social",
    ],
    "RELACOES_INTERNACIONAIS": [
        "Relações Internacionais e Comércio Exterior",
    ],
    "SAUDE": [
        "Saúde",
    ],
    "TRABALHO": [
        "Trabalho e Emprego",
    ],
    "TRANSPORTE": [
        "Viação, Transporte e Mobilidade",
    ],
    "OUTROS": [
        "Homenagens e Datas Comemorativas",
    ],
}


def classificar_tema(tema: str) -> str:
    if not tema:
        return "OUTROS"

    for setor, temas in MAPEAMENTO_TEMAS.items():
        if tema in temas:
            return setor

    return "OUTROS"


df = pd.read_csv(
    ARQUIVO_PROJETOS,
    sep=";",
    encoding="utf-8-sig",
    quotechar='"',
    low_memory=False,
)

df["tema_principal"] = (
    df["tema_principal"]
    .fillna("")
    .astype(str)
    .str.strip()
)

df["setor"] = df["tema_principal"].apply(
    classificar_tema
)


indicadores = (
    df.groupby(
        ["candidato", "setor"],
        as_index=False
    )
    .agg(
        projetos_apresentados=(
            "idProposicao",
            "nunique"
        ),
        projetos_aprovados=(
            "aprovado",
            "sum"
        ),
    )
)


ARQUIVO_SAIDA.parent.mkdir(
    parents=True,
    exist_ok=True
)

indicadores.to_csv(
    ARQUIVO_SAIDA,
    sep=";",
    encoding="utf-8-sig",
    index=False
)

print(
    f"Registros gravados: {len(indicadores)}"
)

print(
    f"Arquivo: {ARQUIVO_SAIDA}"
)