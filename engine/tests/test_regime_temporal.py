"""Testes da tabela de regime temporal (dado versionado).

Estes passam já na Fase 0: validam a estrutura e a resolução de janelas, não o
cálculo monetário (que é Fase 2).
"""

from __future__ import annotations

from datetime import date

import pytest

from value_engine.errors import RegimeIndefinido
from value_engine.regime import carregar_regime_temporal


def test_semente_carrega() -> None:
    regime = carregar_regime_temporal()
    assert regime.versao_tabela >= 1
    assert regime.janelas


def test_janela_ate_2009() -> None:
    regime = carregar_regime_temporal()
    janela = regime.janela_para(date(2008, 12, 31))
    assert janela.regra_correcao == "ipca_e_cjf"
    assert janela.regra_juros == "mora_simples_0_5_am"


def test_janela_selic_unica() -> None:
    regime = carregar_regime_temporal()
    janela = regime.janela_para(date(2023, 1, 1))
    assert janela.regra_correcao == "selic_unica"


def test_lacuna_ec136_e_controvertida() -> None:
    regime = carregar_regime_temporal()
    janela = regime.janela_para(date(2025, 12, 1))
    assert janela.controvertida, "pós-10/09/2025 tem de estar marcada controvertida"


def test_janela_dependente_de_marco_nao_e_temporal() -> None:
    """A janela pós-requisitório depende do marco, não cobre por data pura."""
    regime = carregar_regime_temporal()
    for j in regime.janelas:
        if j.depende_de_marco is not None:
            assert not j.cobre(date(2030, 1, 1))


def test_data_fora_de_qualquer_janela_falha() -> None:
    """Recusar, nunca extrapolar. Uma tabela com furo levanta RegimeIndefinido."""
    regime = carregar_regime_temporal()
    dados = regime.model_dump()
    # remove a primeira janela (a sem limite inferior) para abrir um furo no passado
    dados["janelas"] = [j for j in dados["janelas"] if j["vigencia_ini"] is not None]
    regime_furado = carregar_regime_temporal(dados)
    with pytest.raises(RegimeIndefinido):
        regime_furado.janela_para(date(1990, 1, 1))
