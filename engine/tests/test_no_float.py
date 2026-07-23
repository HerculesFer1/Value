"""Guarda inviolável: NENHUM `float` no pacote do motor (PROMPT_VALUE.md §2.1).

`float` é proibido no caminho de cálculo, na serialização e no banco. Este teste
falha se o token `float` (como chamada, anotação ou construção) aparecer em
qualquer módulo de value_engine. Também barra `DOUBLE PRECISION`.

Comentários e docstrings que mencionam a palavra em prosa são tolerados: a busca
ignora linhas de comentário e conteúdo de strings simples, mirando o CÓDIGO.
"""

from __future__ import annotations

import ast
from pathlib import Path

PACOTE = Path(__file__).resolve().parents[1] / "src" / "value_engine"


def _modulos() -> list[Path]:
    return sorted(PACOTE.rglob("*.py"))


def test_pacote_encontrado() -> None:
    mods = _modulos()
    assert mods, f"nenhum módulo encontrado em {PACOTE}"


def test_sem_float_no_codigo() -> None:
    """Nenhum uso de `float` no AST (nomes, chamadas, anotações)."""
    ofensas: list[str] = []
    for mod in _modulos():
        arvore = ast.parse(mod.read_text(encoding="utf-8"), filename=str(mod))
        for no in ast.walk(arvore):
            if isinstance(no, ast.Name) and no.id == "float":
                ofensas.append(f"{mod.name}:{no.lineno} usa `float`")
            if isinstance(no, ast.Attribute) and no.attr == "float":
                ofensas.append(f"{mod.name}:{no.lineno} usa `.float`")
    assert not ofensas, "float proibido no motor:\n" + "\n".join(ofensas)


def test_sem_double_precision() -> None:
    for mod in _modulos():
        for i, linha in enumerate(mod.read_text(encoding="utf-8").splitlines(), 1):
            codigo = linha.split("#", 1)[0]
            assert "DOUBLE PRECISION" not in codigo.upper(), (
                f"{mod.name}:{i} menciona DOUBLE PRECISION em código"
            )
