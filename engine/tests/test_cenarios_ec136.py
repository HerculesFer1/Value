"""Cenários da lacuna EC 136/2025: o motor apresenta as três teses e não escolhe."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from value_engine.calculo import MomentoArredondamento, PoliticaCalculo
from value_engine.cenarios import (
    DATA_LACUNA,
    DefinicaoCenario,
    atravessa_lacuna,
    calcular_cenarios_ec136,
)
from value_engine.errors import TeseControvertida
from value_engine.regime import carregar_metadados_cenarios_ec136

POL = PoliticaCalculo(momento=MomentoArredondamento.POR_PARCELA, modo="ROUND_HALF_UP", casas=2)


def _definicoes() -> tuple[DefinicaoCenario, ...]:
    """Três teses com taxas distintas de exemplo (a api injeta as reais das séries)."""
    meta = {m["id"]: m for m in carregar_metadados_cenarios_ec136()}
    return (
        DefinicaoCenario(
            id="A", nome=meta["A"]["nome"], fundamento=meta["A"]["fundamento"],
            correcao=Decimal("1.00"), juros=Decimal("0.1200"),  # Selic corrida
        ),
        DefinicaoCenario(
            id="B", nome=meta["B"]["nome"], fundamento=meta["B"]["fundamento"],
            correcao=Decimal("1.0500"), juros=Decimal("0.0400"),  # IPCA + taxa legal
        ),
        DefinicaoCenario(
            id="C", nome=meta["C"]["nome"], fundamento=meta["C"]["fundamento"],
            correcao=Decimal("1.0500"), juros=Decimal("0.0250"),  # IPCA-E + poupança
            ressalva=meta["C"].get("ressalva"),
        ),
    )


def test_atravessa_lacuna() -> None:
    assert DATA_LACUNA == date(2025, 9, 10)
    assert atravessa_lacuna(date(2026, 1, 1))
    assert not atravessa_lacuna(date(2025, 9, 9))


def test_tres_cenarios_e_deltas() -> None:
    base = Decimal("10000.00")
    res = calcular_cenarios_ec136(base, _definicoes(), POL)
    assert {c.id for c in res.cenarios} == {"A", "B", "C"}
    # A: 10000×1.00×1.12 = 11200.00 ; B: 10000×1.05×1.04 = 10920.00 ;
    # C: 10000×1.05×1.025 = 10762.50
    valores = {c.id: c.valor for c in res.cenarios}
    assert valores["A"] == Decimal("11200.00")
    assert valores["B"] == Decimal("10920.00")
    assert valores["C"] == Decimal("10762.50")
    # delta vs o menor (C) e spread em reais
    assert next(c.delta_vs_menor for c in res.cenarios if c.id == "A") == Decimal("437.50")
    assert res.spread == Decimal("437.50")


def test_motor_nao_escolhe_principal() -> None:
    """§2.7: o motor nunca elege a tese principal — isso é do operador (via api)."""
    res = calcular_cenarios_ec136(Decimal("10000.00"), _definicoes(), POL)
    assert res.principal is None
    assert res.controvertido is True


def test_recusa_cenario_unico() -> None:
    with pytest.raises(TeseControvertida):
        calcular_cenarios_ec136(Decimal("10000.00"), _definicoes()[:1], POL)


def test_ressalva_repristinacao_no_cenario_c() -> None:
    res = calcular_cenarios_ec136(Decimal("10000.00"), _definicoes(), POL)
    c = next(c for c in res.cenarios if c.id == "C")
    assert c.ressalva is not None and "repristina" in c.ressalva.lower()
