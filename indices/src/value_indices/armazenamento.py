"""Armazenamento append-only versionado das séries coletadas.

Cada coleta é gravada em series/<nome>/<versao>.jsonl e catalogada em
series/index.jsonl. Revisão de índice cria versão nova; NUNCA sobrescreve
(PROMPT_VALUE.md §2.6, §7). Gravar sobre uma versão existente é erro, não
atualização.

Os dados ficam fora do git (ver .gitignore): são dado versionado por conteúdo e
hash, não código-fonte.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from .base import SerieColetada


class VersaoJaExiste(Exception):
    """Tentativa de sobrescrever uma versão já gravada. Append-only é inviolável."""


def _pasta_serie(raiz: Path, nome: str) -> Path:
    return raiz / nome


def gravar(serie: SerieColetada, raiz: Path) -> Path:
    """Grava a coleta como nova versão. Recusa se a versão já existir."""
    pasta = _pasta_serie(raiz, serie.nome)
    pasta.mkdir(parents=True, exist_ok=True)
    destino = pasta / f"{serie.versao}.jsonl"
    if destino.exists():
        raise VersaoJaExiste(
            f"{serie.nome} v{serie.versao} já existe em {destino}; séries são "
            f"append-only. Crie nova versão."
        )

    with destino.open("w", encoding="utf-8") as fh:
        # cabeçalho de proveniência na primeira linha
        cabecalho = serie.model_dump(mode="json", exclude={"pontos"})
        fh.write(json.dumps(cabecalho, ensure_ascii=False) + "\n")
        for p in serie.pontos:
            fh.write(json.dumps(p.model_dump(mode="json"), ensure_ascii=False) + "\n")

    _catalogar(serie, raiz, destino)
    return destino


def _catalogar(serie: SerieColetada, raiz: Path, destino: Path) -> None:
    raiz.mkdir(parents=True, exist_ok=True)
    entrada = {
        "nome": serie.nome,
        "fonte": serie.fonte.value,
        "versao": serie.versao,
        "url": serie.url,
        "hash_conteudo": serie.hash_conteudo,
        "n_pontos": len(serie.pontos),
        "arquivo": str(destino.relative_to(raiz)),
        "catalogado_em": datetime.now(UTC).isoformat(),
    }
    with (raiz / "index.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entrada, ensure_ascii=False) + "\n")
