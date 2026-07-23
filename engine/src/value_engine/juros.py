"""Juros de mora — simples (Fase 2).

Juros de mora são SIMPLES, nunca compostos, salvo determinação expressa do título
(PROMPT_VALUE.md §2.2). A mora nasce do marco definido (tipicamente a citação, que
exclui o mês inicial), não do vencimento de cada parcela: no caso-paradigma os
juros de poupança são uniformes em 48,9165% para todas as parcelas.

A taxa acumulada da janela vem da série oficial (poupança/Selic) ou do título; o
motor a recebe e aplica. Função pura, precisão plena, sem arredondar.
"""

from __future__ import annotations

from .tipos import Dinheiro, Percentual


def juros_simples(base: Dinheiro, taxa_acumulada: Percentual) -> Dinheiro:
    """Juros simples = base × taxa acumulada (fração decimal), em Decimal.

    `taxa_acumulada` já é a taxa do período inteiro (ex.: 0.489165 para 48,9165%);
    o motor não compõe juros mês a mês.
    """
    return base * taxa_acumulada
