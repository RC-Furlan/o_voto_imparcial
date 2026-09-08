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
        projetos_camara,
        aprovados_camara,
        materias_senado,
        tramitando_senado,
        nao_tramitando_senado
    FROM perfil_candidatos
    ORDER BY NM_URNA_CANDIDATO
    """
).df()


print("VALIDAÇÃO LEGISLATIVA")
print()

print(
    resultado.to_string(index=False)
)

print()

print("TOTAIS")
print(
    f"Projetos Câmara: "
    f"{resultado['projetos_camara'].sum():.0f}"
)

print(
    f"Aprovados Câmara: "
    f"{resultado['aprovados_camara'].sum():.0f}"
)

print(
    f"Matérias Senado: "
    f"{resultado['materias_senado'].sum():.0f}"
)

print(
    f"Em tramitação no Senado: "
    f"{resultado['tramitando_senado'].sum():.0f}"
)

print(
    f"Fora de tramitação no Senado: "
    f"{resultado['nao_tramitando_senado'].sum():.0f}"
)


con.close()