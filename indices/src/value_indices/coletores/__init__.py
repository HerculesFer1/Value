"""Coletores concretos por fonte oficial.

Cada coletor separa duas responsabilidades:
  * `parsear_*` — função PURA: bytes brutos da fonte → SerieColetada (Decimal,
    hash). Testável offline com payload cacheado, sem rede.
  * `coletar_*` — busca na fonte (httpx) e delega o parse. Efeito de rede isolado.
"""

from __future__ import annotations

from .bcb_sgs import coletar_sgs, parsear_sgs

__all__ = ["coletar_sgs", "parsear_sgs"]
