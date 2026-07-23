"""Coletor BCB/SGS (Sistema Gerenciador de Séries Temporais).

Séries: 4390 (Selic acumulada no mês), 11 (Selic diária), TR/poupança.
Formato da API: JSON [{"data":"dd/MM/aaaa","valor":"0.77"}, ...].

O valor vem como string com 2 casas; convertemos para Decimal na fronteira. O
motor nunca recebe float. O hash do payload bruto carimba a proveniência e força
nova versão quando a fonte muda (append-only).
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal

from ..base import FonteSerie, PontoSerie, SerieColetada

BASE_URL = (
    "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
    "?formato=json&dataInicial={ini}&dataFinal={fim}"
)


def _competencia(data_br: str) -> "datetime.date":  # noqa: F821
    """'dd/MM/aaaa' -> date. Sem tolerância a formato inesperado (falhar é obrigatório)."""
    return datetime.strptime(data_br, "%d/%m/%Y").date()


def parsear_sgs(
    conteudo: bytes,
    *,
    nome: str,
    codigo: int,
    url: str,
    versao: str,
    data_coleta: datetime | None = None,
) -> SerieColetada:
    """Função PURA: payload bruto do SGS -> SerieColetada. Decimal e hash.

    `data_coleta` entra como parâmetro para manter o parse determinístico e
    testável (não lê o relógio aqui).
    """
    bruto = json.loads(conteudo)
    pontos = tuple(
        PontoSerie(competencia=_competencia(item["data"]), valor=Decimal(item["valor"]))
        for item in bruto
    )
    return SerieColetada(
        nome=nome,
        fonte=FonteSerie.BCB_SGS,
        url=url,
        versao=versao,
        data_coleta=data_coleta or datetime.now(UTC),
        hash_conteudo=SerieColetada.hash_de(conteudo),
        pontos=pontos,
    )


def coletar_sgs(
    *,
    nome: str,
    codigo: int,
    ini: str,
    fim: str,
    versao: str,
    timeout: float = 30.0,
) -> SerieColetada:
    """Busca a série no BCB/SGS e devolve a coleta versionada.

    `ini`/`fim` no formato dd/MM/aaaa. Efeito de rede isolado aqui; o parse é puro.
    """
    import httpx  # importado aqui para manter o parse sem dependência de rede

    url = BASE_URL.format(codigo=codigo, ini=ini, fim=fim)
    resposta = httpx.get(url, timeout=timeout)
    resposta.raise_for_status()
    return parsear_sgs(
        resposta.content, nome=nome, codigo=codigo, url=url, versao=versao
    )
