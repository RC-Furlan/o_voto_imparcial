from pathlib import Path

import duckdb


ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)


con = duckdb.connect(
    str(ARQUIVO_BANCO)
)


con.execute(
    """
    DROP TABLE IF EXISTS perfil_candidatos
    """
)


con.execute(
    """
    CREATE TABLE perfil_candidatos AS

    SELECT
        c.SQ_CANDIDATO,
        c.NM_CANDIDATO,
        c.NM_URNA_CANDIDATO,
        c.SG_PARTIDO,
        c.DS_GENERO,
        c.DS_COR_RACA,
        c.DS_GRAU_INSTRUCAO,
        c.DS_OCUPACAO,
        c.ST_DECLARAR_BENS,

        COALESCE(c.quantidade_bens, 0)
            AS quantidade_bens,

        COALESCE(c.patrimonio_total, 0)
            AS patrimonio_total,

        COALESCE(c.qtd_imoveis, 0)
            AS qtd_imoveis,

        COALESCE(c.valor_imoveis, 0)
            AS valor_imoveis,

        COALESCE(c.qtd_veiculos, 0)
            AS qtd_veiculos,

        COALESCE(c.valor_veiculos, 0)
            AS valor_veiculos,

        COALESCE(c.qtd_investimentos, 0)
            AS qtd_investimentos,

        COALESCE(c.valor_investimentos, 0)
            AS valor_investimentos,

        COALESCE(c.qtd_participacoes, 0)
            AS qtd_participacoes,

        COALESCE(c.valor_participacoes, 0)
            AS valor_participacoes,

        COALESCE(c.qtd_contas, 0)
            AS qtd_contas,

        COALESCE(c.valor_contas, 0)
            AS valor_contas,

        COALESCE(c.qtd_bens_valor, 0)
            AS qtd_bens_valor,

        COALESCE(c.valor_bens_valor, 0)
            AS valor_bens_valor,

        COALESCE(c.qtd_outros, 0)
            AS qtd_outros,

        COALESCE(c.valor_outros, 0)
            AS valor_outros,

        l.projetos_camara,
        l.aprovados_camara,
        l.materias_senado,
        l.tramitando_senado,
        l.nao_tramitando_senado,

        CASE
            WHEN l.candidato IS NULL
                THEN FALSE
            ELSE TRUE
        END AS possui_dados_legislativos,

        CASE
            WHEN l.candidato IS NULL
                THEN 'SEM_DADOS_NA_BASE_COLETADA'
            ELSE 'DADOS_DISPONIVEIS'
        END AS status_dados_legislativos,

        CASE
            WHEN l.candidato = 'FLAVIO BOLSONARO'
                THEN 'SENADO_FEDERAL'
            WHEN l.candidato = 'RONALDO CAIADO'
                THEN 'CAMARA_DOS_DEPUTADOS_E_SENADO_FEDERAL'
            ELSE NULL
        END AS fontes_legislativas

    FROM candidatos AS c

    LEFT JOIN indicadores_legislativos AS l
        ON c.NM_URNA_CANDIDATO = l.candidato
    """
)


print(
    con.execute(
        """
        SELECT
            NM_URNA_CANDIDATO,
            status_dados_legislativos,
            fontes_legislativas
        FROM perfil_candidatos
        ORDER BY NM_URNA_CANDIDATO
        """
    ).df().to_string(index=False)
)


con.close()