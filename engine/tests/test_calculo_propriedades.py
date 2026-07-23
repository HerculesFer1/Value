"""Testes de propriedade do cálculo (§10), determinísticos (sem hypothesis).

Cobrem: soma das parcelas = total; invariância à ordem; determinismo do recálculo.
"""

from __future__ import annotations

import itertools
from datetime import date
from decimal import Decimal

from value_engine.calculo import (
    EntradaPasep,
    MomentoArredondamento,
    ParcelaCalc,
    PoliticaCalculo,
    calcular_pasep,
)

POL = PoliticaCalculo(momento=MomentoArredondamento.POR_PARCELA, modo="ROUND_HALF_UP", casas=2)


def _parcela(ano: int, sm: str, fator: str) -> ParcelaCalc:
    return ParcelaCalc(
        competencia=date(ano, 1, 1),
        valor_base=Decimal(sm),
        fator_correcao=Decimal(fator),
        taxa_juros=Decimal("0.489165"),
        taxa_selic=Decimal("0.553103"),
    )


BASE = [
    _parcela(2006, "350.00", "2.3492924649"),
    _parcela(2007, "380.00", "2.2711258509"),
    _parcela(2008, "415.00", "2.1447909444"),
]


def _entrada(parcelas) -> EntradaPasep:
    return EntradaPasep(
        data_calculo=date(2026, 7, 23), politica=POL, parcelas=tuple(parcelas)
    )


def test_soma_igual_ao_total() -> None:
    res = calcular_pasep(_entrada(BASE))
    soma = sum((p.atualizado for p in res.parcelas), Decimal(0))
    assert soma == res.total_principal


def test_invariancia_a_ordem() -> None:
    """Total é o mesmo para qualquer ordem das parcelas (momento por_parcela)."""
    esperado = calcular_pasep(_entrada(BASE)).total_principal
    for perm in itertools.permutations(BASE):
        assert calcular_pasep(_entrada(perm)).total_principal == esperado


def test_determinismo() -> None:
    """Mesma entrada ⇒ saída idêntica (byte a byte nos Decimais)."""
    a = calcular_pasep(_entrada(BASE))
    b = calcular_pasep(_entrada(BASE))
    assert a == b


def test_momento_so_no_total_difere_por_no_maximo_centavos() -> None:
    """so_no_total e por_parcela podem divergir por arredondamento, nunca muito."""
    por_parcela = calcular_pasep(_entrada(BASE)).total_principal
    pol_total = PoliticaCalculo(
        momento=MomentoArredondamento.SO_NO_TOTAL, modo="ROUND_HALF_UP", casas=2
    )
    so_total = calcular_pasep(
        EntradaPasep(data_calculo=date(2026, 7, 23), politica=pol_total, parcelas=tuple(BASE))
    ).total_principal
    assert abs(por_parcela - so_total) <= Decimal("0.03")
