from pathlib import Path
from random import SystemRandom
from textwrap import dedent
from html import escape
import base64
import re

import duckdb
import pandas as pd
import streamlit as st


# ============================================================
# CAMINHOS
# ============================================================

RAIZ_PROJETO = Path(__file__).resolve().parent.parent

ARQUIVO_BANCO = (
    RAIZ_PROJETO
    / "banco"
    / "voto_imparcial.duckdb"
)

ARQUIVO_BANNER = (
    RAIZ_PROJETO
    / "OVotoImparcial_Banner-01.png"
)

ARQUIVO_MAPA = (
    RAIZ_PROJETO
    / "Mapa_Candidatos-01.svg"
)


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="O Voto Imparcial",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# RENDERIZAÇÃO
# ============================================================

def render_html(conteudo: str):
    st.html(dedent(conteudo).strip())


# ============================================================
# RECURSOS VISUAIS
# ============================================================

def carregar_banner_base64():
    if not ARQUIVO_BANNER.exists():
        return None

    try:
        return base64.b64encode(
            ARQUIVO_BANNER.read_bytes()
        ).decode("utf-8")
    except OSError:
        return None


def carregar_svg_mapa():
    if not ARQUIVO_MAPA.exists():
        return None

    try:
        svg = ARQUIVO_MAPA.read_text(encoding="utf-8")

        # Remove o fundo branco do arquivo original.
        svg = re.sub(
            r'<g id="Background">.*?</g>',
            '',
            svg,
            flags=re.DOTALL,
        )

        svg = svg.replace(
            '.st0{fill:#F5F7F7;}',
            '.st0{fill:none;}',
        )

        return svg
    except (OSError, UnicodeError):
        return None


def svg_mapa_data_uri(svg_base, cor):
    if svg_base is None:
        return None

    svg = svg_base.replace(
        '#3D9143',
        cor,
    )

    return (
        'data:image/svg+xml;base64,'
        + base64.b64encode(
            svg.encode("utf-8")
        ).decode("utf-8")
    )


BANNER_BASE64 = carregar_banner_base64()
MAPA_SVG_BASE = carregar_svg_mapa()


# ============================================================
# CSS
# ============================================================

