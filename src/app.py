from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st


ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)


st.set_page_config(
    page_title="O Voto Imparcial",
    layout="wide"
)


@st.cache_resource
def conectar_banco():
    return duckdb.connect(
        str(ARQUIVO_BANCO),
        read_only=True
    )


@st.cache_data
def carregar_candidatos():
    con = conectar_banco()

    return con.execute(
        """
        SELECT
            p.SQ_CANDIDATO,
            p.NM_CANDIDATO,
            p.NM_URNA_CANDIDATO,
            p.SG_PARTIDO,
            p.DS_GENERO,
            p.DS_COR_RACA,
            p.DS_GRAU_INSTRUCAO,
            p.DS_OCUPACAO,

            p.ST_DECLARAR_BENS,
            p.quantidade_bens,
            p.patrimonio_total,

            p.qtd_imoveis,
            p.valor_imoveis,

            p.qtd_veiculos,
            p.valor_veiculos,

            p.qtd_investimentos,
            p.valor_investimentos,

            p.qtd_participacoes,
            p.valor_participacoes,

            p.qtd_contas,
            p.valor_contas,

            p.qtd_bens_valor,
            p.valor_bens_valor,

            p.qtd_outros,
            p.valor_outros,

            p.projetos_camara,
            p.aprovados_camara,

            p.materias_senado,
            p.tramitando_senado,
            p.nao_tramitando_senado,

            c.possui_dados_patrimoniais,
            c.possui_dados_legislativos,

            c.status_dados_patrimoniais,
            c.status_dados_legislativos,

            c.fontes_legislativas,
            c.cobertura_geral

        FROM perfil_candidatos AS p

        LEFT JOIN cobertura_dados AS c
            ON p.SQ_CANDIDATO = c.SQ_CANDIDATO

        ORDER BY
            p.NM_URNA_CANDIDATO
        """
    ).df()


@st.cache_data
def carregar_bens(candidato_id):
    candidato_id = int(candidato_id)

    con = conectar_banco()

    return con.execute(
        """
        SELECT
            categoria,
            DS_TIPO_BEM_CANDIDATO,
            DS_BEM_CANDIDATO,
            VR_BEM_CANDIDATO
        FROM bens_candidatos_detalhados
        WHERE SQ_CANDIDATO = ?
        ORDER BY
            VR_BEM_CANDIDATO DESC
        """,
        [candidato_id]
    ).df()


@st.cache_data
def carregar_projetos_camara(candidato):
    candidato = str(candidato)

    con = conectar_banco()

    return con.execute(
        """
        SELECT
            idProposicao,
            siglaTipo,
            numero,
            ano,
            descricaoTipo,
            ementa,
            tema_principal,
            temas,
            aprovado,
            ultimoStatus_descricaoSituacao,
            ultimoStatus_descricaoTramitacao,
            urlInteiroTeor

        FROM projetos_camara

        WHERE candidato = ?

        ORDER BY
            ano DESC,
            numero DESC
        """,
        [candidato]
    ).df()


@st.cache_data
def carregar_materias_senado(candidato):
    candidato = str(candidato)

    mapa_candidatos = {
        "FLAVIO BOLSONARO": "FLAVIO_BOLSONARO",
        "RONALDO CAIADO": "RONALDO_CAIADO",
    }

    candidato_senado = mapa_candidatos.get(
        candidato
    )

    if candidato_senado is None:
        return pd.DataFrame()

    con = conectar_banco()

    return con.execute(
        """
        SELECT
            codigo_materia,
            identificacao_processo,
            descricao_identificacao,
            sigla,
            numero,
            ano,
            ementa,
            data,
            autor_principal,
            outros_autores,
            tramitando

        FROM materias_senado

        WHERE candidato = ?

        ORDER BY
            ano DESC,
            numero DESC
        """,
        [candidato_senado]
    ).df()


def moeda(valor):
    if pd.isna(valor):
        return "Não informado"

    return (
        f"R$ {float(valor):,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def inteiro(valor):
    if pd.isna(valor):
        return "Não informado"

    return f"{int(valor):,}".replace(",", ".")


def percentual(valor):
    if pd.isna(valor):
        return "Não informado"

    return f"{float(valor):.2f}%".replace(".", ",")


candidatos = carregar_candidatos()


st.title(
    "O Voto Imparcial"
)

st.caption(
    "Comparação factual de candidatos à Presidência da República "
    "com base nas fontes de dados coletadas pelo projeto."
)


candidato_selecionado = st.selectbox(
    "Selecione um candidato",
    candidatos["NM_URNA_CANDIDATO"].tolist()
)


candidato = candidatos[
    candidatos["NM_URNA_CANDIDATO"]
    == candidato_selecionado
].iloc[0]


candidato_id = int(
    candidato["SQ_CANDIDATO"]
)


st.divider()


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Partido",
        candidato["SG_PARTIDO"]
    )


