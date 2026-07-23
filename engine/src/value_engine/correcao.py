"""Correção monetária. FASE 2 — esqueleto tipado.

A fonte primária de correção é a tabela do CJF (Manual de Orientação; versão
vigente Res. CJF nº 990, de 13/07/2026). Não recalcular IPCA-E por conta própria.
Divergência entre a tabela do CJF e o índice bruto do IBGE gera ALERTA, não
correção silenciosa (PROMPT_VALUE.md §7).

Não fabricar fatores aqui: eles vêm da série oficial versionada, injetada pela api.
"""

from __future__ import annotations

from datetime import date

from .tipos import Dinheiro, Fator


def corrigir(valor: Dinheiro, de: date, ate: date, fator: Fator) -> Dinheiro:
    """Aplica um fator de correção já obtido da série oficial.

    O motor não decide qual índice: recebe o fator correspondente à janela de
    regime e à série versionada. Determinístico, em Decimal.
    """
    raise NotImplementedError("Correção monetária: Fase 2.")
