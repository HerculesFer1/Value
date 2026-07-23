"""value_engine — motor puro de cálculo de memoriais.

Contrato inviolável deste pacote (ver PROMPT_VALUE.md §2 e docs/adr/):

  * `Decimal` em todo o caminho de cálculo. `float` é PROIBIDO aqui — há um teste
    (engine/tests/test_no_float.py) que falha se o token aparecer no pacote.
  * Nenhum I/O, rede, banco ou leitura de relógio. A data de cálculo entra como
    parâmetro; o motor nunca chama datetime.now().
  * Funções puras. Mesma entrada + mesma versão das séries + mesma versão do motor
    ⇒ saída idêntica, byte a byte (determinismo total).
  * Regras normativas são dado (ver regime.RegimeTemporal), nunca `if` embutido.

A lógica jurídica ainda NÃO está implementada — este é o scaffold da Fase 0.
Os pontos de cálculo lançam NotImplementedError com a fase de destino.
"""

from __future__ import annotations

# Versão do motor. Entra no snapshot de emissão e garante reprodutibilidade.
# Incrementar SEMPRE que a lógica de cálculo mudar de forma observável.
VERSAO_MOTOR = "0.0.0"

__all__ = ["VERSAO_MOTOR"]
