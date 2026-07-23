"""Parse do BCB/SGS: bytes brutos -> SerieColetada em Decimal, com proveniência."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from pathlib import Path

from value_indices.coletores import parsear_sgs

GOLDEN = Path(__file__).resolve().parent / "dados" / "sgs_4390_dez2021_jul2026.json"


def _serie():
    return parsear_sgs(
        GOLDEN.read_bytes(),
        nome="selic_mensal",
        codigo=4390,
        url="golden://sgs_4390",
        versao="teste",
        data_coleta=None,
    )


def test_parse_gera_decimais() -> None:
    serie = _serie()
    assert len(serie.pontos) == 56
    primeiro = serie.pontos[0]
    assert primeiro.competencia == date(2021, 12, 1)
    assert primeiro.valor == Decimal("0.77")
    assert all(isinstance(p.valor, Decimal) for p in serie.pontos)


def test_hash_e_proveniencia() -> None:
    serie = _serie()
    assert len(serie.hash_conteudo) == 64
    assert serie.fonte.value == "bcb_sgs"
    # hash é do conteúdo bruto: reparse do mesmo payload dá o mesmo hash
    assert _serie().hash_conteudo == serie.hash_conteudo