with col2:
    st.metric(
        "Patrimônio declarado",
        moeda(candidato["patrimonio_total"])
    )


with col3:
    st.metric(
        "Quantidade de bens",
        inteiro(candidato["quantidade_bens"])
    )


with col4:
    st.metric(
        "Cobertura",
        str(candidato["cobertura_geral"])
    )


st.subheader(
    "Perfil do candidato"
)


perfil_coluna_1, perfil_coluna_2 = st.columns(2)


with perfil_coluna_1:

    st.write(
        f"**Nome completo:** "
        f"{candidato['NM_CANDIDATO']}"
    )

    st.write(
        f"**Gênero:** "
        f"{candidato['DS_GENERO']}"
    )

    st.write(
        f"**Cor/Raça:** "
        f"{candidato['DS_COR_RACA']}"
    )


with perfil_coluna_2:

    st.write(
        f"**Escolaridade:** "
        f"{candidato['DS_GRAU_INSTRUCAO']}"
    )

    st.write(
        f"**Ocupação:** "
        f"{candidato['DS_OCUPACAO']}"
    )

    st.write(
        f"**Dados patrimoniais:** "
        f"{candidato['status_dados_patrimoniais']}"
    )


st.divider()


tab_patrimonio, tab_legislativo, tab_cobertura = st.tabs(
    [
        "Patrimônio",
        "Atuação Legislativa",
        "Cobertura dos Dados",
    ]
)


