"""Acumulação da Selic para validação da Fase 1.

Sob a EC 113/2021 (Selic única), a acumulação é por SOMA SIMPLES das taxas
mensais — é o que reproduz o caso-paradigma (55,3100% em dez/2021→jun/2026) e a
prática da Contadoria. Juros de mora são simples (PROMPT_VALUE.md §2.2).

Este é um utilitário de VALIDAÇÃO dos coletores (Oráculo A da Fase 1). A versão
autoritativa da acumulação, usada na emissão, vive no motor (Fase 2), a partir da
série versionada. Tudo em Decimal.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from .base import PontoSerie

CEM = Decimal(100)


def soma_simples_percent(
    pontos: tuple[PontoSerie, ...], ini: date, fim: date
) -> Decimal:
    """Soma das taxas mensais no intervalo [ini, fim] inclusive, em pontos percentuais.

    `pontos` são taxas mensais (ex.: SGS 4390). Meses fora do intervalo são
    ignorados; nada é interpolado nem extrapolado.
    """
    return sum(
        (p.valor for p in pontos if ini <= p.competencia <= fim), Decimal(0)
    )


def fator_soma_simples(
    pontos: tuple[PontoSerie, ...], ini: date, fim: date
) -> Decimal:
    """Fator multiplicativo correspondente à soma simples: 1 + soma/100."""
    return Decimal(1) + soma_simples_percent(pontos, ini, fim) / CEM
