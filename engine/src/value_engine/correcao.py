"""Correção monetária — aplicação de fator (Fase 2).

A fonte primária de correção é a tabela do CJF (Manual; Res. CJF nº 990/2026). O
motor NÃO recalcula IPCA-E: recebe o fator já obtido da série oficial versionada e
o aplica. Divergência entre a tabela do CJF e o índice bruto do IBGE gera alerta no
`indices/`, não correção silenciosa (PROMPT_VALUE.md §7).

Função pura, precisão plena (sem arredondar aqui — o arredondamento acontece no
momento definido pela política, ver `calculo.arredondar`).
"""

from __future__ import annotations

from .tipos import Dinheiro, Fator


def corrigir(valor: Dinheiro, fator: Fator) -> Dinheiro:
    """Valor corrigido = valor × fator, em Decimal, sem arredondar."""
    return valor * fator
