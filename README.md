# Value

Sistema interno de produção de **memoriais de cálculo** de créditos de servidores
públicos contra a Fazenda Pública municipal, na Justiça Comum estadual (TJPI).

> Isto **não é uma calculadora.** É um compilador. O título judicial (sentença +
> acórdão) é o código-fonte; o memorial é o artefato compilado; a Contadoria
> Judicial é o verificador. O projeto é construído sob essa metáfora.

O produto final é uma **peça processual auditável** (PDF + planilha XLSX espelho)
que será juntada aos autos e conferida pela Contadoria Judicial e pela procuradoria
do município. Um erro não gera bug — gera excesso de execução, impugnação e perda
de honorários.

---

## Estado atual

**Fase 1 em curso.** Scaffold (Fase 0) completo. Os coletores do BCB/SGS já coletam
de verdade, com armazenamento append-only versionado (fonte, url, versão, hash) e
recusa de sobrescrever. O critério de aceite da Selic foi reproduzido: soma simples
dez/2021→jun/2026 = **55,3100%** (paradigma 55,3103%; resíduo de 0,0003pp
documentado no [ADR 0003](docs/adr/0003-acumulacao-selic-soma-simples.md), a resolver
com a Selic diária). A metade IPCA-E depende da tabela autoritativa do CJF — ver
abaixo. A lógica de cálculo do **motor** segue não implementada (Fase 2): os pontos
onde ela entra são esqueletos tipados que lançam `NotImplementedError`.

O roteiro completo está em [`PROMPT_VALUE.md`](PROMPT_VALUE.md) — a especificação
que origina o projeto. As fases de execução estão na seção 13 desse documento.

| Fase | Entrega | Estado |
|---|---|---|
| 0 | Scaffold do monorepo, tooling, contratos, fixture nº 1 | **feito** |
| 1 | `indices/` — coletores de séries oficiais versionadas | **em curso** — BCB/SGS feito e validado; CJF pendente da tabela |
| 2 | `engine/` — regime temporal, correção, juros, prescrição | a fazer |
| 3 | política do escritório definida + cenários EC 136 | **bloqueado** (ver abaixo) |
| 4 | `api/` + modelo de dados + papéis e quatro olhos | a fazer |
| 5 | geração de PDF e XLSX | a fazer |
| 6 | `web/` com o design da seção 11 | a fazer |
| 7 | Docker Compose, backup, manual do operador | a fazer |

### Bloqueios conhecidos (decisão humana obrigatória)

1. **Parâmetros de política do escritório** — oito chaves estão marcadas
   `PENDENTE` em [`config/politica_escritorio.yaml`](config/politica_escritorio.yaml).
   O sistema **recusa emitir** enquanto houver qualquer `PENDENTE`. Precisam ser
   decididas antes da Fase 3.
2. **Perguntas jurídicas da Fase 2** — ver
   [`docs/PERGUNTAS_JURIDICAS.md`](docs/PERGUNTAS_JURIDICAS.md).
3. **Lacuna normativa pós-10/09/2025 (EC 136/2025)** — três teses concorrentes;
   o motor apresentará cenários e não escolherá. Ver
   [`docs/VIGILANCIA_NORMATIVA.md`](docs/VIGILANCIA_NORMATIVA.md).

---

## Restrições invioláveis (resumo)

Detalhadas na seção 2 do `PROMPT_VALUE.md` e nos ADRs em [`docs/adr/`](docs/adr/).

- **`Decimal` em todo o caminho de cálculo.** `float` é proibido no motor, na
  serialização e no banco (`NUMERIC`, nunca `DOUBLE PRECISION`). Há um teste que
  falha se `float` aparecer no pacote do motor.
- **Juros de mora simples**, nunca compostos, salvo determinação expressa do título.
- **Nenhum LLM no caminho de cálculo.** IA só auxilia a *extração* do título, com
  confirmação humana obrigatória.
- **Regras normativas são dado, não código** — vivem em tabela versionada com
  janela de vigência.
- **Determinismo total** e **imutabilidade da emissão** (snapshot congelado, séries
  *append-only*).
- **Onde a tese é controvertida, o sistema apresenta cenários e não escolhe.**
- **Falhar é obrigatório** diante de campo obrigatório em branco, série sem
  cobertura ou marco ausente. Nunca extrapola.

---

## Arquitetura

Monorepo com quatro fronteiras rígidas (ver
[`docs/adr/0001-arquitetura-em-camadas.md`](docs/adr/0001-arquitetura-em-camadas.md)):

```
value/
├─ engine/     motor puro: sem I/O, sem rede, sem banco, sem relógio. Sagrado.
├─ api/        FastAPI: persistência, autenticação, orquestração
├─ web/        React + TypeScript: interface interna (design Apple / oxblood)
├─ indices/    coletores de séries oficiais (executáveis isolados)
├─ docs/       ADRs, vigilância normativa, manual do operador
├─ fixtures/   casos-paradigma e casos sintéticos de validação
└─ config/     política do escritório (parâmetros que exigem decisão humana)
```

### Stack

- Python 3.12+, `uv`, `ruff`, `mypy --strict`, `pytest`, `hypothesis`
- FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, PostgreSQL 16
- React 19 + TypeScript + Vite + Tailwind CSS v4 + TanStack Query + TanStack Table
- PDF: Jinja2 → WeasyPrint · XLSX: openpyxl
- Docker Compose para tudo

**Hospedagem: local / on-premise.** Dados sob sigilo profissional (art. 34, VII,
EOAB, e LGPD). Nada em nuvem pública sem decisão explícita.

---

## Como rodar (dev)

Pré-requisitos: [`uv`](https://docs.astral.sh/uv/), Node 20+, Docker.

```bash
# instalar o workspace Python (engine + api + indices)
uv sync

# verificações de qualidade
uv run ruff check .
uv run mypy .
uv run pytest

# subir a stack (banco, api, web) — quando as fases 4/6 existirem
docker compose up
```

O scaffold já roda `pytest`: o teste do guarda-`Decimal` passa, e o teste do
fixture-paradigma fica marcado `xfail` até a Fase 2 preencher o motor.

---

## Licença e sigilo

Uso interno do escritório. Não expor à internet pública. Ver
[`docs/adr/0001-arquitetura-em-camadas.md`](docs/adr/0001-arquitetura-em-camadas.md).
