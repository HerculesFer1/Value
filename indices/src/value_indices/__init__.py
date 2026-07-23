"""value_indices — coletores de séries oficiais.

Cada série é coletada por script isolado e gravada append-only com
(fonte, url, versao, data_coleta, hash_conteudo). Revisão de índice cria versão
nova, jamais sobrescreve (PROMPT_VALUE.md §7).

Aqui `float` é tolerado apenas no transporte bruto vindo da fonte; a conversão
para Decimal acontece na fronteira, antes de qualquer persistência ou cálculo.
O motor NUNCA recebe float.
"""

from __future__ import annotations

from .base import FonteSerie, PontoSerie, SerieColetada

__all__ = ["FonteSerie", "PontoSerie", "SerieColetada"]
