from pathlib import Path

import duckdb


ARQUIVO_BANCO = Path(
    "banco/voto_imparcial.duckdb"
)


con = duckdb.connect(
    str(ARQUIVO_BANCO)
)


resultado = con.execute(
    """
    SELECT
        NM_URNA_CANDIDATO,
        SG_PARTIDO,
        patrimonio_total,

        CASE
            WHEN quantidade_bens > 0
                THEN TRUE
            ELSE FALSE
        END AS possui_dados_patrimoniais,

        possui_dados_legislativos,

        status_dados_legislativos,

        CASE
            WHEN projetos_camara IS NOT NULL
                OR materias_senado IS NOT NULL
                THEN TRUE
            ELSE FALSE
        END AS possui_producao_legislativa,

        projetos_camara,
        aprovados_camara,

        materias_senado,
        tramitando_senado,
        nao_tramitando_senado,

        fontes_legislativas

    FROM perfil_candidatos

    ORDER BY
        NM_URNA_CANDIDATO
    """
).df()


print("COBERTURA DOS DADOS")
print()

print(
    resultado.to_string(index=False)
)

print()

print("RESUMO")

print(
    f"Candidatos: {len(resultado)}"
)

print(
    f"Com dados patrimoniais: "
    f"{resultado['possui_dados_patrimoniais'].sum()}"
)

print(
    f"Sem dados patrimoniais: "
    f"{(~resultado['possui_dados_patrimoniais']).sum()}"
)

print(
    f"Com dados legislativos: "
    f"{resultado['possui_dados_legislativos'].sum()}"
)

print(
    f"Sem dados legislativos: "
    f"{(~resultado['possui_dados_legislativos']).sum()}"
)


con.close()