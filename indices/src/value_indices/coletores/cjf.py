"""Coletor da tabela de correção do CJF — fonte PRIMÁRIA de correção (§7).

Manual de Orientação de Procedimentos para os Cálculos na Justiça Federal.
Versão vigente: Resolução CJF nº 990, de 13/07/2026 (sucede a Res. 963/2025).
Verificar edição posterior antes de fixar (ver docs/VIGILANCIA_NORMATIVA.md).

Estado: ESQUELETO. A tabela do CJF não tem API JSON limpa como o BCB; depende da
tabela autoritativa (arquivo oficial). Enquanto ela não é ingerida, os 6 fatores
IPCA-E do caso-paradigma (2006–2011) ficam em fixtures/cjf_ipca_e_paradigma.json,
com origem declarada — são números já reproduzidos pelo advogado, não inferência.

NÃO recalcular IPCA-E por conta própria. Divergência entre a tabela do CJF e o
índice bruto do IBGE gera ALERTA, não correção silenciosa.
"""

from __future__ import annotations

from ..base import SerieColetada


def coletar_cjf(*args: object, **kwargs: object) -> SerieColetada:
    raise NotImplementedError(
        "Coletor CJF: requer a tabela autoritativa (Res. CJF nº 990/2026). "
        "Aguardando o arquivo oficial. Interino: fixtures/cjf_ipca_e_paradigma.json."
    )
