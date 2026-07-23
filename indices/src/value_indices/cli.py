"""CLI dos coletores (Fase 1).

Uso:
    value-coletar selic_mensal --ini 01/12/2021 --fim 31/07/2026 --versao 2026-07
    value-coletar selic_diaria --ini 01/12/2021 --fim 30/06/2026 --versao 2026-07

As séries do BCB/SGS já coletam de verdade. IBGE, IPEAData e CJF entram na
sequência da fase. A coleta grava append-only (nunca sobrescreve).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .coletores import coletar_sgs
from .fontes import CATALOGO

_RAIZ_SERIES = Path("series")

# séries do BCB/SGS que já coletam
_SGS = {"selic_mensal": 4390, "selic_diaria": 11}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="value-coletar")
    parser.add_argument("serie", choices=sorted(CATALOGO), help="série a coletar")
    parser.add_argument("--ini", help="data inicial dd/MM/aaaa")
    parser.add_argument("--fim", help="data final dd/MM/aaaa")
    parser.add_argument("--versao", help="rótulo da versão desta coleta")
    parser.add_argument("--raiz", default=str(_RAIZ_SERIES), help="pasta das séries")
    args = parser.parse_args(argv)

    info = CATALOGO[args.serie]
    print(f"série: {args.serie} — {info['descricao']}", file=sys.stderr)

    if args.serie in _SGS:
        if not (args.ini and args.fim and args.versao):
            parser.error("--ini, --fim e --versao são obrigatórios para séries SGS")
        from .armazenamento import gravar

        coleta = coletar_sgs(
            nome=args.serie,
            codigo=_SGS[args.serie],
            ini=args.ini,
            fim=args.fim,
            versao=args.versao,
        )
        destino = gravar(coleta, Path(args.raiz))
        print(
            f"gravado: {destino} | {len(coleta.pontos)} pontos | "
            f"hash {coleta.hash_conteudo[:12]}…",
            file=sys.stderr,
        )
        return 0

    raise NotImplementedError(
        f"coletor de '{args.serie}' ainda não implementado nesta fase "
        f"(IBGE/IPEAData/CJF entram na sequência)."
    )


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
