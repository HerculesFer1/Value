"""Catálogo das fontes oficiais (PROMPT_VALUE.md §7).

Endereços e identificadores de série. Os coletores concretos (Fase 1) usam este
catálogo; nada aqui faz requisição — é só o registro declarativo das origens.
"""

from __future__ import annotations

from .base import FonteSerie

# BCB/SGS — a data entra no formato dd/MM/aaaa.
BCB_SGS_URL = (
    "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
    "?formato=json&dataInicial={ini}&dataFinal={fim}"
)

CATALOGO = {
    "selic_mensal": {
        "fonte": FonteSerie.BCB_SGS,
        "codigo_sgs": 4390,   # Selic acumulada no mês
        "descricao": "Selic acumulada no mês (BCB/SGS 4390)",
    },
    "selic_diaria": {
        "fonte": FonteSerie.BCB_SGS,
        "codigo_sgs": 11,     # Selic diária
        "descricao": "Selic diária (BCB/SGS 11)",
    },
    "tr": {
        "fonte": FonteSerie.BCB_SGS,
        "codigo_sgs": None,   # definir código na Fase 1
        "descricao": "TR / poupança (BCB/SGS)",
    },
    "ipca": {
        "fonte": FonteSerie.IBGE_SIDRA,
        "descricao": "IPCA (IBGE/SIDRA)",
    },
    "ipca_e": {
        "fonte": FonteSerie.IBGE_SIDRA,
        "descricao": "IPCA-E (IBGE/SIDRA) — mas correção usa a TABELA DO CJF",
    },
    "salario_minimo": {
        "fonte": FonteSerie.IPEADATA,
        "descricao": "Salário mínimo histórico (IPEAData)",
    },
    "correcao_cjf": {
        "fonte": FonteSerie.CJF,
        "descricao": (
            "Tabela de correção — Manual CJF, Res. CJF nº 990 de 13/07/2026. "
            "Fonte PRIMÁRIA de correção; não recalcular IPCA-E por conta própria."
        ),
    },
}