render_html(
    """
    <style>

    html,
    body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    [data-testid="stMain"] {
        background: #0b1220 !important;
        color: #f2f4f7 !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    [data-testid="stToolbar"] {
        display: none;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    [data-testid="block-container"] {
        max-width: 1380px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    p,
    span,
    label,
    div {
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }

    h1,
    h2,
    h3 {
        color: #f2f4f7 !important;
        letter-spacing: -0.025em;
    }

    [data-testid="stMetricLabel"] {
        color: #98a2b3 !important;
    }

    [data-testid="stMetricValue"] {
        color: #f2f4f7 !important;
    }

    /* ========================================================
       BANNER
       ======================================================== */

    .main-banner {
        width: 100%;
        overflow: hidden;
        border-radius: 26px;
        margin-bottom: 2rem;
        border: 1px solid #25344d;
        background: #111c2f;
        box-shadow:
            0 20px 55px rgba(0, 0, 0, 0.30);
    }

    .main-banner img {
        display: block;
        width: 100%;
        height: auto;
    }

    /* ========================================================
       COMO FUNCIONA
       ======================================================== */

    .how-it-works {
        padding: 1.45rem 1.7rem;
        margin-bottom: 2.3rem;
        background:
            linear-gradient(
                145deg,
                #151f31 0%,
                #111827 100%
            );
        border: 1px solid #273449;
        border-radius: 20px;
        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.18);
    }

    .how-it-works-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: #f2f4f7;
        margin-bottom: 0.45rem;
    }

    .how-it-works-text {
        color: #98a2b3;
        font-size: 0.92rem;
        line-height: 1.6;
        max-width: 1000px;
    }

    /* ========================================================
       SEÇÕES
       ======================================================== */

    .section-heading {
        margin-top: 2.1rem;
        margin-bottom: 0.4rem;
        font-size: 1.45rem;
        font-weight: 780;
        color: #f2f4f7;
        letter-spacing: -0.025em;
    }

    .section-caption {
        margin-bottom: 1.25rem;
        color: #98a2b3;
        font-size: 0.92rem;
        line-height: 1.5;
    }

    /* ========================================================
       CARDS
       ======================================================== */

    .candidate-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;

        position: relative;
        overflow: hidden;

        height: 235px;
        min-height: 235px;

        text-decoration: none !important;
        color: inherit !important;
        text-align: center;

        background:
            linear-gradient(
                145deg,
                #151f31 0%,
                #111827 100%
            );

        border: 1px solid #273449;
        border-radius: 20px;

        padding: 1rem;

        margin-bottom: 1rem;

        box-shadow:
            0 10px 28px rgba(0, 0, 0, 0.18);

        transition:
            transform 160ms ease,
            box-shadow 160ms ease,
            border-color 160ms ease;
    }

    .candidate-card:hover {
        transform: translateY(-4px);
        border-color: #475467;
        box-shadow:
            0 18px 38px rgba(0, 0, 0, 0.28);
    }

    .candidate-card-accent {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
    }

    .candidate-map {
        display: flex;
        align-items: center;
        justify-content: center;

        width: 68px;
        height: 68px;

        margin: 0 auto 0.55rem auto;

        flex-shrink: 0;
    }

    .candidate-map img {
        display: block;
        width: 68px;
        height: 68px;
        object-fit: contain;
    }

    .candidate-number {
        width: 100%;
        text-align: center;

        font-size: 1.24rem;
        line-height: 1.1;

        font-weight: 820;

        color: #f8fafc;

        letter-spacing: -0.025em;
    }

    .candidate-status {
        text-align: center;
        margin-top: 0.45rem;
        font-size: 0.65rem;
        font-weight: 800;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        color: var(--candidate-color);
    }

    /* ========================================================
       PERFIL ANÔNIMO
       ======================================================== */

    .anonymous-header {
        position: relative;
        overflow: hidden;
        padding: 2.1rem 2.3rem;
        background:
            linear-gradient(
                135deg,
                #111c2f 0%,
                #17243a 100%
            );
        color: #f8fafc;
        border-radius: 24px;
        margin-bottom: 1.8rem;
        border: 1px solid #25344d;
        box-shadow:
            0 20px 50px rgba(0, 0, 0, 0.25);
    }

    .anonymous-header-accent {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 8px;
    }

    .anonymous-header-kicker {
        margin-top: 0.7rem;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-weight: 750;
        color: #98a2b3;
    }

    .anonymous-header-title {
        margin-top: 0.6rem;
        font-size: 2.65rem;
        line-height: 1;
        font-weight: 850;
        letter-spacing: -0.045em;
        color: #f8fafc;
    }

    .anonymous-header-subtitle {
        margin-top: 0.85rem;
        max-width: 760px;
        color: #b8c0cc;
        font-size: 0.98rem;
        line-height: 1.6;
    }

    /* ========================================================
       PAINÉIS
       ======================================================== */

    .info-panel {
        border: 1px solid #273449;
        background:
            linear-gradient(
                145deg,
                #151f31 0%,
                #111827 100%
            );
        border-radius: 20px;
        padding: 1.35rem 1.45rem;
        margin-bottom: 1.1rem;
        box-shadow:
            0 8px 26px rgba(0, 0, 0, 0.18);
    }

    .info-label {
        font-size: 0.69rem;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        font-weight: 750;
        color: #667085;
    }

    .info-value {
        margin-top: 0.3rem;
        font-size: 1.08rem;
        font-weight: 700;
        color: #f2f4f7;
        line-height: 1.4;
    }

    /* ========================================================
       TIMELINE
       ======================================================== */

    .timeline-item {
        border-left: 4px solid #475467;
        padding: 0.95rem 1.15rem;
        margin-bottom: 0.8rem;
        background: #131d2d;
        border-radius: 0 14px 14px 0;
        border-top: 1px solid #202c40;
        border-right: 1px solid #202c40;
        border-bottom: 1px solid #202c40;
    }

    .timeline-title {
        font-weight: 760;
        color: #f2f4f7;
    }

    .timeline-meta {
        margin-top: 0.28rem;
        color: #98a2b3;
        font-size: 0.86rem;
    }

    /* ========================================================
       REVELAÇÃO
       ======================================================== */

    .reveal-panel {
        border: 1px solid #344054;
        background:
            linear-gradient(
                145deg,
                #182235 0%,
                #101826 100%
            );
        border-radius: 24px;
        padding: 1.8rem;
        margin-top: 1.2rem;
        margin-bottom: 1.2rem;
        box-shadow:
            0 18px 45px rgba(0, 0, 0, 0.26);
    }

    .reveal-kicker {
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #98a2b3;
    }

    .reveal-name {
        margin-top: 0.35rem;
        font-size: 2.2rem;
        line-height: 1.05;
        font-weight: 850;
        color: #f8fafc;
        letter-spacing: -0.04em;
    }

    .reveal-note {
        margin-top: 0.65rem;
        color: #98a2b3;
        line-height: 1.5;
    }

    /* ========================================================
       COBERTURA
       ======================================================== */

    .coverage-box {
        border-radius: 18px;
        padding: 1.15rem 1.3rem;
        border: 1px solid #273449;
        background: #121c2c;
        margin-bottom: 0.9rem;
    }

    .coverage-title {
        font-weight: 760;
        color: #f2f4f7;
        margin-bottom: 0.28rem;
    }

    .coverage-text {
        color: #98a2b3;
        line-height: 1.55;
        font-size: 0.92rem;
    }

    /* ========================================================
       AVISO
       ======================================================== */

    .warning-box {
        border-left: 4px solid #f79009;
        background: #241d13;
        border-radius: 0 14px 14px 0;
        padding: 1rem 1.15rem;
        color: #f5d7a4;
        line-height: 1.5;
        margin-top: 1rem;
        border-top: 1px solid #48371d;
        border-right: 1px solid #48371d;
        border-bottom: 1px solid #48371d;
    }

    /* ========================================================
       IDENTIDADE
       ======================================================== */

    .identity-grid {
        display: grid;
        grid-template-columns:
            repeat(4, minmax(0, 1fr));
        gap: 0.8rem;
        margin-top: 1.2rem;
    }

    .identity-item {
        background: #101826;
        border: 1px solid #273449;
        border-radius: 16px;
        padding: 1rem;
    }

    .identity-label {
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #667085;
        font-weight: 750;
    }

    .identity-value {
        margin-top: 0.3rem;
        font-size: 1.02rem;
        font-weight: 750;
        color: #f2f4f7;
    }

    /* ========================================================
       COMPONENTES STREAMLIT
       ======================================================== */

    [data-testid="stDataFrame"] {
        border: 1px solid #273449 !important;
        border-radius: 16px !important;
        overflow: hidden !important;
    }

    [data-testid="stExpander"] {
        background: #111b2a !important;
        border: 1px solid #273449 !important;
        border-radius: 16px !important;
    }

    [data-testid="stExpander"] summary {
        color: #d0d5dd !important;
    }

    [data-testid="stExpander"] summary:hover {
        color: #ffffff !important;
    }

    div.stButton > button,
    div.stLinkButton > a {
        border-radius: 12px !important;
        font-weight: 750 !important;
        letter-spacing: 0.02em !important;
    }

    div.stButton > button {
        background: #1d2939 !important;
        color: #f2f4f7 !important;
        border: 1px solid #344054 !important;
    }

    div.stButton > button:hover {
        border-color: #667085 !important;
        background: #253248 !important;
    }

    [data-testid="stLinkButton"] a {
        background: #1d2939 !important;
        color: #f2f4f7 !important;
        border: 1px solid #344054 !important;
    }

    [data-testid="stLinkButton"] a:hover {
        background: #253248 !important;
        border-color: #667085 !important;
    }

    [data-testid="stAlert"] {
        background: #121c2c !important;
        border-color: #273449 !important;
        color: #d0d5dd !important;
    }

    [data-testid="stCaptionContainer"] {
        color: #667085 !important;
    }

    hr {
        border-color: #25344d !important;
    }

    @media (max-width: 900px) {

        .identity-grid {
            grid-template-columns:
                repeat(2, minmax(0, 1fr));
        }

        .candidate-card {
            height: 220px;
            min-height: 220px;
        }

        .candidate-map,
        .candidate-map img {
            width: 62px;
            height: 62px;
        }
    }

    @media (max-width: 600px) {

        .identity-grid {
            grid-template-columns: 1fr;
        }

        .candidate-card {
            height: 210px;
            min-height: 210px;
        }

        .candidate-map,
        .candidate-map img {
            width: 58px;
            height: 58px;
        }
    }

    </style>
    """
)


