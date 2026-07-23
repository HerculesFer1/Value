# ADR 0004 — Aritmética do motor e momento de arredondamento

- **Status:** aceito (derivado e provado contra o paradigma na Fase 2)
- **Data:** 2026-07-23
- **Contexto:** PROMPT_VALUE.md §2.1, §5, §10; ADR 0003

## Contexto

O critério de aceite da Fase 2 é reproduzir o caso-paradigma ao centavo. Derivamos
empiricamente, do próprio paradigma, a cadeia aritmética e a regra de arredondamento
que o reproduzem — em vez de assumir uma regra e torcer para bater.

## Decisão — cadeia de precisão plena, arredonda só o resultado

Por parcela, tudo em `Decimal` com precisão plena, arredondando **apenas** o
`atualizado`:

```
corrigido  = valor_base × fator_correcao          (fator IPCA-E do CJF)
juros      = corrigido × taxa_juros               (simples, uniforme desde a citação)
base       = corrigido + juros
selic      = base × taxa_selic                     (EC 113, soma simples — ADR 0003)
atualizado = arredondar(base + selic)              (por política)
```

Prova (Selic 55,3103%, momento `por_parcela`, `ROUND_HALF_UP`, 2 casas):

| momento | total principal | parcelas ao centavo |
|---|---|---|
| `por_parcela` | **12.753,33 ✓** | **6/6 ✓** |
| `so_no_total` | 12.753,34 ✗ | 6/6 |

Arredondar colunas intermediárias (corrigido, juros) antes de somar **quebra** a
reprodução — por isso a precisão é plena até o `atualizado`.

O **momento** de arredondamento é chave `PENDENTE` da política (§5). A regra que
reproduz o paradigma é `por_parcela`; o motor a recebe como parâmetro e não decide.

## Defeito nº 6 (observado agora): precisão da Selic dividida no paradigma

O principal usou a Selic a **55,3103%** (precisão de série diária), mas os
honorários usaram **55,3100%** (Selic a 2 casas, série 4390) — a mesma Selic, em
duas precisões. É o que faz os honorários fecharem em **2.889,50** e o total geral
em **15.642,83** (o total que o §10 declara correto, corrigindo o defeito nº 3).

Se padronizarmos a precisão alta (55,3103%) também nos honorários, o resultado
consistente é **2.889,51** e total **15.642,84**. Ou seja: o total "correto"
declarado (15.642,83) embute a inconsistência de precisão do paradigma.

**Decisão tomada (2026-07-23):** padronizar a Selic numa **única precisão —
55,3103%** (série diária) para todas as verbas. Consequência: os honorários passam a
**2.889,51** e o total normalizado a **15.642,84**. Isso supera a afirmação do §10
(defeito nº 3) de que o total correto seria 15.642,83 — aquele número dependia da
precisão dividida do paradigma; sob precisão única, o total correto é 15.642,84. A
fixture registra os valores normalizados como alvo e preserva os originais do
paradigma em `valores_originais_paradigma` para rastreabilidade.

## Consequências

`calculo.calcular_pasep` implementa esta cadeia e é coberto por testes de paradigma
(ao centavo) e de propriedade (soma=total, invariância à ordem, determinismo). A
prescrição (Súmula 85 STJ) e as funções de correção/juros são puras e testadas. A
resolução por janelas de regime e os cenários EC 136 seguem para a continuação da
Fase 2.
