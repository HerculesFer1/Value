"""Regime temporal — a linha do tempo normativa como DADO, não como código.

Regra de correção e juros vive em tabela versionada com janela de vigência
(PROMPT_VALUE.md §2.4). Uma emenda constitucional é um `INSERT`, não um `git push`.
Nunca codifique regra normativa em `if` (§14).
"""

from __future__ import annotations

from .temporal import (
    JanelaRegime,
    RegimeTemporal,
    carregar_metadados_cenarios_ec136,
    carregar_regime_temporal,
)

__all__ = [
    "JanelaRegime",
    "RegimeTemporal",
    "carregar_metadados_cenarios_ec136",
    "carregar_regime_temporal",
]
