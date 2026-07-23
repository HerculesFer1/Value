"""Estruturas de proveniência das séries coletadas.

Toda série coletada carrega sua origem verificável. O hash do conteúdo permite
detectar revisão da fonte e forçar nova versão (append-only), nunca sobrescrita.
"""

from __future__ import annotations

import hashlib
from datetime import date, datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class FonteSerie(str, Enum):
    BCB_SGS = "bcb_sgs"        # Selic (4390 mensal, 11 diária), TR/poupança
    IBGE_SIDRA = "ibge_sidra"  # IPCA e IPCA-E
    IPEADATA = "ipeadata"      # salário mínimo histórico
    CJF = "cjf"                # tabela de correção (Manual; Res. 990/2026)


class PontoSerie(BaseModel):
    """Um ponto (competência, valor) de uma série. Valor em Decimal."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    competencia: date
    valor: Decimal


class SerieColetada(BaseModel):
    """Uma coleta versionada e verificável de uma série."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    nome: str                      # ex.: "selic_mensal_4390"
    fonte: FonteSerie
    url: str
    versao: str                    # incremental; nova coleta = nova versão
    data_coleta: datetime
    hash_conteudo: str = Field(min_length=64, max_length=64)
    pontos: tuple[PontoSerie, ...]

    @staticmethod
    def hash_de(conteudo_bruto: bytes) -> str:
        """SHA-256 do payload bruto da fonte, para carimbar a proveniência."""
        return hashlib.sha256(conteudo_bruto).hexdigest()
