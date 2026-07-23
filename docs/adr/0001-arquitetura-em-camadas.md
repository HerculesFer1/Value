# ADR 0001 — Arquitetura em camadas com motor puro

- **Status:** aceito
- **Data:** 2026-07-23
- **Contexto normativo:** PROMPT_VALUE.md §2, §6, §13

## Contexto

O Value produz memoriais de cálculo que são juntados aos autos e conferidos pela
Contadoria Judicial. O produto não é um número, é uma peça auditável e
reproduzível. Um erro não é bug: é excesso de execução, impugnação e perda de
honorários. A metáfora que rege o projeto: o título judicial é o código-fonte, o
memorial é o artefato compilado, a Contadoria é o verificador.

Isso impõe requisitos que a arquitetura precisa garantir por construção, não por
disciplina: determinismo total, imutabilidade da emissão, `Decimal` em todo o
caminho, regras normativas como dado, e recusa de emitir diante de dado faltante.

## Decisão

Monorepo com quatro fronteiras rígidas:

```
value/
├─ engine/   motor puro: sem I/O, sem rede, sem banco, sem relógio
├─ api/      FastAPI: persistência, autenticação, orquestração
├─ web/      React + TypeScript: interface interna
├─ indices/  coletores de séries oficiais (executáveis isolados)
├─ docs/     ADRs, vigilância normativa, manual do operador
└─ fixtures/ casos-paradigma e casos sintéticos de validação
```

Princípios que decorrem e que a estrutura faz cumprir:

1. **`engine/` é sagrado.** Funções puras; entrada e saída são modelos Pydantic v2;
   zero dependência de infraestrutura. Recebe a data de cálculo como parâmetro —
   nunca lê o relógio. 100% da lógica jurídica e 100% da cobertura de testes vivem
   aqui. Um teste (`engine/tests/test_no_float.py`) falha se `float` aparecer no
   pacote do motor.
2. **Regras normativas são dado.** A linha do tempo de correção/juros vive em
   `engine/.../regime/regime_temporal.yaml` com janelas de vigência versionadas.
   Uma emenda constitucional é um `INSERT`, não um `git push`. Nunca `if` normativo.
3. **Séries oficiais são coletadas isoladamente** em `indices/`, gravadas
   *append-only* com `(fonte, url, versao, data_coleta, hash_conteudo)`. Revisão
   de índice cria versão nova, jamais sobrescreve.
4. **Determinismo e imutabilidade.** A emissão congela um snapshot: entrada,
   versões de todas as séries, versão do motor, hash da saída. Recalcular no
   futuro reproduz byte a byte.
5. **A api orquestra e persiste; o motor calcula.** O banco usa `NUMERIC`, jamais
   `DOUBLE PRECISION`. Papéis (`operador`, `revisor`, `admin`) e a regra dos
   quatro olhos vivem na api, não no motor.
6. **On-premise.** Dados sob sigilo profissional (art. 34, VII, EOAB, e LGPD).
   Sem nuvem pública sem decisão explícita. Sem exposição à internet aberta.

## Consequências

**Positivas.** O motor é testável sem infraestrutura (Oráculo A: casos sintéticos
contra a calculadora do CJF). O determinismo permite regressão por snapshot. A
separação de séries em `indices/` permite auditar a proveniência de cada número.

**Custos aceitos.** Duplicação de modelos entre `engine` (Pydantic) e `api`
(SQLAlchemy) — deliberada, para manter o motor sem dependência de ORM. Passar a
data de cálculo e as séries como parâmetro torna as assinaturas mais verbosas —
é o preço do determinismo.

**Rejeitado.** Uma única aplicação FastAPI com a lógica de cálculo embutida:
quebra o determinismo e a testabilidade, e mistura relógio/banco com cálculo.
