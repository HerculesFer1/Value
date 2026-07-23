# Manual do operador (rascunho — Fase 7)

Este manual será preenchido quando o fluxo estiver completo (Fase 6/7). Por ora,
registra o fluxo pretendido e os papéis, para orientar a construção.

## Papéis

- **operador** — ingere o título, confirma a extração assistida, parametriza,
  gera o rascunho.
- **revisor** — confere e aprova. A regra dos quatro olhos é inegociável: o
  memorial só sai de `rascunho` para `emitido` com aprovação de um usuário
  **distinto** de quem o produziu. Não há "modo rápido" que pule isto.
- **admin** — gere usuários, séries e a tabela de regime.

## Fluxo

```
ingestão do título (PDF) → OCR e extração assistida → CONFIRMAÇÃO HUMANA obrigatória
  → parametrização (Camada Título) → geração das parcelas → corte prescricional
  → correção → juros → regime pós-2021 → cenários → honorários → consolidação
  → revisão por segundo usuário → emissão (snapshot congelado) → PDF + XLSX
```

## Trilha de auditoria por célula

Toda linha do memorial carrega três ponteiros: (i) dispositivo do título que a
autoriza, (ii) norma que rege a etapa, (iii) ponto da série oficial com versão.
Na interface, a **faixa de proveniência** abre o inspetor lateral com essa cadeia.
No PDF, ela vai em anexo.

## Quando o sistema recusa emitir

- Qualquer parâmetro de política `PENDENTE`.
- Campo obrigatório em branco, série sem cobertura do período, marco ausente.
- Ponto controvertido (lacuna EC 136) sem cenários habilitados.

A recusa é proposital: o sistema nunca extrapola nem assume valor padrão.
