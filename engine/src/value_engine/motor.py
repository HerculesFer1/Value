"""Ponto de entrada do motor: `calcular`. FASE 2 — esqueleto tipado.

Orquestra o fluxo puro (PROMPT_VALUE.md §9):

    parcelas → corte prescricional → correção → juros → regime pós-2021
      → cenários (quando atravessa lacuna) → honorários → consolidação

Recebe EntradaCalculo (incluindo `data_calculo` como parâmetro — o motor não lê o
relógio) e o RegimeTemporal (dado versionado, injetado pela api). Devolve
ResultadoCalculo determinístico. Mesma entrada + mesma versão de séries + mesma
versão do motor ⇒ saída idêntica byte a byte.
"""

from __future__ import annotations

from .models import EntradaCalculo, ResultadoCalculo
from .regime import RegimeTemporal

# O cálculo concreto do PASEP (única verba da v1) vive em `calculo.calcular_pasep`
# e já reproduz o caso-paradigma ao centavo. Este entrypoint genérico orquestrará,
# na sequência da Fase 2, a resolução por janelas de regime, a prescrição e os
# cenários da lacuna EC 136 sobre a `EntradaCalculo` genérica do §8.


def calcular(entrada: EntradaCalculo, regime: RegimeTemporal) -> ResultadoCalculo:
    """Orquestrador genérico (§8). Função pura, determinística, em Decimal.

    Onde o cálculo atravessa ponto controvertido (ex.: lacuna EC 136/2025 pós
    10/09/2025), preencherá `ResultadoCalculo.cenarios` e NÃO escolherá número
    único (§2.7). Para o PASEP da v1, use `calculo.calcular_pasep`.
    """
    raise NotImplementedError(
        "Orquestrador genérico §8: continuação da Fase 2 (resolução por janelas de "
        "regime, prescrição, cenários). O cálculo do PASEP está em calcular_pasep."
    )
