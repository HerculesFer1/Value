"""CLI dos coletores. FASE 1 — esqueleto.

Uso pretendido:
    value-coletar selic_mensal --ini 01/12/2021 --fim 31/07/2026

Cada coleta grava uma SerieColetada versionada (append-only) com proveniência.
O critério de aceite da Fase 1: reproduzir 55,3103% (Selic dez/21→jul/26) e os
6 fatores IPCA-E do paradigma. Nada é fabricado aqui até a Fase 1.
"""

from __future__ import annotations

import argparse
import sys

from .fontes import CATALOGO


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="value-coletar")
    parser.add_argument("serie", choices=sorted(CATALOGO), help="série a coletar")
    parser.add_argument("--ini", help="data inicial dd/MM/aaaa")
    parser.add_argument("--fim", help="data final dd/MM/aaaa")
    args = parser.parse_args(argv)

    info = CATALOGO[args.serie]
    print(f"série: {args.serie} — {info['descricao']}", file=sys.stderr)
    raise NotImplementedError(
        "Coletor concreto é da Fase 1. Deve baixar da fonte, carimbar hash e "
        "gravar SerieColetada append-only."
    )


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