# ============================================================
# BANCO
# ============================================================

@st.cache_resource
def conectar_banco():
    return duckdb.connect(
        str(ARQUIVO_BANCO),
        read_only=True,
    )


def obter_coluna_numero_candidato(con):

    schema = con.execute(
        "PRAGMA table_info('candidatos')"
    ).df()

    colunas = set(
        schema["name"].tolist()
    )

    for coluna in [
        "NR_CANDIDATO",
        "NR_CANDIDATO_ELEICAO",
        "NR_CANDIDATO_CARGO",
    ]:
        if coluna in colunas:
            return coluna

    return None


# ============================================================
# NÚMEROS DE URNA VERIFICADOS
# ============================================================

NUMEROS_URNA_VERIFICADOS = {
    "CLARIANA BARAO": "27",
    "EDMILSON COSTA": "21",
    "ESCRITOR AUGUSTO CURY": "70",
    "FLAVIO BOLSONARO": "22",
    "HERTZ DIAS": "16",
    "LULA": "13",
    "PABLO MARÇAL": "28",
    "RENAN SANTOS": "14",
    "RONALDO CAIADO": "55",
    "RUI COSTA PIMENTA": "29",
    "SAMARA": "80",
    "VETERINÁRIO WILSON GRASSI": "35",
    "ZEMA": "30",
}


# ============================================================
# CARGA DOS CANDIDATOS
# ============================================================

