"""Indenização substitutiva do PASEP — a única verba da v1 (PROMPT_VALUE.md §4).

Fórmula (abono anual, art. 239, §3º, CF; LC 8/70; Leis 7.859/89 e 7.998/90):

    parcela(ano) = salario_minimo_referencia(ano) × [fator de proporcionalidade,
                                                      se aplicável]

Elegibilidade a validar POR ANO:
  * remuneração mensal até 2 salários mínimos;
  * atividade remunerada por ao menos 30 dias no ano-base;
  * 5 anos de cadastramento no PASEP (na indenização substitutiva, conta-se da
    admissão, dada a omissão do ente em inscrever).

Dois parâmetros de política afetam a base (config/politica_escritorio.yaml):
  * pasep.base       — SM cheio do ano OU proporcional aos meses (1/12);
  * pasep.ancoragem  — ano-base OU exercício de pagamento do abono.

FASE 2: implementar. Este é o esqueleto tipado; não fabricar números agora.
"""

from __future__ import annotations

from ..models import Parcela


class VerbaPasep:
    """Indenização substitutiva do PASEP."""

    tipo = "pasep"
    base_legal = "art. 239, §3º, CF; LC 8/70; Leis 7.859/89 e 7.998/90"

    def gerar_parcelas(self) -> tuple[Parcela, ...]:
        raise NotImplementedError(
            "PASEP: geração de parcelas é da Fase 2. Depende de pasep.base e "
            "pasep.ancoragem (política do escritório) e da série de salário mínimo."
        )
