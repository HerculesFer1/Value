"""Carga e validação da política do escritório.

Enquanto qualquer chave for `PENDENTE`, o sistema recusa emitir memorial
(PROMPT_VALUE.md §5). Esta função é o portão: a emissão a chama antes de tudo.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from value_engine.errors import PoliticaPendente

_SENTINELA = "PENDENTE"


def _achatar(d: dict[str, Any], prefixo: str = "") -> list[tuple[str, Any]]:
    itens: list[tuple[str, Any]] = []
    for k, v in d.items():
        chave = f"{prefixo}{k}"
        if isinstance(v, dict):
            itens.extend(_achatar(v, f"{chave}."))
        else:
            itens.append((chave, v))
    return itens


def carregar_politica(caminho: Path) -> dict[str, Any]:
    """Carrega a política e RECUSA se houver qualquer PENDENTE."""
    dados = yaml.safe_load(caminho.read_text(encoding="utf-8"))
    pendentes = [k for k, v in _achatar(dados) if v == _SENTINELA]
    if pendentes:
        raise PoliticaPendente(
            "política do escritório incompleta; decida antes de emitir: "
            + ", ".join(sorted(pendentes))
        )
    return dados
