"""Fixture nº 1 — caso-paradigma (processo 0000392-65.2011.8.18.0037).

O motor deve bater AO CENTAVO (PROMPT_VALUE.md §10). Marcado `xfail` (strict) até a
Fase 2 implementar o cálculo: quando o motor passar a reproduzir o paradigma, o
xfail vira XPASS e o strict acusa que a marcação precisa ser removida.
"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pytest

FIXTURE = (
    Path(__file__).resolve().parents[2] / "fixtures" / "paradigma_pasep_amarante.json"
)


def _fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_fixture_existe_e_e_coerente() -> None:
    """Sanidade da própria fixture — passa já na Fase 0.

    A soma dos 'atualizado' das parcelas confere com o total do principal, em
    Decimal exato (sem float).
    """
    dados = _fixture()
    soma = sum(
        (Decimal(p["atualizado"]) for p in dados["parcelas"]), Decimal("0")
    )
    assert soma == Decimal(dados["totais_principal"]["atualizado"])
    # total geral = principal atualizado + honorários
    total = Decimal(dados["totais_principal"]["atualizado"]) + Decimal(
        dados["honorarios"]["honorarios"]
    )
    assert total == Decimal(dados["total_geral"])


@pytest.mark.paradigma
@pytest.mark.xfail(
    reason="motor ainda não implementado (Fase 2); deve bater ao centavo",
    strict=True,
    raises=NotImplementedError,
)
def test_motor_reproduz_paradigma_ao_centavo() -> None:
    from value_engine.motor import calcular
    from value_engine.models import EntradaCalculo
    from value_engine.regime import carregar_regime_temporal

    _ = _fixture()
    # Fase 2: montar EntradaCalculo a partir da fixture e comparar cada parcela
    # com tolerância de ±R$ 0,01, e o total com 15.642,83 exato.
    entrada = EntradaCalculo(
        data_calculo=__import__("datetime").date(2026, 7, 23),
        marcos=(),
        parcelas=(),
    )
    calcular(entrada, carregar_regime_temporal())
