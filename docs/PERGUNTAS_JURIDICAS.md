# Perguntas jurídicas — respostas necessárias antes da Fase 2

O motor não inventa critério jurídico para preencher lacuna: pergunta
(PROMPT_VALUE.md §14). Estas são as decisões que preciso de você, advogado, antes
de implementar o cálculo. Cada resposta vira parâmetro de política e/ou dado na
tabela de regime, com registro de quem decidiu e quando.

## Bloco A — parâmetros de `config/politica_escritorio.yaml` (§5)

1. **`pasep.base`** — a parcela anual usa o salário mínimo **cheio** do ano, ou
   **proporcional** aos meses trabalhados (1/12)?
2. **`pasep.ancoragem`** — ancorar no **ano-base** ou no **exercício de pagamento**
   do abono?
3. **`honorarios.marco_juros`** — os juros dos honorários correm da **citação**,
   do **trânsito em julgado** ou do **arbitramento**? (Defeito nº 1 do paradigma.)
4. **`honorarios.base`** — sobre **valor da causa atualizado** ou **valor da
   condenação**?
5. **`arredondamento.momento`** — arredondar **por parcela** ou **só no total**?
6. **`arredondamento.modo` / `casas`** — confirmar **ROUND_HALF_UP**, 2 casas?
7. **`lacuna_ec136.tese_principal`** — Cenário **A**, **B** ou **C** como principal?
8. **`emissao.cenarios`** — sempre os **três** cenários, ou apenas o principal com
   nota de ressalva?

## Bloco B — regime e prescrição

9. **PASEP — elegibilidade dos 5 anos de cadastramento.** Confirmar que, na
   indenização substitutiva, o quinquênio conta-se da **admissão** (dada a omissão
   do ente em inscrever), e não da inscrição efetiva.
10. **Prescrição (Súmula 85 STJ).** Confirmar a premissa de trato sucessivo com
    direito não negado, de modo que só prescrevem as prestações anteriores ao
    quinquênio da propositura. Há caso em que o próprio direito foi negado (muda o
    corte)?
11. **Juros — exclusão do mês da citação.** Confirmar a regra usada no paradigma
    (juros excluem o mês inicial; mora uniforme desde a citação para todas as
    parcelas).

## Bloco C — pós-requisitório

12. **Trava pela Selic** (art. 97, §16 e §16-A, ADCT): confirmar a regra "IPCA +
    2% a.a. simples, aplicando a Selic se for menor" e o ponto exato de virada
    (expedição do requisitório como marco).

> Enquanto estas respostas não vierem, a Fase 2 fica parametrizada mas o motor
> recusa emitir (política `PENDENTE`).