@st.cache_data
def carregar_candidatos():

    con = conectar_banco()

    coluna_numero = obter_coluna_numero_candidato(con)

    if coluna_numero is None:
        numero_sql = "NULL AS numero_candidato"
    else:
        numero_sql = (
            f'CAST(c."{coluna_numero}" AS VARCHAR) '
            "AS numero_candidato"
        )

    consulta = f"""
        SELECT
            c.SQ_CANDIDATO,
            c.NM_CANDIDATO,
            c.NM_URNA_CANDIDATO,
            {numero_sql},
            c.SG_PARTIDO,
            c.DS_GENERO,
            c.DS_COR_RACA,
            c.DS_GRAU_INSTRUCAO,
            c.DS_OCUPACAO,
            c.ST_DECLARAR_BENS,

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
            p.possui_dados_legislativos,
            p.status_dados_legislativos,
            p.fontes_legislativas,

            cd.possui_dados_patrimoniais,
            cd.status_dados_patrimoniais,
            cd.cobertura_geral

        FROM candidatos AS c

        INNER JOIN candidatos_anonimos AS a
            ON c.SQ_CANDIDATO = a.SQ_CANDIDATO

        LEFT JOIN perfil_candidatos AS p
            ON c.SQ_CANDIDATO = p.SQ_CANDIDATO

        LEFT JOIN cobertura_dados AS cd
            ON c.SQ_CANDIDATO = cd.SQ_CANDIDATO
    """

    df = con.execute(consulta).df()

    anonimato = con.execute(
        """
        SELECT
            SQ_CANDIDATO,
            indice_anonimo,
            rotulo_anonimo,
            cor_card
        FROM candidatos_anonimos
        """
    ).df()

    df = df.merge(
        anonimato,
        on="SQ_CANDIDATO",
        how="inner",
        validate="one_to_one",
    )

    proposta = con.execute(
        """
        SELECT
            SQ_CANDIDATO,
            codigo_documento_tse,
            url_proposta_governo,
            fonte_proposta_governo,
            url_catalogo_tse,
            tipo_documento,
            acesso_publico
        FROM propostas_governo
        """
    ).df()

    df = df.merge(
        proposta,
        on="SQ_CANDIDATO",
        how="left",
        validate="one_to_one",
    )

    df["numero_urna_verificado"] = (
        df["NM_URNA_CANDIDATO"]
        .astype(str)
        .str.strip()
        .map(NUMEROS_URNA_VERIFICADOS)
    )

    df["numero_candidato"] = (
        df["numero_urna_verificado"]
        .combine_first(
            df["numero_candidato"]
        )
    )

    return df


@st.cache_data
def carregar_cargos():

    con = conectar_banco()

    return con.execute(
        """
        SELECT
            SQ_CANDIDATO,
            cargo,
            esfera,
            localidade,
            inicio,
            fim,
            situacao,
            fonte,
            url_fonte
        FROM historico_cargos_politicos
        ORDER BY
            SQ_CANDIDATO,
            inicio
        """
    ).df()


@st.cache_data
def carregar_bens():

    con = conectar_banco()

    return con.execute(
        """
        SELECT
            SQ_CANDIDATO,
            categoria,
            DS_TIPO_BEM_CANDIDATO,
            DS_BEM_CANDIDATO,
            VR_BEM_CANDIDATO
        FROM bens_candidatos_detalhados
        ORDER BY
            SQ_CANDIDATO,
            VR_BEM_CANDIDATO DESC
        """
    ).df()


@st.cache_data
def carregar_projetos_camara():

    con = conectar_banco()

    return con.execute(
        """
        SELECT
            idProposicao,
            candidato,
            siglaTipo,
            numero,
            ano_y AS ano,
            descricaoTipo,
            ementa,
            ementaDetalhada,
            tema_principal,
            temas,
            aprovado,
            ultimoStatus_dataHora,
            ultimoStatus_descricaoTramitacao,
            ultimoStatus_descricaoSituacao,
            ultimoStatus_apreciacao,
            urlInteiroTeor,
            ultimoStatus_url
        FROM projetos_camara
        ORDER BY
            candidato,
            ano_y DESC,
            numero DESC
        """
    ).df()


@st.cache_data
def carregar_materias_senado():

    con = conectar_banco()

    df = con.execute(
        """
        SELECT
            candidato,
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
        ORDER BY
            candidato,
            ano DESC,
            numero DESC
        """
    ).df()

    df["candidato_key"] = (
        df["candidato"]
        .astype(str)
        .str.replace(
            "_",
            " ",
            regex=False,
        )
        .str.upper()
        .str.strip()
    )

    return df


# ============================================================
# FORMATAÇÃO
# ============================================================

