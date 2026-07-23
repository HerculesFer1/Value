"""Interface `Verba` — contrato que toda verba implementa.

Preparado para extensão (ATS, insalubridade, URV) sem construí-las agora.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ..models import Parcela


@runtime_checkable
class Verba(Protocol):
    """Uma verba sabe gerar suas parcelas originárias a partir de parâmetros.

    A geração das parcelas é o único ponto específico da verba; correção, juros,
    regime temporal, prescrição e honorários são etapas GENÉRICAS aplicadas a
    qualquer verba, e vivem fora daqui.
    """

    #: identificador estável da verba (ex.: "pasep")
    tipo: str

    #: base legal citável (entra na trilha de auditoria por célula)
    base_legal: str

    def gerar_parcelas(self) -> tuple[Parcela, ...]:
        """Produz as parcelas originárias, já validada a elegibilidade por ano."""
        ...
