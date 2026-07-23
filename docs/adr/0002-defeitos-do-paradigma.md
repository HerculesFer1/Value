# ADR 0002 — Cinco defeitos do caso-paradigma a corrigir, não replicar

- **Status:** aceito
- **Data:** 2026-07-23
- **Contexto:** PROMPT_VALUE.md §10; `fixtures/paradigma_pasep_amarante.json`

## Contexto

O caso-paradigma (processo 0000392-65.2011.8.18.0037) é a âncora ao centavo do
motor. A aritmética foi reproduzida integralmente, mas a planilha de origem carrega
cinco defeitos. O motor deve **corrigir** cada um, não reproduzi-los. Registramo-los
para que a correção seja rastreável e não vire regressão.

## Decisão — os cinco defeitos e o tratamento

1. **Marco de juros dos honorários diverge do principal sem justificativa.**
   No paradigma, honorários usam 2,7775% e o principal 48,9165%. Isso vira o
   parâmetro explícito `honorarios.marco_juros` (citação | trânsito | arbitramento),
   decidido na política do escritório. O motor nunca aplica dois marcos sem que a
   política os declare.

2. **Rótulo de índice falso.** "Índice de correção – ago/20" para o fator
   1,8101960511, cuja base real é out/2011. Resíduo de planilha. O motor rotula
   cada fator pela sua base real, vinda da série versionada.

3. **Somatório não normalizado.** A planilha traz 15.642,84; o total correto é
   15.642,83. O arredondamento passa a ser governado pela política
   (`arredondamento.momento` e `arredondamento.modo`), e o alvo do motor é
   **15.642,83**.

4. **Fonte da Selic e modo de acumulação não declarados.** Reprodutibilidade é
   requisito. A Selic vem da série BCB/SGS versionada (série 4390 acumulada no mês),
   com o modo de acumulação declarado na trilha de auditoria.

5. **Critério do PASEP não explicitado.** SM cheio, ancorado no ano-base, era
   implícito. Vira `pasep.base` e `pasep.ancoragem` na política do escritório.

## Consequências

O motor, ao reproduzir o paradigma na Fase 2, produzirá **15.642,83** (não
15.642,84) e trilha de auditoria com fonte e acumulação declaradas. Os defeitos 1
e 5 dependem de decisão de política (§5) antes da Fase 3.
