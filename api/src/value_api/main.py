"""Aplicação FastAPI (esqueleto — Fase 4).

On-premise. Não expor à internet pública. Papéis: operador, revisor, admin.
Regra dos quatro olhos aplicada na emissão (revisor != operador), sem exceção
configurável (§9, §14).
"""

from __future__ import annotations

from fastapi import FastAPI

from value_engine import VERSAO_MOTOR

app = FastAPI(
    title="Value — API interna",
    description="Produção de memoriais de cálculo. Uso interno, on-premise.",
    version="0.0.0",
)


@app.get("/saude")
def saude() -> dict[str, str]:
    """Sonda simples de saúde; expõe a versão do motor para rastreabilidade."""
    return {"status": "ok", "versao_motor": VERSAO_MOTOR}


# Rotas de ingestão, parametrização, cálculo, revisão (quatro olhos), emissão e
# geração de PDF/XLSX entram na Fase 4/5. A emissão chamará politica.carregar_politica
# e recusará enquanto houver PENDENTE.
