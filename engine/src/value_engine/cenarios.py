"""Cenários da lacuna EC 136/2025 (pré-requisitório) — o motor apresenta, não escolhe.

EC 136/2025 revogou o art. 3º da EC 113/2021. A partir de 10/09/2025, na fase
pré-requisitório, há três teses concorrentes (PROMPT_VALUE.md §3):

  A — Selic corrida (manutenção do regime EC 113 enquanto não expedido requisitório)
  B — Código Civil, arts. 389 e 406 (Lei 14.905/2024): IPCA + taxa legal
  C — retorno aos Temas 810/905 (IPCA-E + poupança), com objeção da repristinação
      (art. 2º, §3º, LINDB)

Quando o cálculo atravessa 10/09/2025, o memorial OBRIGATORIAMENTE traz os três
cenários com o delta em reais e a fundamentação de cada um. O operador escolhe qual
vai como principal; a api registra quem e quando. O MOTOR NÃO ESCOLHE — emitir um
número único num ponto controvertido é o modo de falha mais grave (§2.7).

Tudo em Decimal. As taxas acumuladas de cada cenário entram como parâmetro.
"""

from __future__ import annotations

from datetime import date

from .calculo import PoliticaCalculo, arredondar
from .correcao import corrigir
from .errors import TeseControvertida
from .juros import juros_simples
from .models import _Base
from .tipos import Dinheiro, Fator, Percentual

#: início da lacuna (EC 136/2025; fase pré-requisitório)
DATA_LACUNA = date(2025, 9, 10)


def atravessa_lacuna(fim_periodo: date) -> bool:
    """O período de cálculo alcança a lacuna pós-10/09/2025?"""
    return fim_periodo >= DATA_LACUNA


class DefinicaoCenario(_Base):
    """Uma tese concorrente, com metadados e as taxas acumuladas do pós-corte."""

    id: str                    # "A" | "B" | "C"
    nome: str
    fundamento: str
    correcao: Fator            # fator de correção acumulado do pós-10/09/2025
    juros: Percentual          # juros acumulados do pós-10/09/2025 (fração)
    ressalva: str | None = None


class ResultadoCenario(_Base):
    id: str
    nome: str
    fundamento: str
    valor: Dinheiro            # valor consolidado sob esta tese
    delta_vs_menor: Dinheiro   # quanto esta tese excede a de menor valor
    ressalva: str | None = None


class ResultadoCenariosEC136(_Base):
    base_em_corte: Dinheiro    # valor consolidado até 09/09/2025
    cenarios: tuple[ResultadoCenario, ...]
    spread: Dinheiro           # maior - menor (amplitude da controvérsia, em reais)
    #: o motor NUNCA escolhe: a tese principal é sempre None aqui. A escolha do
    #: operador é registrada pela api (quem e quando), fora do motor.
    principal: None = None
    controvertido: bool = True


def calcular_cenarios_ec136(
    base_em_corte: Dinheiro,
    definicoes: tuple[DefinicaoCenario, ...],
    politica: PoliticaCalculo,
) -> ResultadoCenariosEC136:
    """Computa cada tese sobre a base consolidada no corte e devolve todas.

    Recusa operar com menos de dois cenários: num ponto controvertido, um número
    único sem sinalização é proibido (§2.7).
    """
    if len(definicoes) < 2:
        raise TeseControvertida(
            "a lacuna EC 136/2025 exige múltiplos cenários; recebido "
            f"{len(definicoes)}. O motor não emite número único em ponto controvertido."
        )

    ids = [d.id for d in definicoes]
    if len(set(ids)) != len(ids):
        raise TeseControvertida(f"cenários com id duplicado: {ids}")

    valores: dict[str, Dinheiro] = {}
    for d in definicoes:
        corr = corrigir(base_em_corte, d.correcao)
        jur = juros_simples(corr, d.juros)
        valores[d.id] = arredondar(corr + jur, politica)

    menor = min(valores.values())
    maior = max(valores.values())

    resultados = tuple(
        ResultadoCenario(
            id=d.id,
            nome=d.nome,
            fundamento=d.fundamento,
            valor=valores[d.id],
            delta_vs_menor=valores[d.id] - menor,
            ressalva=d.ressalva,
        )
        for d in definicoes
    )
    return ResultadoCenariosEC136(
        base_em_corte=base_em_corte,
        cenarios=resultados,
        spread=maior - menor,
    )
