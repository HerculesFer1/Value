"""Núcleo de cálculo do PASEP (Fase 2).

Aritmética derivada e provada contra o caso-paradigma (§10):

  corrigido = SM × fator_correção            (precisão plena)
  juros     = corrigido × taxa_juros         (simples, uniforme desde a citação)
  base      = corrigido + juros
  selic     = base × taxa_selic              (EC 113; taxa acumulada por soma simples)
  atualizado = arredondar(base + selic)      (arredonda conforme a POLÍTICA)

O motor recebe as taxas já acumuladas (fator de correção do CJF, juros da poupança,
Selic acumulada) como PARÂMETRO — nunca as recalcula nem lê o relógio. Tudo em
Decimal; `float` é proibido neste pacote.

O `momento` de arredondamento é decisão de política do escritório (§5). A regra que
reproduz o paradigma é `por_parcela` com `ROUND_HALF_UP`, 2 casas.
"""

from __future__ import annotations

from datetime import date
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal
from enum import Enum

from pydantic import Field

from .correcao import corrigir
from .juros import juros_simples
from .models import LinhaMemorial, _Base
from .tipos import Dinheiro, Fator, Percentual

_MODOS = {
    "ROUND_HALF_UP": ROUND_HALF_UP,
    "ROUND_HALF_EVEN": ROUND_HALF_EVEN,
}


class MomentoArredondamento(str, Enum):
    POR_PARCELA = "por_parcela"
    SO_NO_TOTAL = "so_no_total"


class PoliticaCalculo(_Base):
    """Fatia da política do escritório que o motor precisa (§5).

    O motor recebe isto já resolvido; não lê YAML nem decide política.
    """

    momento: MomentoArredondamento
    modo: str = "ROUND_HALF_UP"
    casas: int = Field(default=2, ge=0, le=6)

    def quantum(self) -> Decimal:
        return Decimal(1).scaleb(-self.casas)  # 2 casas -> 0.01


def arredondar(valor: Dinheiro, politica: PoliticaCalculo) -> Dinheiro:
    """Arredonda conforme a política (modo + casas)."""
    return valor.quantize(politica.quantum(), rounding=_MODOS[politica.modo])


class ParcelaCalc(_Base):
    """Uma parcela pronta para cálculo: valor-base e as taxas acumuladas da janela."""

    competencia: date
    valor_base: Dinheiro          # ex.: salário mínimo do ano-base (PASEP)
    fator_correcao: Fator         # fator IPCA-E (CJF) até o marco de virada
    taxa_juros: Percentual        # juros simples acumulados (poupança), fração
    taxa_selic: Percentual        # Selic acumulada pós-EC 113, fração


class Honorarios(_Base):
    """Honorários: percentual sobre a base atualizada, com marco de juros próprio.

    O marco de juros dos honorários pode divergir do principal (defeito nº 1 do
    paradigma) — por isso é parâmetro explícito, não herança implícita.
    """

    percentual: Percentual
    valor_base: Dinheiro          # valor da causa (ou da condenação, por política)
    fator_correcao: Fator
    taxa_juros: Percentual
    taxa_selic: Percentual


class EntradaPasep(_Base):
    """Entrada do cálculo do PASEP. `data_calculo` é parâmetro — o motor não lê o relógio."""

    data_calculo: date
    politica: PoliticaCalculo
    parcelas: tuple[ParcelaCalc, ...]
    honorarios: Honorarios | None = None


class ParcelaResultado(_Base):
    competencia: date
    corrigido: Dinheiro
    juros: Dinheiro
    base_selic: Dinheiro
    selic: Dinheiro
    atualizado: Dinheiro


class ResultadoPasep(_Base):
    parcelas: tuple[ParcelaResultado, ...]
    total_principal: Dinheiro
    honorarios: Dinheiro
    total_geral: Dinheiro
    linhas: tuple[LinhaMemorial, ...]


def _atualizar(
    valor_base: Dinheiro,
    fator_correcao: Fator,
    taxa_juros: Percentual,
    taxa_selic: Percentual,
) -> tuple[Dinheiro, Dinheiro, Dinheiro, Dinheiro, Dinheiro]:
    """Cadeia de precisão plena: corrigido, juros, base, selic, atualizado_raw."""
    corr = corrigir(valor_base, fator_correcao)
    jur = juros_simples(corr, taxa_juros)
    base = corr + jur
    sel = base * taxa_selic
    return corr, jur, base, sel, base + sel


def calcular_pasep(entrada: EntradaPasep) -> ResultadoPasep:
    """Calcula o memorial do PASEP. Puro e determinístico.

    Arredonda conforme a política: `por_parcela` arredonda cada `atualizado` e
    soma; `so_no_total` mantém precisão plena e arredonda apenas os totais.
    """
    pol = entrada.politica
    por_parcela = pol.momento is MomentoArredondamento.POR_PARCELA

    parcelas_res: list[ParcelaResultado] = []
    linhas: list[LinhaMemorial] = []
    total_principal_raw = Decimal(0)

    for p in entrada.parcelas:
        corr, jur, base, sel, at_raw = _atualizar(
            p.valor_base, p.fator_correcao, p.taxa_juros, p.taxa_selic
        )
        at = arredondar(at_raw, pol) if por_parcela else at_raw
        total_principal_raw += at
        parcelas_res.append(
            ParcelaResultado(
                competencia=p.competencia,
                corrigido=arredondar(corr, pol),
                juros=arredondar(jur, pol),
                base_selic=arredondar(base, pol),
                selic=arredondar(sel, pol),
                atualizado=arredondar(at_raw, pol),
            )
        )
        linhas.append(
            LinhaMemorial(
                etapa=f"pasep {p.competencia.year}",
                fator=p.fator_correcao,
                valor=arredondar(at_raw, pol),
                ref_dispositivo="",   # preenchido pela api a partir do título
                ref_norma="art. 239, §3º, CF; LC 8/70",
                ref_serie="",         # preenchido pela api a partir da série usada
            )
        )

    total_principal = arredondar(total_principal_raw, pol)

    honor = Decimal(0)
    if entrada.honorarios is not None:
        h = entrada.honorarios
        _, _, _, _, h_at_raw = _atualizar(
            h.valor_base, h.fator_correcao, h.taxa_juros, h.taxa_selic
        )
        honor = arredondar(h_at_raw * h.percentual, pol)

    total_geral = arredondar(total_principal + honor, pol)

    return ResultadoPasep(
        parcelas=tuple(parcelas_res),
        total_principal=total_principal,
        honorarios=honor,
        total_geral=total_geral,
        linhas=tuple(linhas),
    )
