"""Modelos de entrada e saída do motor (Pydantic v2).

Entrada e saída do motor são modelos Pydantic imutáveis. Todos os valores
monetários e fatores são `Decimal` — nunca `float` (PROMPT_VALUE.md §2.1).

Estes modelos são o *contrato* entre o motor e o resto do sistema. A api serializa
para/desde eles; o motor só conhece isto. Campos serão acrescentados conforme as
fases avançarem — este é o esqueleto mínimo da Fase 0.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from .tipos import Dinheiro, Fator


class _Base(BaseModel):
    """Base imutável e estrita para todos os modelos do motor."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        # Decimal preservado; serialização como string é responsabilidade da api.
        arbitrary_types_allowed=False,
    )


class TipoMarco(str, Enum):
    AJUIZAMENTO = "ajuizamento"
    CITACAO = "citacao"
    TRANSITO = "transito"
    REQUISITORIO = "requisitorio"


class Marco(_Base):
    """Marco temporal do processo. Fonte documental obrigatória."""

    tipo: TipoMarco
    data: date
    fonte_doc: str = Field(min_length=1)


class Parcela(_Base):
    """Uma prestação originária, antes de qualquer correção ou juros."""

    competencia: date
    valor_originario: Dinheiro
    origem_do_valor: str = Field(min_length=1)
    vencimento: date


class LinhaMemorial(_Base):
    """Uma linha do memorial, com sua trilha de auditoria por célula.

    Toda linha carrega três ponteiros (PROMPT_VALUE.md §9): dispositivo do título,
    norma que rege a etapa, e ponto da série oficial com versão. É o que separa
    uma peça auditável de uma planilha de escritório.
    """

    etapa: str
    fator: Fator
    valor: Dinheiro
    ref_dispositivo: str
    ref_norma: str
    ref_serie: str


class EntradaCalculo(_Base):
    """Tudo que o motor precisa para calcular — incluindo a data de cálculo.

    O motor NUNCA lê o relógio: `data_calculo` entra aqui como parâmetro
    (PROMPT_VALUE.md §6).
    """

    data_calculo: date
    marcos: tuple[Marco, ...]
    parcelas: tuple[Parcela, ...]
    # As versões das séries usadas entram no snapshot; preenchidas pela api.
    versoes_series: dict[str, str] = Field(default_factory=dict)


class ResultadoCalculo(_Base):
    """Saída determinística do motor."""

    linhas: tuple[LinhaMemorial, ...]
    total: Dinheiro
    # Cenários concorrentes, quando o cálculo atravessa ponto controvertido.
    # Vazio significa que não houve controvérsia no intervalo calculado.
    cenarios: dict[str, "ResultadoCalculo"] = Field(default_factory=dict)


# Necessário para a auto-referência em `cenarios`.
ResultadoCalculo.model_rebuild()


def total_confere(resultado: ResultadoCalculo) -> bool:
    """Propriedade: a soma das linhas de valor é igual ao total.

    Usada pelos testes de propriedade (hypothesis). Comparação exata em Decimal.
    """
    soma = sum((linha.valor for linha in resultado.linhas), Decimal(0))
    return soma == resultado.total
