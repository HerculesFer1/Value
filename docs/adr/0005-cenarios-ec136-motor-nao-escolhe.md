# ADR 0005 — Lacuna EC 136/2025: o motor apresenta cenários, nunca escolhe

- **Status:** aceito
- **Data:** 2026-07-23
- **Contexto:** PROMPT_VALUE.md §2.7, §3, §5, §14; `regime/cenarios_ec136.yaml`

## Contexto

A EC 136/2025 revogou o art. 3º da EC 113/2021. A partir de 10/09/2025, na fase
pré-requisitório, o regime de correção e juros é **controvertido**: há três teses
concorrentes, sem definição jurisprudencial fixada (Tema 1.419/STF e o REsp
2.236.270/SP delimitam, mas não fecham a lacuna pré-requisitório).

Emitir um número único num ponto controvertido, sem sinalizar, é o modo de falha
mais grave possível (§2.7). Por outro lado, o operador precisa de um número
principal para a peça.

## Decisão

1. **Quando o cálculo atravessa 10/09/2025, o motor computa os três cenários** e os
   devolve com o valor de cada tese, o **delta em reais** vs. o de menor valor, e o
   **spread** (amplitude da controvérsia). Implementado em
   `value_engine.cenarios.calcular_cenarios_ec136`.

   - **A** — Selic corrida (manutenção do regime EC 113 até o requisitório).
   - **B** — Código Civil, arts. 389/406 (Lei 14.905/2024): IPCA + taxa legal.
   - **C** — retorno aos Temas 810/905 (IPCA-E + poupança), com a **ressalva** da
     vedação à repristinação (art. 2º, §3º, LINDB) carregada no resultado.

2. **O motor NUNCA elege a tese principal.** `ResultadoCenariosEC136.principal` é
   sempre `None`; `controvertido` é sempre `True`. A escolha do operador — e o
   registro de **quem** escolheu e **quando** — é responsabilidade da api, fora do
   motor puro.

3. **Recusa de cenário único.** Chamar o cálculo da lacuna com menos de dois
   cenários levanta `TeseControvertida`. Não há caminho que produza número único
   nesse ponto sem sinalização.

4. As **taxas acumuladas** de cada cenário (correção e juros do pós-10/09/2025) são
   parâmetro, vindas das séries oficiais versionadas; o YAML-semente
   (`cenarios_ec136.yaml`) fornece apenas a moldura jurídica (id, nome, fundamento,
   ressalva).

## Pendências que interagem com esta decisão

- **Política `lacuna_ec136.tese_principal`** (§5): qual cenário o escritório adota
  por padrão como principal. É decisão de política, aplicada pela api, não pelo
  motor.
- **Política `emissao.cenarios`** (§5): sempre os três, ou principal com nota de
  ressalva. Também aplicada na emissão (api).
- **Vigilância** (Tema 1.419/STF, jurisprudência do TJPI): quando a lacuna fechar,
  mover a janela de `controvertido` para `vigente` na tabela de regime; abrir ADR.

## Consequências

O sistema honra o §2.7 por construção: no ponto mais perigoso do domínio, é
impossível emitir número único sem sinalizar a controvérsia. Coberto por testes
(três cenários, deltas, recusa de cenário único, ressalva da repristinação, motor
não escolhe principal).
