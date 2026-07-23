"""Fixture nº 1 — caso-paradigma (processo 0000392-65.2011.8.18.0037).

O motor reproduz o paradigma AO CENTAVO (PROMPT_VALUE.md §10): 6/6 parcelas,
total principal 12.753,33 e total geral 15.642,83 (corrige o defeito nº 3: a
planilha trazia 15.642,84).

As taxas acumuladas (fator IPCA-E do CJF, juros de poupança, Selic) entram como
parâmetro — o motor não as recalcula. A Selic é 55,3103% (a precisão exata; ver
ADR 0003). O momento de arredondamento que reproduz o paradigma é `por_parcela`.
"""

from __future__ import annotations

import json
from datetime import date
from decimal import Decimal
from pathlib import Path

from value_engine.calculo import (
    EntradaPasep,
    Honorarios,
    MomentoArredondamento,
    ParcelaCalc,
    PoliticaCalculo,
    calcular_pasep,
)

FIXTURE = (
    Path(__file__).resolve().parents[2] / "fixtures" / "paradigma_pasep_amarante.json"
)


def _fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def _pct(s: str) -> Decimal:
    return Decimal(s) / Decimal(100)


def _entrada(dados: dict) -> EntradaPasep:
    juros = _pct(dados["marcos"]["juros_poupanca_uniforme_percent"])
    selic = _pct(dados["marcos"]["selic_dez2021_a_jul2026_percent"])
    parcelas = tuple(
        ParcelaCalc(
            competencia=date(p["ano"], 1, 1),
            valor_base=Decimal(p["salario_minimo"]),
            fator_correcao=Decimal(p["fator_ipca_e"]),
            taxa_juros=juros,
            taxa_selic=selic,
        )
        for p in dados["parcelas"]
    )
    h = dados["honorarios"]
    honor = Honorarios(
        percentual=Decimal(h["percentual"]),
        valor_base=Decimal(h["valor_causa"]),
        fator_correcao=Decimal(h["fator_correcao"]),
        taxa_juros=_pct(h["taxa_juros_percent"]),
        taxa_selic=_pct(h["taxa_selic_percent"]),
    )
    return EntradaPasep(
        data_calculo=date(2026, 7, 23),
        politica=PoliticaCalculo(
            momento=MomentoArredondamento.POR_PARCELA, modo="ROUND_HALF_UP", casas=2
        ),
        parcelas=parcelas,
        honorarios=honor,
    )


def test_fixture_existe_e_e_coerente() -> None:
    dados = _fixture()
    soma = sum((Decimal(p["atualizado"]) for p in dados["parcelas"]), Decimal("0"))
    assert soma == Decimal(dados["totais_principal"]["atualizado"])
    total = Decimal(dados["totais_principal"]["atualizado"]) + Decimal(
        dados["honorarios"]["honorarios"]
    )
    assert total == Decimal(dados["total_geral"])


def test_cada_parcela_ao_centavo() -> None:
    dados = _fixture()
    res = calcular_pasep(_entrada(dados))
    for calc, esperado in zip(res.parcelas, dados["parcelas"], strict=True):
        assert calc.atualizado == Decimal(esperado["atualizado"]), (
            f"{esperado['ano']}: {calc.atualizado} != {esperado['atualizado']}"
        )


def test_totais_ao_centavo() -> None:
    dados = _fixture()
    res = calcular_pasep(_entrada(dados))
    assert res.total_principal == Decimal(dados["totais_principal"]["atualizado"])
    assert res.honorarios == Decimal(dados["honorarios"]["honorarios"])
    assert res.total_geral == Decimal(dados["total_geral"])
    # corrige o defeito nº 3: total normalizado é 15.642,83, não 15.642,84
    assert res.total_geral == Decimal("15642.83")


def test_soma_das_parcelas_igual_ao_total() -> None:
    """Propriedade: soma dos atualizados = total principal (momento por_parcela)."""
    dados = _fixture()
    res = calcular_pasep(_entrada(dados))
    soma = sum((p.atualizado for p in res.parcelas), Decimal(0))
    assert soma == res.total_principal
