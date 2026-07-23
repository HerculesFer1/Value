"""Erros do motor. Falhar é obrigatório (PROMPT_VALUE.md §2.8).

O motor nunca extrapola, nunca assume valor padrão silencioso. Diante de campo
obrigatório em branco, série sem cobertura do período ou marco temporal ausente,
ele levanta uma destas exceções e recusa produzir número.
"""

from __future__ import annotations


class ErroDoMotor(Exception):
    """Base de todos os erros do motor."""


class DadoObrigatorioAusente(ErroDoMotor):
    """Campo obrigatório em branco. Ex.: marco de citação não informado."""


class SerieSemCobertura(ErroDoMotor):
    """A série oficial não cobre a competência pedida.

    Nunca interpolar nem extrapolar: é recusa de emissão, não aproximação.
    """


class RegimeIndefinido(ErroDoMotor):
    """Nenhuma (ou mais de uma) janela de `regime_temporal` cobre a data.

    Sobreposição ou lacuna na tabela de regime é erro de dado normativo e
    precisa de decisão humana — jamais de escolha implícita.
    """


class TeseControvertida(ErroDoMotor):
    """Ponto em disputa alcançado sem cenários habilitados.

    Emitir número único num ponto controvertido, sem sinalizar, é o modo de
    falha mais grave possível (PROMPT_VALUE.md §2.7). Quando o cálculo atravessa
    uma lacuna (ex.: pós-10/09/2025, EC 136/2025), o motor exige cenários.
    """


class PoliticaPendente(ErroDoMotor):
    """Há parâmetro `PENDENTE` em config/politica_escritorio.yaml.

    O sistema recusa emitir enquanto qualquer decisão de política estiver aberta.
    """
