"""Corte prescricional — Súmula 85 do STJ (Fase 2).

Nas relações de trato sucessivo com a Fazenda Pública, quando não negado o próprio
direito, a prescrição atinge apenas as prestações vencidas antes do quinquênio
anterior à propositura (Decreto 20.910/32, art. 1º). PROMPT_VALUE.md §3.

Função pura e determinística; idempotente por construção. Quando o próprio direito
foi negado, o corte é outro (fundo de direito) — caso a tratar à parte, com decisão
jurídica; este corte assume trato sucessivo com direito não negado.
"""

from __future__ import annotations

from datetime import date

from .models import Parcela


def _quinquenio_antes(quando: date) -> date:
    """Data cinco anos antes de `quando`, tratando 29/02 → 28/02."""
    try:
        return quando.replace(year=quando.year - 5)
    except ValueError:  # 29/02 em ano não bissexto
        return quando.replace(year=quando.year - 5, day=28)


def cortar(
    parcelas: tuple[Parcela, ...], data_ajuizamento: date
) -> tuple[Parcela, ...]:
    """Mantém as parcelas vencidas dentro do quinquênio anterior à propositura.

    Prescrevem as vencidas ANTES do corte; preservam-se as com vencimento no corte
    ou depois. Idempotente: cortar de novo não remove mais nada.
    """
    corte = _quinquenio_antes(data_ajuizamento)
    return tuple(p for p in parcelas if p.vencimento >= corte)
