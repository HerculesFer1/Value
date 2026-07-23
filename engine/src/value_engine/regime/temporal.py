"""Carga e resolução da tabela de regime temporal.

A tabela é DADO versionado (regime_temporal.yaml). Em produção, a versão vigente
vem do banco via api e é passada ao motor; o arquivo empacotado aqui é a semente
de referência e a fonte dos testes do motor.

Este módulo faz apenas: (1) parsear a tabela para modelos Pydantic e (2) resolver
qual janela cobre uma data. A APLICAÇÃO das regras de correção/juros (o cálculo
monetário em si) é da Fase 2 e vive em outros módulos, ainda como esqueleto.
"""

from __future__ import annotations

import importlib.resources as resources
from datetime import date
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict

from ..errors import RegimeIndefinido

_ARQUIVO_SEMENTE = "regime_temporal.yaml"


class JanelaRegime(BaseModel):
    """Uma janela de vigência da tabela de regime temporal."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str
    vigencia_ini: date | None
    vigencia_fim: date | None
    regra_correcao: str
    regra_juros: str
    status: str  # "vigente" | "controvertido"
    fundamento: str
    depende_de_marco: str | None = None

    @property
    def controvertida(self) -> bool:
        return self.status == "controvertido"

    def cobre(self, quando: date) -> bool:
        """A janela cobre `quando`? Janelas dependentes de marco não são temporais."""
        if self.depende_de_marco is not None:
            return False
        depois_do_inicio = self.vigencia_ini is None or quando >= self.vigencia_ini
        antes_do_fim = self.vigencia_fim is None or quando <= self.vigencia_fim
        return depois_do_inicio and antes_do_fim


class RegimeTemporal(BaseModel):
    """A tabela inteira, versionada."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    versao_tabela: int
    escopo: str
    data_referencia: date
    janelas: tuple[JanelaRegime, ...]

    def janela_para(self, quando: date) -> JanelaRegime:
        """Retorna a única janela temporal que cobre `quando`.

        Lacuna ou sobreposição é erro de dado normativo, não escolha implícita:
        levanta RegimeIndefinido (PROMPT_VALUE.md §2.8, §14).
        """
        cobrem = [j for j in self.janelas if j.cobre(quando)]
        if len(cobrem) == 0:
            raise RegimeIndefinido(
                f"nenhuma janela de regime temporal cobre {quando.isoformat()}"
            )
        if len(cobrem) > 1:
            ids = ", ".join(j.id for j in cobrem)
            raise RegimeIndefinido(
                f"sobreposição de janelas em {quando.isoformat()}: {ids}"
            )
        return cobrem[0]


def carregar_regime_temporal(dados: dict[str, Any] | None = None) -> RegimeTemporal:
    """Constrói o RegimeTemporal.

    Sem argumento, lê a tabela-semente empacotada. Com `dados`, valida o dict
    fornecido (é assim que a api injeta a versão vigente do banco).
    """
    if dados is None:
        texto = (
            resources.files("value_engine.regime")
            .joinpath(_ARQUIVO_SEMENTE)
            .read_text(encoding="utf-8")
        )
        dados = yaml.safe_load(texto)
    return RegimeTemporal.model_validate(dados)
