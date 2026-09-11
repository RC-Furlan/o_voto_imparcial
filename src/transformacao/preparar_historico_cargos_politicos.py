from pathlib import Path

import duckdb
import pandas as pd


ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)

ARQUIVO_SAIDA = Path(
    "dados/processado/historico_cargos_politicos.csv"
)


CARGOS = [
    {
        "NM_URNA_CANDIDATO": "LULA",
        "cargo": "Deputado Federal",
        "esfera": "Federal",
        "localidade": "São Paulo",
        "inicio": "1987-02-01",
        "fim": "1991-01-31",
        "situacao": "Encerrado",
        "fonte": (
            "Câmara dos Deputados — Biografia "
            "Luiz Inácio Lula da Silva"
        ),
        "url_fonte": (
            "https://www.camara.leg.br/"
            "deputados/139289/biografia"
        ),
    },
    {
        "NM_URNA_CANDIDATO": "LULA",
        "cargo": "Presidente da República",
        "esfera": "Federal",
        "localidade": "Brasil",
        "inicio": "2003-01-01",
        "fim": "2007-01-01",
        "situacao": "Encerrado",
        "fonte": (
            "Biblioteca da Presidência da República"
        ),
        "url_fonte": (
            "https://biblioteca.presidencia.gov.br/"
            "presidencia/ex-presidentes/"
            "luiz-inacio-lula-da-silva/biografia"
        ),
    },
    {
        "NM_URNA_CANDIDATO": "LULA",
        "cargo": "Presidente da República",
        "esfera": "Federal",
        "localidade": "Brasil",
        "inicio": "2007-01-01",
        "fim": "2011-01-01",
        "situacao": "Encerrado",
        "fonte": (
            "Biblioteca da Presidência da República"
        ),
        "url_fonte": (
            "https://biblioteca.presidencia.gov.br/"
            "presidencia/ex-presidentes/"
            "luiz-inacio-lula-da-silva/biografia"
        ),
    },
    {
        "NM_URNA_CANDIDATO": "LULA",
        "cargo": "Presidente da República",
        "esfera": "Federal",
        "localidade": "Brasil",
        "inicio": "2023-01-01",
        "fim": None,
        "situacao": "Em exercício",
        "fonte": (
            "Governo Federal — Presidência da República"
        ),
        "url_fonte": (
            "https://www.gov.br/planalto/pt-br/"
            "acompanhe-o-planalto"
        ),
    },
    {
        "NM_URNA_CANDIDATO": "FLAVIO BOLSONARO",
        "cargo": "Deputado Estadual",
        "esfera": "Estadual",
        "localidade": "Rio de Janeiro",
        "inicio": "2003-02-01",
        "fim": "2019-01-31",
        "situacao": "Encerrado",
        "fonte": (
            "Senado Federal — Trajetória política"
        ),
        "url_fonte": (
            "https://www12.senado.leg.br/"
            "noticias/materias/2019/01/18/"
            "flavio-bolsonaro-psl"
        ),
    },
    {
        "NM_URNA_CANDIDATO": "FLAVIO BOLSONARO",
        "cargo": "Senador",
        "esfera": "Federal",
        "localidade": "Rio de Janeiro",
        "inicio": "2019-02-01",
        "fim": "2027-01-31",
        "situacao": "Em exercício",
        "fonte": (
            "Senado Federal — Perfil parlamentar"
        ),
        "url_fonte": (
            "https://www25.senado.leg.br/"
            "web/senadores/senador/-/perfil/5894"
        ),
    },
    {
        "NM_URNA_CANDIDATO": "RONALDO CAIADO",
        "cargo": "Deputado Federal",
        "esfera": "Federal",
        "localidade": "Goiás",
        "inicio": "1991-02-01",
        "fim": "1995-01-31",
        "situacao": "Encerrado",
        "fonte": (
            "Câmara dos Deputados — Biografia"
        ),
        "url_fonte": (
            "https://www.camara.leg.br/"
            "deputados/74813/biografia"
        ),
    },
    {
        "NM_URNA_CANDIDATO": "RONALDO CAIADO",
        "cargo": "Deputado Federal",
        "esfera": "Federal",
        "localidade": "Goiás",
        "inicio": "1999-02-01",
        "fim": "2015-01-31",
        "situacao": "Encerrado",
        "fonte": (
            "Câmara dos Deputados — Biografia"
        ),
        "url_fonte": (
            "https://www.camara.leg.br/"
            "deputados/74813/biografia"
        ),
    },
    {
        "NM_URNA_CANDIDATO": "RONALDO CAIADO",
        "cargo": "Senador",
        "esfera": "Federal",
        "localidade": "Goiás",
        "inicio": "2015-02-01",
        "fim": "2019-01-31",
        "situacao": "Encerrado",
        "fonte": (
            "Câmara dos Deputados — Biografia"
        ),
        "url_fonte": (
            "https://www.camara.leg.br/"
            "deputados/74813/biografia"
        ),
    },
    {
        "NM_URNA_CANDIDATO": "RONALDO CAIADO",
        "cargo": "Governador",
        "esfera": "Estadual",
        "localidade": "Goiás",
        "inicio": "2019-01-01",
        "fim": "2026-03-31",
        "situacao": "Encerrado",
        "fonte": (
            "Governo de Goiás — Governantes do Estado"
        ),
        "url_fonte": (
            "https://goias.gov.br/casacivil/"
            "governantes-republica/"
        ),
    },
    {
        "NM_URNA_CANDIDATO": "ZEMA",
        "cargo": "Governador",
        "esfera": "Estadual",
        "localidade": "Minas Gerais",
        "inicio": "2019-01-01",
        "fim": "2022-12-31",
        "situacao": "Encerrado",
        "fonte": (
            "Portal MG — Romeu Zema Neto"
        ),
        "url_fonte": (
            "https://www.mg.gov.br/"
            "governador/romeu-zema-neto"
        ),
    },
    {
        "NM_URNA_CANDIDATO": "ZEMA",
        "cargo": "Governador",
        "esfera": "Estadual",
        "localidade": "Minas Gerais",
        "inicio": "2023-01-01",
        "fim": "2026-03-21",
        "situacao": "Encerrado",
        "fonte": (
            "Portal MG — Romeu Zema Neto"
        ),
        "url_fonte": (
            "https://www.mg.gov.br/"
            "governador/romeu-zema-neto"
        ),
    },
]


