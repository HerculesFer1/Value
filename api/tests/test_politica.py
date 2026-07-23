"""O portão da política: recusar emitir enquanto houver PENDENTE (§5)."""

from __future__ import annotations

from pathlib import Path

import pytest

from value_api.politica import carregar_politica
from value_engine.errors import PoliticaPendente

POLITICA = Path(__file__).resolve().parents[2] / "config" / "politica_escritorio.yaml"


def test_politica_pendente_recusa() -> None:
    """Com o arquivo-semente (tudo PENDENTE), a carga tem de recusar."""
    with pytest.raises(PoliticaPendente):
        carregar_politica(POLITICA)


def test_politica_completa_passa(tmp_path: Path) -> None:
    """Sem nenhum PENDENTE, a carga devolve os valores."""
    completa = tmp_path / "politica.yaml"
    completa.write_text(
        "versao_politica: 1\n"
        "decidido_por: teste\n"
        "decidido_em: 2026-07-23\n"
        "pasep:\n  base: sm_cheio\n  ancoragem: ano_base\n"
        "honorarios:\n  marco_juros: citacao\n  base: valor_causa_atualizado\n"
        "arredondamento:\n  momento: por_parcela\n  modo: ROUND_HALF_UP\n  casas: 2\n"
        "lacuna_ec136:\n  tese_principal: A\n"
        "emissao:\n  cenarios: sempre_tres\n",
        encoding="utf-8",
    )
    dados = carregar_politica(completa)
    assert dados["pasep"]["base"] == "sm_cheio"
