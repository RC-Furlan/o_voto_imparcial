from pathlib import Path

import pandas as pd


ARQUIVO = Path(
    "dados/bruto/camara/temas/proposicoesTemas-2026.csv"
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


df = pd.read_csv(
    ARQUIVO,
    sep=";",
    encoding="utf-8",
    quotechar='"',
    low_memory=False,
)


temas_oficiais = set(
    df["tema"]
    .dropna()
    .drop_duplicates()
)


temas_mapeados = {
    tema
    for temas in MAPEAMENTO_TEMAS.values()
    for tema in temas
}


nao_mapeados = sorted(
    temas_oficiais - temas_mapeados
)

duplicados = sorted(
    tema
    for tema in temas_mapeados
    if sum(tema in temas for temas in MAPEAMENTO_TEMAS.values()) > 1
)


print(f"Temas oficiais: {len(temas_oficiais)}")
print(f"Temas mapeados: {len(temas_mapeados)}")
print()

print("TEMAS NÃO MAPEADOS:")
if nao_mapeados:
    for tema in nao_mapeados:
        print(f"- {tema}")
else:
    print("Nenhum")

print()

print("TEMAS DUPLICADOS:")
if duplicados:
    for tema in duplicados:
        print(f"- {tema}")
else:
    print("Nenhum")