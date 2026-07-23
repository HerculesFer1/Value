"""Tipos monetários e de fator. Decimal em todo o caminho (PROMPT_VALUE.md §2.1).

`float` é proibido no pacote do motor. Estes aliases existem para que a intenção
fique explícita na assinatura das funções e dos modelos.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Annotated

from pydantic import Field

# Valor em reais. Serializado como string para não passar por float em lugar nenhum.
Dinheiro = Decimal

# Fator multiplicativo adimensional (ex.: fator IPCA-E, acumulação Selic).
# Guardamos toda a precisão publicada pela fonte oficial; o arredondamento para
# 2 casas acontece só no momento definido pela política do escritório.
Fator = Decimal

# Percentual expresso como fração decimal (ex.: 0.489165 para 48,9165%).
Percentual = Decimal

# Restrição de não-negatividade para valores monetários que não podem ser negativos.
DinheiroNaoNegativo = Annotated[Decimal, Field(ge=0)]
