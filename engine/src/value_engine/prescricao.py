"""Corte prescricional. FASE 2 — esqueleto tipado.

Súmula 85 do STJ (não do STF): nas relações de trato sucessivo com a Fazenda
Pública, quando não negado o próprio direito, a prescrição atinge apenas as
prestações vencidas antes do quinquênio anterior à propositura (Decreto 20.910/32,
art. 1º). PROMPT_VALUE.md §3.

Propriedades exigidas (testes de propriedade, §10):
  * idempotência: cortar duas vezes = cortar uma vez;
  * monotonicidade: mais tempo nunca reduz o valor.
"""

from __future__ import annotations

from datetime import date

from .models import Parcela


def cortar(
    parcelas: tuple[Parcela, ...], data_ajuizamento: date
) -> tuple[Parcela, ...]:
    """Remove as parcelas vencidas antes do quinquênio anterior à propositura.

    Função pura e determinística; idempotente por construção.
    """
    raise NotImplementedError("Corte prescricional (Súmula 85 STJ): Fase 2.")
