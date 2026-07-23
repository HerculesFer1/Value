"""Armazenamento append-only: grava versão nova, recusa sobrescrever."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from value_indices.armazenamento import VersaoJaExiste, gravar
from value_indices.base import FonteSerie, PontoSerie, SerieColetada


def _serie(versao: str) -> SerieColetada:
    conteudo = b'[{"data":"01/12/2021","valor":"0.77"}]'
    return SerieColetada(
        nome="selic_mensal",
        fonte=FonteSerie.BCB_SGS,
        url="golden://sgs_4390",
        versao=versao,
        data_coleta=datetime.now(UTC),
        hash_conteudo=SerieColetada.hash_de(conteudo),
        pontos=(PontoSerie(competencia=__import__("datetime").date(2021, 12, 1),
                           valor=Decimal("0.77")),),
    )


def test_grava_e_cataloga(tmp_path: Path) -> None:
    destino = gravar(_serie("2026-07"), tmp_path)
    assert destino.exists()
    assert (tmp_path / "index.jsonl").exists()
    linhas = destino.read_text(encoding="utf-8").splitlines()
    assert len(linhas) == 2  # cabeçalho de proveniência + 1 ponto


def test_recusa_sobrescrever(tmp_path: Path) -> None:
    gravar(_serie("2026-07"), tmp_path)
    with pytest.raises(VersaoJaExiste):
        gravar(_serie("2026-07"), tmp_path)


def test_nova_versao_convive(tmp_path: Path) -> None:
    gravar(_serie("2026-07"), tmp_path)
    gravar(_serie("2026-08"), tmp_path)  # não levanta
    assert (tmp_path / "selic_mensal" / "2026-07.jsonl").exists()
    assert (tmp_path / "selic_mensal" / "2026-08.jsonl").exists()
