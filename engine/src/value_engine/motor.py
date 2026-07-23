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


def calcular(entrada: EntradaCalculo, regime: RegimeTemporal) -> ResultadoCalculo:
    """Calcula o memorial. Função pura, determinística, em Decimal.

    Onde o cálculo atravessa ponto controvertido (ex.: lacuna EC 136/2025 pós
    10/09/2025), preenche `ResultadoCalculo.cenarios` e NÃO escolhe um número
    único (§2.7).
    """
    raise NotImplementedError(
        "Orquestração do cálculo: Fase 2. Requer correção, juros, prescrição e "
        "cenários implementados, e a política do escritório definida (§5)."
    )
