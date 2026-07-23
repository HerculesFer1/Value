"""Juros de mora. FASE 2 — esqueleto tipado.

Juros de mora são SIMPLES, nunca compostos, salvo determinação expressa do título
(PROMPT_VALUE.md §2.2). A mora nasce do marco definido (tipicamente a citação, que
exclui o mês inicial), não do vencimento de cada parcela — no caso-paradigma os
juros de poupança são uniformes em 48,9165% para todas as parcelas.

A regra de juros de cada intervalo vem da tabela de regime temporal (dado).
"""

from __future__ import annotations

from datetime import date

from .tipos import Dinheiro, Percentual


def juros_mora_simples(
    base: Dinheiro, taxa_acumulada: Percentual, marco_juros: date
) -> Dinheiro:
    """Juros simples sobre a base, pela taxa acumulada da janela.

    `taxa_acumulada` já vem calculada a partir da série oficial e do marco; o
    motor não compõe juros. Determinístico, em Decimal.
    """
    raise NotImplementedError("Juros de mora: Fase 2.")