def main() -> None:

    con = duckdb.connect(
        str(ARQUIVO_BANCO),
        read_only=True
    )

    candidatos = con.execute(
        """
        SELECT
            SQ_CANDIDATO,
            NM_URNA_CANDIDATO
        FROM candidatos
        """
    ).df()

    con.close()

    df_cargos = pd.DataFrame(
        CARGOS
    )

    if df_cargos.empty:
        raise ValueError(
            "Nenhum cargo político foi configurado."
        )

    df_final = candidatos.merge(
        df_cargos,
        on="NM_URNA_CANDIDATO",
        how="inner",
        validate="one_to_many"
    )

    if df_final.empty:
        raise ValueError(
            "Nenhum cargo pôde ser relacionado "
            "aos candidatos."
        )

    df_final = df_final[
        [
            "SQ_CANDIDATO",
            "NM_URNA_CANDIDATO",
            "cargo",
            "esfera",
            "localidade",
            "inicio",
            "fim",
            "situacao",
            "fonte",
            "url_fonte",
        ]
    ].copy()

    df_final = df_final.drop_duplicates(
        subset=[
            "SQ_CANDIDATO",
            "cargo",
            "inicio",
            "fim",
        ]
    )

    ARQUIVO_SAIDA.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df_final.to_csv(
        ARQUIVO_SAIDA,
        sep=";",
        encoding="utf-8-sig",
        index=False
    )

    print(
        f"Registros gravados: {len(df_final)}"
    )

    print(
        f"Candidatos com cargos: "
        f"{df_final['SQ_CANDIDATO'].nunique()}"
    )

    print()

    print(
        df_final[
            [
                "NM_URNA_CANDIDATO",
                "cargo",
                "esfera",
                "localidade",
                "inicio",
                "fim",
                "situacao",
            ]
        ].to_string(index=False)
    )

    print()
    print(
        f"Arquivo: {ARQUIVO_SAIDA}"
    )


if __name__ == "__main__":
    main()