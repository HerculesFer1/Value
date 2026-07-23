"""Critério de aceite da Fase 1 (parte Selic): reproduzir 55,3103% do paradigma.

Usa payload cacheado do BCB/SGS 4390 (offline, determinístico). A acumulação é
por SOMA SIMPLES das taxas mensais — é o que reproduz o paradigma; a composição
diverge em ~20 pontos.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from pathlib import Path

from value_indices.acumulacao import fator_soma_simples, soma_simples_percent
from value_indices.coletores import parsear_sgs

GOLDEN = Path(__file__).resolve().parent / "dados" / "sgs_4390_dez2021_jul2026.json"

# dez/2021 -> jun/2026 (jul/2026 não fecha antes da data de cálculo, 23/07/2026)
INI = date(2021, 12, 1)
FIM = date(2026, 6, 1)

PARADIGMA_PCT = Decimal("55.3103")
TOLERANCIA = Decimal("0.01")  # ±R$ 0,01/parcela ⇒ margem no fator acumulado


def _serie():
    conteudo = GOLDEN.read_bytes()
    return parsear_sgs(
        conteudo,
        nome="selic_mensal",
        codigo=4390,
        url="golden://sgs_4390",
        versao="teste",
        data_coleta=None,
    )


def test_soma_simples_reproduz_paradigma() -> None:
    serie = _serie()
    pct = soma_simples_percent(serie.pontos, INI, FIM)
    # SGS 4390 vem com 2 casas; soma dá 55,3100%.
    assert pct == Decimal("55.3100")
    # dentro da tolerância declarada do paradigma (55,3103%). O resíduo de
    # 0,0003pp é o defeito nº 4: reprodução exata exige a Selic diária (SGS 11).
    assert abs(pct - PARADIGMA_PCT) <= TOLERANCIA


def test_fator_acumulado() -> None:
    serie = _serie()
    fator = fator_soma_simples(serie.pontos, INI, FIM)
    assert fator == Decimal("1.553100")


def test_composicao_diverge() -> None:
    """Sanidade: juros compostos NÃO reproduzem o paradigma (seriam ~74,8%)."""
    serie = _serie()
    composto = Decimal(1)
    for p in serie.pontos:
        if INI <= p.competencia <= FIM:
            composto *= Decimal(1) + p.valor / Decimal(100)
    pct_composto = (composto - 1) * Decimal(100)
    assert abs(pct_composto - PARADIGMA_PCT) > Decimal(10)
