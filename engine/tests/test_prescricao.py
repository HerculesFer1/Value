"""Corte prescricional (Súmula 85 STJ): correção, idempotência, monotonicidade."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from value_engine.models import Parcela
from value_engine.prescricao import cortar


def _p(ano: int) -> Parcela:
    return Parcela(
        competencia=date(ano, 1, 1),
        valor_originario=Decimal("100.00"),
        origem_do_valor="teste",
        vencimento=date(ano, 12, 31),
    )


PARCELAS = tuple(_p(a) for a in range(2004, 2012))  # 2004..2011


def test_corta_anteriores_ao_quinquenio() -> None:
    # ajuizamento 25/10/2011 -> corte 25/10/2006; vencimentos 31/12 preservam 2006+
    restantes = cortar(PARCELAS, date(2011, 10, 25))
    anos = [p.competencia.year for p in restantes]
    assert anos == [2006, 2007, 2008, 2009, 2010, 2011]


def test_idempotente() -> None:
    uma = cortar(PARCELAS, date(2011, 10, 25))
    duas = cortar(uma, date(2011, 10, 25))
    assert uma == duas


def test_monotonicidade_temporal() -> None:
    """Ajuizar mais cedo desloca o quinquênio para trás e preserva MAIS parcelas."""
    cedo = cortar(PARCELAS, date(2010, 1, 1))    # corte 2005 -> preserva 2005..2011
    tarde = cortar(PARCELAS, date(2011, 10, 25))  # corte 2006 -> preserva 2006..2011
    assert len(cedo) >= len(tarde)


def test_ordem_nao_afeta_conjunto() -> None:
    invertidas = tuple(reversed(PARCELAS))
    assert set(cortar(invertidas, date(2011, 10, 25))) == set(
        cortar(PARCELAS, date(2011, 10, 25))
    )
