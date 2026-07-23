# Architecture Decision Records (ADR)

Registro cronológico das decisões de arquitetura e das decisões jurídicas que
viram parâmetro. Um ADR não se apaga: quando superado, cria-se um novo com status
`substitui ADR NNNN`.

| ADR | Título | Status |
|---|---|---|
| [0001](0001-arquitetura-em-camadas.md) | Arquitetura em camadas com motor puro | aceito |
| [0002](0002-defeitos-do-paradigma.md) | Cinco defeitos do caso-paradigma a corrigir | aceito |
| [0003](0003-acumulacao-selic-soma-simples.md) | Acumulação da Selic (EC 113) por soma simples; fonte e precisão | aceito |
| [0004](0004-aritmetica-do-motor-e-arredondamento.md) | Aritmética do motor e momento de arredondamento | aceito |
| [0005](0005-cenarios-ec136-motor-nao-escolhe.md) | Lacuna EC 136/2025: o motor apresenta cenários, nunca escolhe | aceito |

## Pendentes de abertura (conforme as fases avançam)

- Decisão de cada parâmetro de `config/politica_escritorio.yaml` (um ADR por
  bloco de decisão, ou um ADR consolidado antes da Fase 3).
- Escolha da tese principal da lacuna EC 136/2025 (`lacuna_ec136.tese_principal`).
- Estratégia de cifragem em repouso dos dados pessoais.