with tab_patrimonio:

    st.subheader(
        "Patrimônio declarado"
    )

    possui_patrimonio = bool(
        candidato["possui_dados_patrimoniais"]
    )

    if possui_patrimonio:

        bens = carregar_bens(
            candidato_id
        )

        if not bens.empty:

            resumo = (
                bens
                .groupby(
                    "categoria",
                    as_index=False
                )["VR_BEM_CANDIDATO"]
                .sum()
                .sort_values(
                    "VR_BEM_CANDIDATO",
                    ascending=False
                )
            )

            resumo = resumo.rename(
                columns={
                    "VR_BEM_CANDIDATO": "valor"
                }
            )

            resumo_display = resumo.copy()

            resumo_display["valor"] = (
                resumo_display["valor"]
                .map(moeda)
            )

            resumo_display = resumo_display.rename(
                columns={
                    "categoria": "Categoria",
                    "valor": "Valor",
                }
            )

            st.dataframe(
                resumo_display,
                use_container_width=True,
                hide_index=True
            )

            st.subheader(
                "Bens declarados"
            )

            bens_display = bens.copy()

            bens_display[
                "VR_BEM_CANDIDATO"
            ] = (
                bens_display[
                    "VR_BEM_CANDIDATO"
                ].map(moeda)
            )

            bens_display = bens_display.rename(
                columns={
                    "categoria": "Categoria",
                    "DS_TIPO_BEM_CANDIDATO": "Tipo",
                    "DS_BEM_CANDIDATO": "Descrição",
                    "VR_BEM_CANDIDATO": "Valor",
                }
            )

            st.dataframe(
                bens_display[
                    [
                        "Categoria",
                        "Tipo",
                        "Descrição",
                        "Valor",
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Não foram encontrados bens detalhados "
                "para este candidato."
            )

    else:

        st.info(
            "Não há dados patrimoniais disponíveis "
            "na base coletada para este candidato."
        )


with tab_legislativo:

    st.subheader(
        "Atuação Legislativa"
    )

    possui_legislativo = bool(
        candidato["possui_dados_legislativos"]
    )

    if possui_legislativo:

        fonte = candidato[
            "fontes_legislativas"
        ]

        if pd.notna(fonte):

            st.caption(
                f"Fontes disponíveis: {fonte}"
            )


        camara_coluna, senado_coluna = st.columns(2)


        with camara_coluna:

            st.markdown(
                "**Câmara dos Deputados**"
            )

            projetos_camara = candidato[
                "projetos_camara"
            ]

            aprovados_camara = candidato[
                "aprovados_camara"
            ]

            if pd.isna(projetos_camara):

                st.info(
                    "Sem dados da Câmara disponíveis "
                    "na cobertura atual."
                )

            else:

                st.metric(
                    "Projetos encontrados",
                    inteiro(projetos_camara)
                )

                st.metric(
                    "Aprovação identificada",
                    inteiro(aprovados_camara)
                )

                if (
                    float(projetos_camara) > 0
                    and not pd.isna(aprovados_camara)
                ):

                    taxa = (
                        float(aprovados_camara)
                        / float(projetos_camara)
                        * 100
                    )

                    st.metric(
                        "Taxa de aprovação",
                        percentual(taxa)
                    )


        with senado_coluna:

            st.markdown(
                "**Senado Federal**"
            )

            materias_senado = candidato[
                "materias_senado"
            ]

            tramitando_senado = candidato[
                "tramitando_senado"
            ]

            nao_tramitando_senado = candidato[
                "nao_tramitando_senado"
            ]

            if pd.isna(materias_senado):

                st.info(
                    "Sem dados do Senado disponíveis "
                    "na cobertura atual."
                )

            else:

                st.metric(
                    "Matérias encontradas",
                    inteiro(materias_senado)
                )

                st.metric(
                    "Em tramitação",
                    inteiro(tramitando_senado)
                )

                st.metric(
                    "Fora de tramitação",
                    inteiro(nao_tramitando_senado)
                )


        st.divider()


        projetos = carregar_projetos_camara(
            candidato_selecionado
        )

        materias = carregar_materias_senado(
            candidato_selecionado
        )


        if not projetos.empty:

            st.subheader(
                "Projetos na Câmara"
            )

            projetos_display = projetos[
                [
                    "siglaTipo",
                    "numero",
                    "ano",
                    "descricaoTipo",
                    "tema_principal",
                    "aprovado",
                    "ultimoStatus_descricaoSituacao",
                    "ementa",
                ]
            ].copy()

            projetos_display = projetos_display.rename(
                columns={
                    "siglaTipo": "Tipo",
                    "numero": "Número",
                    "ano": "Ano",
                    "descricaoTipo": "Descrição",
                    "tema_principal": "Tema principal",
                    "aprovado": "Aprovação identificada",
                    "ultimoStatus_descricaoSituacao": "Situação",
                    "ementa": "Ementa",
                }
            )

            st.dataframe(
                projetos_display,
                use_container_width=True,
                hide_index=True
            )


        if not materias.empty:

            st.subheader(
                "Matérias no Senado"
            )

            materias_display = materias[
                [
                    "descricao_identificacao",
                    "sigla",
                    "numero",
                    "ano",
                    "ementa",
                    "autor_principal",
                    "tramitando",
                ]
            ].copy()

            materias_display = materias_display.rename(
                columns={
                    "descricao_identificacao": "Identificação",
                    "sigla": "Tipo",
                    "numero": "Número",
                    "ano": "Ano",
                    "ementa": "Ementa",
                    "autor_principal": "Autor principal",
                    "tramitando": "Tramitando",
                }
            )

            st.dataframe(
                materias_display,
                use_container_width=True,
                hide_index=True
            )

    else:

        st.info(
            "Não há dados legislativos disponíveis "
            "na base coletada para este candidato."
        )


with tab_cobertura:

    st.subheader(
        "Cobertura e limitações"
    )

    st.write(
        f"**Patrimônio:** "
        f"{candidato['status_dados_patrimoniais']}"
    )

    st.write(
        f"**Legislativo:** "
        f"{candidato['status_dados_legislativos']}"
    )

    if pd.notna(
        candidato["fontes_legislativas"]
    ):

        st.write(
            f"**Fontes legislativas:** "
            f"{candidato['fontes_legislativas']}"
        )

    st.warning(
        "A ausência de dados legislativos nesta aplicação "
        "significa que não foram encontrados registros nas "
        "fontes e períodos coletados pelo projeto. Isso não "
        "deve ser interpretado como prova de ausência de "
        "atuação legislativa."
    )

    st.write(
        "Os indicadores apresentados são descritivos. "
        "O projeto não atribui nota, mérito ou recomendação "
        "eleitoral aos candidatos."
    )


st.divider()


st.caption(
    "O Voto Imparcial — análise baseada exclusivamente "
    "nos dados disponíveis nas fontes incorporadas ao projeto."
)