def moeda(valor):

    if valor is None or pd.isna(valor):
        return "Não informado"

    return (
        f"R$ {float(valor):,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def moeda_compacta(valor):

    if valor is None or pd.isna(valor):
        return "—"

    valor = float(valor)

    if valor >= 1_000_000_000:
        numero = valor / 1_000_000_000
        if numero.is_integer():
            return f"R$ {int(numero)} Bi"
        return f"R$ {numero:.1f} Bi".replace(".", ",")

    if valor >= 1_000_000:
        numero = valor / 1_000_000
        if numero.is_integer():
            return f"R$ {int(numero)} Mi"
        return f"R$ {numero:.1f} Mi".replace(".", ",")

    if valor >= 1_000:
        numero = valor / 1_000
        if numero.is_integer():
            return f"R$ {int(numero)} Mil"
        return f"R$ {numero:.1f} Mil".replace(".", ",")

    return moeda(valor)


def inteiro(valor):

    if valor is None or pd.isna(valor):
        return "Não informado"

    return f"{int(valor):,}".replace(",", ".")


def valor_card(valor):

    if valor is None or pd.isna(valor):
        return "—"

    return inteiro(valor)


def texto(valor):

    if valor is None or pd.isna(valor):
        return "Não informado"

    return str(valor)


def numero_urna(valor):

    if valor is None or pd.isna(valor):
        return "Não informado"

    valor = str(valor).strip()

    if valor.endswith(".0"):
        valor = valor[:-2]

    return valor


# ============================================================
# INDICADORES
# ============================================================

STATUS_FINAIS = {
    "Arquivada",
    "Tramitação Finalizada",
    "Transformado em Norma Jurídica",
    "Vetado totalmente",
    "Retirado pelo(a) Autor(a)",
}


def calcular_indicadores_card(
    candidato_nome,
    projetos_camara,
    materias_senado,
    possui_dados_legislativos,
):

    if not bool(possui_dados_legislativos):
        return {
            "propostas": None,
            "andamento": None,
            "aprovados": None,
        }

    projetos = projetos_camara[
        projetos_camara["candidato"]
        == candidato_nome
    ].copy()

    materias = materias_senado[
        materias_senado["candidato_key"]
        == candidato_nome.upper()
    ].copy()

    propostas = 0

    if not projetos.empty:
        propostas += int(
            projetos[
                "idProposicao"
            ].nunique()
        )

    if not materias.empty:
        propostas += int(
            materias[
                "codigo_materia"
            ].nunique()
        )

    andamento = 0

    if not materias.empty:
        andamento += int(
            (
                materias["tramitando"]
                .astype(str)
                .str.upper()
                .eq("S")
            ).sum()
        )

    if not projetos.empty:

        situacoes = (
            projetos[
                "ultimoStatus_descricaoSituacao"
            ]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        classificaveis = (
            situacoes.ne("")
            & ~situacoes.isin(STATUS_FINAIS)
        )

        andamento += int(
            classificaveis.sum()
        )

    aprovados = None

    if not projetos.empty:
        aprovados = int(
            projetos["aprovado"]
            .fillna(False)
            .sum()
        )

    return {
        "propostas": propostas,
        "andamento": andamento,
        "aprovados": aprovados,
    }


# ============================================================
# DADOS
# ============================================================

candidatos = carregar_candidatos()
cargos = carregar_cargos()
bens = carregar_bens()
projetos_camara = carregar_projetos_camara()
materias_senado = carregar_materias_senado()

candidatos_por_id = candidatos.set_index(
    "indice_anonimo",
    drop=False,
)


# ============================================================
# ORDEM ALEATÓRIA
# ============================================================

ids_anonimos = (
    candidatos["indice_anonimo"]
    .astype(int)
    .tolist()
)

if (
    "ordem_home" not in st.session_state
    or set(st.session_state["ordem_home"])
    != set(ids_anonimos)
):
    ordem = ids_anonimos.copy()
    SystemRandom().shuffle(ordem)
    st.session_state["ordem_home"] = ordem


# ============================================================
# CANDIDATOS VISTOS
# ============================================================

if "candidatos_vistos" not in st.session_state:
    st.session_state["candidatos_vistos"] = set()


# ============================================================
# NAVEGAÇÃO
# ============================================================

parametro = st.query_params.get("candidato")

try:
    candidato_selecionado = (
        int(parametro)
        if parametro is not None
        else None
    )
except (TypeError, ValueError):
    candidato_selecionado = None


def voltar_home():
    st.query_params.clear()
    st.rerun()


# ============================================================
# HOME
# ============================================================

def render_home():

    # --------------------------------------------------------
    # BANNER
    # --------------------------------------------------------

    if BANNER_BASE64:
        render_html(
            f"""
            <div class="main-banner">
                <img
                    src="data:image/png;base64,{BANNER_BASE64}"
                    alt="O Voto Imparcial"
                />
            </div>
            """
        )
    else:
        render_html(
            """
            <section class="hero">
                <div class="hero-title">
                    O Voto Imparcial
                </div>
            </section>
            """
        )

    # --------------------------------------------------------
    # COMO FUNCIONA
    # --------------------------------------------------------

    render_html(
        """
        <section class="how-it-works">
            <div class="how-it-works-title">
                Como funciona
            </div>
            <div class="how-it-works-text">
                Os candidatos são apresentados de forma anônima.
                Você pode consultar as informações públicas
                disponíveis sobre cada perfil antes de revelar
                sua identidade. A identidade só é exibida depois
                que você decide selecionar o candidato.
            </div>
        </section>
        """
    )

    # --------------------------------------------------------
    # TÍTULO
    # --------------------------------------------------------

    render_html(
        """
        <div class="section-heading">
            Conheça os candidatos
        </div>
        """
    )

    render_html(
        """
        <div class="section-caption">
            Explore os perfis sem conhecer previamente sua identidade.
        </div>
        """
    )

    ordem = st.session_state["ordem_home"]

    for inicio in range(0, len(ordem), 3):

        linha = ordem[inicio:inicio + 3]

        colunas = st.columns(
            3,
            gap="large",
        )

        for coluna, anon_id in zip(colunas, linha):

            candidato = candidatos_por_id.loc[anon_id]

            cor = escape(
                str(candidato["cor_card"])
            )

            rotulo = escape(
                str(candidato["rotulo_anonimo"])
            )

            foi_visto = (
                int(anon_id)
                in st.session_state["candidatos_vistos"]
            )

            if foi_visto:
                status_html = (
                    f"""
                    <div
                        class="candidate-status"
                        style="--candidate-color:{cor};"
                    >
                        Candidato visto
                    </div>
                    """
                )
            else:
                status_html = ""

            mapa_uri = svg_mapa_data_uri(
                MAPA_SVG_BASE,
                cor,
            )

            if mapa_uri:
                icon_html = (
                    f"""
                    <div class="candidate-map">
                        <img
                            src="{mapa_uri}"
                            alt=""
                        />
                    </div>
                    """
                )
            else:
                icon_html = (
                    f"""
                    <div
                        class="candidate-map"
                        style="color:{cor};"
                    >
                        <span
                            style="
                                font-size:1.4rem;
                                font-weight:800;
                            "
                        >
                            {int(anon_id)}
                        </span>
                    </div>
                    """
                )

            card_html = (
                f"""
                <a
                    class="candidate-card"
                    href="?candidato={int(anon_id)}"
                >
                    <div
                        class="candidate-card-accent"
                        style="background:{cor};"
                    ></div>

                    {icon_html}

                    <div class="candidate-number">
                        {rotulo}
                    </div>

                    {status_html}
                </a>
                """
            )

            with coluna:
                render_html(card_html)


# ============================================================
# PERFIL
# ============================================================

def render_perfil(anon_id):

    if anon_id not in candidatos_por_id.index:
        voltar_home()

    st.session_state["candidatos_vistos"].add(
        int(anon_id)
    )

    candidato = candidatos_por_id.loc[anon_id]

    sq_candidato = int(
        candidato["SQ_CANDIDATO"]
    )

    nome_candidato = str(
        candidato["NM_URNA_CANDIDATO"]
    )

    rotulo = str(
        candidato["rotulo_anonimo"]
    )

    cor = str(
        candidato["cor_card"]
    )

    projetos = projetos_camara[
        projetos_camara["candidato"]
        == nome_candidato
    ].copy()

    materias = materias_senado[
        materias_senado["candidato_key"]
        == nome_candidato.upper()
    ].copy()

    cargos_candidato = cargos[
        cargos["SQ_CANDIDATO"]
        == sq_candidato
    ].copy()

    bens_candidato = bens[
        bens["SQ_CANDIDATO"]
        == sq_candidato
    ].copy()

    indicadores = calcular_indicadores_card(
        nome_candidato,
        projetos_camara,
        materias_senado,
        candidato["possui_dados_legislativos"],
    )

    revelado = (
        st.session_state.get(
            "candidato_revelado"
        ) == int(anon_id)
    )

    voltar = st.button(
        "← Voltar para candidatos",
        use_container_width=False,
    )

    if voltar:
        voltar_home()

    # --------------------------------------------------------
    # CABEÇALHO
    # --------------------------------------------------------

    render_html(
        f"""
        <section class="anonymous-header">

            <div
                class="anonymous-header-accent"
                style="background:{escape(cor)};"
            ></div>

            <div class="anonymous-header-kicker">
                PERFIL ANÔNIMO
            </div>

            <div class="anonymous-header-title">
                {escape(rotulo)}
            </div>

            <div class="anonymous-header-subtitle">
                Este perfil apresenta informações de formação,
                patrimônio, cargos políticos e atuação legislativa.
                A identidade permanece oculta até sua decisão.
            </div>

        </section>
        """
    )

    # --------------------------------------------------------
    # RESUMO
    # --------------------------------------------------------

    render_html(
        """
        <div class="section-heading">
            Resumo
        </div>
        """
    )

    resumo1, resumo2, resumo3, resumo4 = st.columns(
        4,
        gap="medium",
    )

    with resumo1:
        st.metric(
            "Patrimônio declarado",
            moeda_compacta(
                candidato["patrimonio_total"]
            ),
        )

    with resumo2:
        st.metric(
            "Bens declarados",
            inteiro(
                candidato["quantidade_bens"]
            ),
        )

    with resumo3:
        st.metric(
            "Propostas legislativas",
            valor_card(
                indicadores["propostas"]
            ),
        )

    with resumo4:
        st.metric(
            "Aprovados",
            valor_card(
                indicadores["aprovados"]
            ),
        )

    # --------------------------------------------------------
    # FORMAÇÃO
    # --------------------------------------------------------

    render_html(
        """
        <div class="section-heading">
            Formação e perfil
        </div>
        """
    )

    perfil1, perfil2 = st.columns(
        2,
        gap="large",
    )

    with perfil1:
        render_html(
            f"""
            <div class="info-panel">
                <div class="info-label">
                    Escolaridade
                </div>
                <div class="info-value">
                    {escape(
                        texto(
                            candidato["DS_GRAU_INSTRUCAO"]
                        )
                    )}
                </div>
            </div>
            """
        )

    with perfil2:
        render_html(
            f"""
            <div class="info-panel">
                <div class="info-label">
                    Ocupação
                </div>
                <div class="info-value">
                    {escape(
                        texto(
                            candidato["DS_OCUPACAO"]
                        )
                    )}
                </div>
            </div>
            """
        )

    # --------------------------------------------------------
    # CARGOS POLÍTICOS
    # --------------------------------------------------------

    render_html(
        """
        <div class="section-heading">
            Cargos políticos ocupados
        </div>
        """
    )

    render_html(
        """
        <div class="section-caption">
            Somente cargos políticos confirmados pelas fontes
            incorporadas ao projeto são apresentados.
        </div>
        """
    )

    if cargos_candidato.empty:
        st.info(
            "Não há cargos políticos confirmados na base coletada."
        )
    else:
        for _, cargo in cargos_candidato.iterrows():

            inicio = texto(cargo["inicio"])
            fim = cargo["fim"]

            if pd.isna(fim):
                periodo = f"{inicio} — atual"
            else:
                periodo = f"{inicio} — {fim}"

            meta = (
                f"{cargo['esfera']} • "
                f"{cargo['localidade']} • "
                f"{periodo}"
            )

            render_html(
                f"""
                <div
                    class="timeline-item"
                    style="border-left-color:{escape(cor)};"
                >
                    <div class="timeline-title">
                        {escape(str(cargo['cargo']))}
                    </div>
                    <div class="timeline-meta">
                        {escape(meta)}
                    </div>
                </div>
                """
            )

    # --------------------------------------------------------
    # PATRIMÔNIO
    # --------------------------------------------------------

    render_html(
        """
        <div class="section-heading">
            Patrimônio
        </div>
        """
    )

    possui_bens = bool(
        candidato["quantidade_bens"]
        and float(candidato["quantidade_bens"]) > 0
    )

    if not possui_bens:

        st.info(
            "Não há dados patrimoniais disponíveis na base coletada."
        )

    elif bens_candidato.empty:

        st.info(
            "Existe patrimônio declarado, mas o detalhamento dos bens "
            "não está disponível na tabela analítica."
        )

    else:

        resumo_bens = (
            bens_candidato
            .groupby(
                "categoria",
                as_index=False,
            )["VR_BEM_CANDIDATO"]
            .sum()
            .sort_values(
                "VR_BEM_CANDIDATO",
                ascending=False,
            )
        )

        patrimonio1, patrimonio2 = st.columns(
            [1, 2],
            gap="large",
        )

        with patrimonio1:

            render_html(
                f"""
                <div class="info-panel">
                    <div class="info-label">
                        Patrimônio total
                    </div>
                    <div
                        class="info-value"
                        style="font-size:1.75rem;margin-top:0.55rem;"
                    >
                        {moeda(
                            candidato["patrimonio_total"]
                        )}
                    </div>
                </div>
                """
            )

        with patrimonio2:

            resumo_display = (
                resumo_bens
                .rename(
                    columns={
                        "categoria": "Categoria",
                        "VR_BEM_CANDIDATO": "Valor",
                    }
                )
                .copy()
            )

            resumo_display["Valor"] = (
                resumo_display["Valor"].map(moeda)
            )

            st.dataframe(
                resumo_display,
                use_container_width=True,
                hide_index=True,
            )

        with st.expander(
            "Ver todos os bens declarados",
            expanded=False,
        ):

            bens_display = (
                bens_candidato[
                    [
                        "categoria",
                        "DS_TIPO_BEM_CANDIDATO",
                        "DS_BEM_CANDIDATO",
                        "VR_BEM_CANDIDATO",
                    ]
                ]
                .copy()
            )

            bens_display["VR_BEM_CANDIDATO"] = (
                bens_display["VR_BEM_CANDIDATO"].map(moeda)
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
                bens_display,
                use_container_width=True,
                hide_index=True,
            )

    # --------------------------------------------------------
    # LEGISLATIVO
    # --------------------------------------------------------

    render_html(
        """
        <div class="section-heading">
            Atuação legislativa
        </div>
        """
    )

    if not bool(
        candidato["possui_dados_legislativos"]
    ):

        st.info(
            "Não há dados legislativos disponíveis na base coletada."
        )

    else:

        fonte = candidato["fontes_legislativas"]

        if pd.notna(fonte):
            render_html(
                f"""
                <div class="coverage-box">
                    <div class="coverage-title">
                        Fontes disponíveis
                    </div>
                    <div class="coverage-text">
                        {escape(str(fonte))}
                    </div>
                </div>
                """
            )

        leg1, leg2, leg3 = st.columns(
            3,
            gap="medium",
        )

        with leg1:
            st.metric(
                "Propostas",
                valor_card(indicadores["propostas"]),
            )

        with leg2:
            st.metric(
                "Em andamento",
                valor_card(indicadores["andamento"]),
            )

        with leg3:
            st.metric(
                "Aprovados",
                valor_card(indicadores["aprovados"]),
            )

        if not projetos.empty:

            with st.expander(
                "Câmara dos Deputados — atuação completa",
                expanded=False,
            ):

                tabela = projetos[
                    [
                        "siglaTipo",
                        "numero",
                        "ano",
                        "descricaoTipo",
                        "tema_principal",
                        "aprovado",
                        "ultimoStatus_descricaoSituacao",
                        "ultimoStatus_descricaoTramitacao",
                        "ementa",
                        "urlInteiroTeor",
                    ]
                ].copy()

                tabela = tabela.rename(
                    columns={
                        "siglaTipo": "Tipo",
                        "numero": "Número",
                        "ano": "Ano",
                        "descricaoTipo": "Descrição",
                        "tema_principal": "Tema",
                        "aprovado": "Aprovação identificada",
                        "ultimoStatus_descricaoSituacao": "Situação",
                        "ultimoStatus_descricaoTramitacao": "Tramitação",
                        "ementa": "Ementa",
                        "urlInteiroTeor": "Inteiro teor",
                    }
                )

                st.dataframe(
                    tabela,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Inteiro teor":
                            st.column_config.LinkColumn(
                                "Inteiro teor",
                                display_text="Abrir",
                            )
                    },
                )

        if not materias.empty:

            with st.expander(
                "Senado Federal — atuação completa",
                expanded=False,
            ):

                tabela = materias[
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

                tabela = tabela.rename(
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
                    tabela,
                    use_container_width=True,
                    hide_index=True,
                )

    # --------------------------------------------------------
    # COBERTURA
    # --------------------------------------------------------

    render_html(
        """
        <div class="section-heading">
            Cobertura dos dados
        </div>
        """
    )

    status_patrimonio = (
        "Dados disponíveis"
        if bool(candidato["possui_dados_patrimoniais"])
        else "Sem dados patrimoniais na base coletada"
    )

    status_legislativo = texto(
        candidato["status_dados_legislativos"]
    )

    render_html(
        f"""
        <div class="coverage-box">
            <div class="coverage-title">
                Patrimônio
            </div>
            <div class="coverage-text">
                {escape(status_patrimonio)}
            </div>
        </div>

        <div class="coverage-box">
            <div class="coverage-title">
                Atuação legislativa
            </div>
            <div class="coverage-text">
                {escape(status_legislativo)}
            </div>
        </div>
        """
    )

    fontes = candidato["fontes_legislativas"]

    if pd.notna(fontes):
        render_html(
            f"""
            <div class="coverage-box">
                <div class="coverage-title">
                    Fontes legislativas
                </div>
                <div class="coverage-text">
                    {escape(str(fontes))}
                </div>
            </div>
            """
        )

    render_html(
        """
        <div class="warning-box">
            Ausência de dados nesta aplicação significa que
            não foram encontrados registros nas fontes incorporadas
            ao projeto. Isso não deve ser interpretado como prova
            de ausência de atuação política ou legislativa.
        </div>
        """
    )

    # --------------------------------------------------------
    # DECISÃO
    # --------------------------------------------------------

    render_html(
        """
        <div class="section-heading">
            Decisão
        </div>
        """
    )

    if not revelado:

        render_html(
            """
            <div class="coverage-box">
                <div class="coverage-title">
                    Você já conhece o histórico.
                </div>
                <div class="coverage-text">
                    A identidade permanece oculta até que você
                    decida selecionar este candidato.
                </div>
            </div>
            """
        )

        selecionar = st.button(
            "SELECIONAR CANDIDATO",
            use_container_width=True,
            type="primary",
        )

        if selecionar:
            st.session_state[
                "candidato_revelado"
            ] = int(anon_id)
            st.rerun()

    else:

        numero = numero_urna(
            candidato["numero_candidato"]
        )

        proposta_url = candidato[
            "url_proposta_governo"
        ]

        render_html(
            f"""
            <div class="reveal-panel">

                <div class="reveal-kicker">
                    IDENTIDADE REVELADA
                </div>

                <div class="reveal-name">
                    {escape(
                        str(
                            candidato["NM_CANDIDATO"]
                        )
                    )}
                </div>

                <div class="reveal-note">
                    Estas informações só estão disponíveis
                    porque você decidiu selecionar este candidato.
                </div>

                <div class="identity-grid">

                    <div class="identity-item">
                        <div class="identity-label">
                            Número de urna
                        </div>
                        <div class="identity-value">
                            {escape(numero)}
                        </div>
                    </div>

                    <div class="identity-item">
                        <div class="identity-label">
                            Gênero
                        </div>
                        <div class="identity-value">
                            {escape(
                                texto(
                                    candidato["DS_GENERO"]
                                )
                            )}
                        </div>
                    </div>

                    <div class="identity-item">
                        <div class="identity-label">
                            Partido
                        </div>
                        <div class="identity-value">
                            {escape(
                                texto(
                                    candidato["SG_PARTIDO"]
                                )
                            )}
                        </div>
                    </div>

                    <div class="identity-item">
                        <div class="identity-label">
                            Identificador
                        </div>
                        <div class="identity-value">
                            {escape(rotulo)}
                        </div>
                    </div>

                </div>

            </div>
            """
        )

        if (
            pd.notna(proposta_url)
            and str(proposta_url).strip()
        ):

            render_html(
                """
                <div class="section-heading">
                    Proposta de governo
                </div>
                """
            )

            st.write(
                "Documento de proposta de governo disponível publicamente."
            )

            st.link_button(
                "ABRIR PROPOSTA DE GOVERNO",
                str(proposta_url),
                use_container_width=True,
            )

            fonte_proposta = candidato[
                "fonte_proposta_governo"
            ]

            if pd.notna(fonte_proposta):
                st.caption(
                    str(fonte_proposta)
                )

        else:

            st.info(
                "Não há proposta de governo vinculada na base do projeto."
            )

    st.divider()

    st.caption(
        "O Voto Imparcial — os indicadores são descritivos "
        "e não constituem recomendação eleitoral."
    )


# ============================================================
# EXECUÇÃO
# ============================================================

if candidato_selecionado is None:
    render_home()
else:
    render_perfil(candidato_selecionado)
