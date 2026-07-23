# ADR 0003 — Acumulação da Selic (EC 113) por soma simples; fonte e precisão

- **Status:** aceito (premissa confirmada na Fase 1)
- **Data:** 2026-07-23
- **Contexto:** PROMPT_VALUE.md §2.2, §3, §7, §10 (defeito nº 4); Fase 1

## Contexto

Sob a EC 113/2021, a Selic única engloba correção e juros no período
09/12/2021–09/09/2025. O caso-paradigma declara "Selic dez/2021→jul/2026 de
55,3103%". Precisávamos fixar, com prova, **como** a Selic acumula, para o coletor
e o motor produzirem esse número de forma reproduzível.

## Investigação (Fase 1, dado real)

Coletamos a série BCB/SGS 4390 (Selic acumulada no mês) e testamos duas hipóteses
de acumulação no intervalo dez/2021 → jun/2026:

| Método | Resultado | Veredito |
|---|---|---|
| **Soma simples** das taxas mensais | **55,3100%** | reproduz o paradigma |
| Capitalização composta ∏(1+i) | 74,8311% | diverge ~20 pontos — descartado |

Nota temporal: a data de cálculo é 23/07/2026; julho não fechou. A soma vai até o
último mês fechado (jun/2026). O rótulo "→jul/2026" designa a data da apuração,
não um mês de julho somado.

## Decisão

1. **Acumulação da Selic da EC 113 = soma simples das taxas mensais.** Coerente
   com juros de mora simples (§2.2) e com a prática da Contadoria. Composição só se
   o título determinar expressamente.
2. **Fonte e modo de acumulação são declarados na trilha de auditoria** (corrige o
   defeito nº 4 do paradigma): série BCB/SGS, código, versão, hash; método = soma
   simples; intervalo com marco inicial e mês final fechado.

## Resíduo em aberto (0,0003pp)

A SGS 4390 publica a taxa mensal com 2 casas (`"0.77"`); a soma dá 55,3100%, contra
os 55,3103% do paradigma — resíduo de 0,0003pp, dentro da tolerância declarada
(±R$ 0,01/parcela). A reprodução **exata** dos 55,3103% provavelmente exige a Selic
diária (SGS 11) capitalizada dentro do mês. Ação: ao integrar a SGS 11, verificar
se fecha os 55,3103 e, em caso positivo, adotá-la como fonte de precisão. Até lá, o
sistema declara 55,3100% com fonte 4390 e o método, nunca um número não rastreável.

## Consequências

O utilitário de validação da Fase 1 (`value_indices.acumulacao.soma_simples_percent`)
implementa a soma simples e é coberto por teste com payload cacheado. A versão
autoritativa da acumulação, usada na emissão, será portada ao motor na Fase 2, a
partir da série versionada — nunca recalculando fora da fonte oficial.
