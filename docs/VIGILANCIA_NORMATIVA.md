# Vigilância normativa

Pendências e fontes normativas que podem alterar a tabela `regime_temporal` ou os
cenários. **Regra de ouro:** alteração normativa é `INSERT` de nova janela/versão
na tabela de dados, com bump de `versao_tabela` — nunca reescrita silenciosa de
regra no código.

- **Última verificação geral:** 2026-07-23
- **Responsável pela verificação:** PENDENTE (definir na equipe)
- **Cadência sugerida:** mensal, e sempre antes de emitir memorial que atravesse
  janela controvertida.

---

## Pendências em aberto

### Tema 1.457/STF — termo inicial de incidência da EC 113/2021
- **Estado (jul/2026):** pendente de julgamento.
- **Impacto esperado:** pode deslocar a fronteira de início do regime Selic única
  (janela `2021_12_09_a_2025_09_09`). Afeta todo cálculo que cruze dez/2021.
- **Ação ao julgar:** revisar `vigencia_ini` da janela Selic; abrir ADR; nova
  `versao_tabela`.

### Lacuna EC 136/2025 — pós-10/09/2025 (fase pré-requisitório)
- **Estado:** lacuna com três teses concorrentes (A: Selic corrida; B: CC arts.
  389/406, Lei 14.905/2024; C: retorno aos Temas 810/905, com objeção de
  repristinação, art. 2º, §3º, LINDB).
- **Fontes:** EC 136/2025 (revogou art. 3º da EC 113); STJ, REsp 2.236.270/SP
  (Rel. Min. Gurgel de Faria, pub. 02/03/2026), que restringiu a nova redação aos
  requisitórios.
- **Tratamento no sistema:** o motor apresenta os três cenários com delta em reais
  e não escolhe. O operador seleciona a tese principal
  (`lacuna_ec136.tese_principal`); o sistema registra quem e quando.
- **Ação ao consolidar jurisprudência:** quando o TJPI/STJ/STF fixarem tese, mover
  de `controvertido` para `vigente` na tabela; abrir ADR.

### Tabela de correção do CJF
- **Versão fixada:** Resolução CJF nº 990, de 13/07/2026 (sucede a Res. 963/2025).
- **Ação:** verificar se houve edição posterior antes de fixar cada emissão. A
  tabela do CJF é a fonte primária de correção; divergência com o IBGE gera
  **alerta**, não correção silenciosa.

---

## Como registrar uma verificação

Acrescente uma linha ao log abaixo a cada verificação, mesmo quando "sem novidade".

| Data | Item verificado | Resultado | Quem |
|---|---|---|---|
| 2026-07-23 | Tema 1.457/STF | pendente, sem julgamento | (scaffold inicial) |
| 2026-07-23 | Lacuna EC 136/2025 | três teses; REsp 2.236.270/SP registrado | (scaffold inicial) |
| 2026-07-23 | Res. CJF 990/2026 | vigente | (scaffold inicial) |
