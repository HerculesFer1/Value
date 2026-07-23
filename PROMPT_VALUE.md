# PROMPT DE CONSTRUÇÃO — PROJETO **VALUE**

> Cole este documento inteiro como primeira mensagem de uma sessão nova do Claude Code, na raiz de um diretório vazio chamado `value/`.

---

## 0. Papel e contrato de trabalho

Você é o arquiteto e implementador único do sistema **Value**. Eu sou advogado e geotecnólogo, não sou programador: você decide a engenharia, eu decido o direito. Quando uma escolha for técnica, decida e justifique em uma linha. Quando for jurídica ou de política do escritório, **pare e pergunte** — nunca invente.

Regra permanente desta sessão: **não escreva código antes de eu aprovar o plano da fase corrente.** Ao fim de cada fase, pare, mostre o que foi feito e os testes passando, e espere confirmação.

---

## 1. O que o Value é

Sistema interno de produção de **memoriais de cálculo** de créditos de servidores públicos contra a Fazenda Pública municipal, na Justiça Comum estadual (TJPI).

- **Usuários**: exclusivamente a equipe interna do escritório. Sem cadastro público, sem exposição à internet aberta.
- **Saída**: memorial em PDF (e planilha XLSX espelho) **que será juntado aos autos** e conferido pela Contadoria Judicial e pela procuradoria do município.
- **Consequência disso**: o produto não é "um número". É uma peça processual auditável. Um erro não gera bug — gera excesso de execução, impugnação e perda de honorários.

O erro conceitual a evitar desde a primeira linha: **isto não é uma calculadora.** É um compilador. O título judicial (sentença + acórdão) é o código-fonte; o memorial é o artefato compilado; a Contadoria é o verificador. Projete assim.

---

## 2. Restrições invioláveis

Estas não são preferências. Violá-las invalida o sistema.

1. **`Decimal` em todo o caminho de cálculo.** `float` é proibido no motor, na serialização e no banco (`NUMERIC`, nunca `DOUBLE PRECISION`). Adicione um teste que falha se algum `float` aparecer no pacote do motor.
2. **Juros de mora são simples, nunca compostos**, salvo determinação expressa do título.
3. **Nenhum LLM no caminho de cálculo.** IA pode auxiliar a *extração* de dados do título, sempre com confirmação humana obrigatória e campo `confirmado_por`. Nenhum número do memorial pode ter sido produzido por inferência estatística.
4. **Regras normativas são dado, não código.** Regime de correção e juros vive em tabela versionada com janela de vigência. Uma emenda constitucional é um `INSERT`, não um `git push`.
5. **Determinismo total.** Mesma entrada + mesma versão das séries + mesma versão do motor ⇒ saída idêntica, byte a byte. Recalcular um memorial emitido em 2026 daqui a três anos tem que devolver exatamente o que foi protocolado.
6. **Imutabilidade da emissão.** Ao emitir, congela-se um *snapshot*: entrada, versões de todas as séries, versão do motor, hash da saída. Séries são *append-only* — revisão de índice cria versão nova, jamais sobrescreve.
7. **Onde a tese é controvertida, o sistema apresenta cenários e não escolhe.** Emitir número único num ponto em disputa, sem sinalizar, é o modo de falha mais grave possível.
8. **Falhar é obrigatório.** Campo obrigatório em branco, série sem cobertura do período, marco temporal ausente ⇒ o sistema recusa emitir. Nunca extrapola, nunca assume valor padrão silencioso.

---

## 3. Domínio jurídico — a linha do tempo normativa

Este é o núcleo. Modele como tabela `regime_temporal`, com `(norma, escopo, vigencia_ini, vigencia_fim, regra_correcao, regra_juros, status)`.

| Janela | Correção monetária | Juros de mora | Fundamento |
|---|---|---|---|
| até 29/06/2009 | IPCA‑E (tabela CJF) | 0,5% a.m. simples | art. 1º‑F Lei 9.494/97 (red. MP 2.180‑35/2001); Tema 810/STF |
| 30/06/2009 – 08/12/2021 | IPCA‑E (tabela CJF) | poupança: 0,5% a.m. ou 70% da Selic mensalizada, o menor; simples | art. 1º‑F Lei 9.494/97 (red. Lei 11.960/2009); Tema 810/STF e Tema 905/STJ |
| 09/12/2021 – 09/09/2025 | Selic única (engloba correção e juros; vedado fracionar) | — | art. 3º EC 113/2021, redação original; Tema 1.419/STF |
| a partir de 10/09/2025, **fase pré‑requisitório** | **LACUNA — três teses concorrentes** | idem | EC 136/2025 revogou o art. 3º da EC 113; STJ, REsp 2.236.270/SP (Rel. Min. Gurgel de Faria, pub. 02/03/2026), restringiu a nova redação aos requisitórios |
| após expedição de precatório/RPV | IPCA + juros simples de 2% a.a., com trava pela Selic (aplica‑se a Selic se for menor) | idem | art. 3º EC 113/2021 c/ red. EC 136/2025; art. 97, §16 e §16‑A, ADCT |

**Cenários obrigatórios para a lacuna pós‑10/09/2025 (pré‑requisitório):**

- **Cenário A** — Selic corrida (tese de manutenção enquanto não expedido requisitório; adotada por câmaras do TJSP).
- **Cenário B** — Código Civil, arts. 389 e 406 com redação da Lei 14.905/2024 (IPCA + taxa legal), a partir de 10/09/2025.
- **Cenário C** — retorno aos Temas 810/905 (IPCA‑E + poupança). Registre a objeção da vedação à repristinação (art. 2º, §3º, LINDB) no próprio relatório.

Quando o cálculo atravessar 10/09/2025, o memorial **obrigatoriamente** traz os três cenários com o delta em reais e a fundamentação de cada um. O operador escolhe qual vai como principal; o sistema registra quem escolheu e quando.

**Pendência a monitorar**: Tema 1.457/STF (termo inicial de incidência da EC 113/2021) estava pendente de julgamento em julho/2026. Crie `docs/VIGILANCIA_NORMATIVA.md` com essa e outras pendências, data da última verificação e impacto esperado.

**Prescrição**: Súmula 85 do **STJ** (não do STF) — nas relações de trato sucessivo com a Fazenda Pública, quando não negado o próprio direito, a prescrição atinge apenas as prestações vencidas antes do quinquênio anterior à propositura. Decreto 20.910/32, art. 1º.

---

## 4. Verbas na versão 1

**Escopo da v1: apenas indenização substitutiva do PASEP.** Não implemente adicional por tempo de serviço, insalubridade ou URV agora. Deixe a arquitetura preparada (interface `Verba`), mas não construa.

**Fórmula do PASEP** (abono anual, art. 239, §3º, CF; LC 8/70; Leis 7.859/89 e 7.998/90):

```
parcela(ano) = salario_minimo_referencia(ano) × [fator de proporcionalidade, se aplicável]
```

Requisitos de elegibilidade a validar por ano: remuneração mensal até 2 salários mínimos; atividade remunerada por ao menos 30 dias no ano‑base; 5 anos de cadastramento no PASEP (na indenização substitutiva, conta‑se da admissão, dada a omissão do ente em inscrever).

---

## 5. Parâmetros de política do escritório

Estes valores **eu ainda não defini**. Crie `config/politica_escritorio.yaml` com todos eles explicitamente marcados como `PENDENTE`, e faça o sistema **recusar emitir memorial** enquanto houver qualquer `PENDENTE`. Me pergunte cada um antes da Fase 3.

| Chave | Decisão pendente |
|---|---|
| `pasep.base` | salário mínimo cheio do ano **ou** proporcional aos meses trabalhados (1/12) |
| `pasep.ancoragem` | ano‑base **ou** exercício de pagamento do abono |
| `honorarios.marco_juros` | citação, trânsito em julgado **ou** arbitramento |
| `honorarios.base` | valor da causa atualizado **ou** valor da condenação |
| `arredondamento.momento` | por parcela **ou** só no total |
| `arredondamento.modo` | `ROUND_HALF_UP`, 2 casas (confirmar) |
| `lacuna_ec136.tese_principal` | Cenário A, B ou C |
| `emissao.cenarios` | sempre os três **ou** apenas o principal com nota de ressalva |

---

## 6. Arquitetura

Monorepo com quatro fronteiras rígidas:

```
value/
├─ engine/          # motor puro: sem I/O, sem rede, sem banco, sem data atual
├─ api/             # FastAPI: persistência, autenticação, orquestração
├─ web/             # React + TypeScript: interface interna
├─ indices/         # coletores de séries oficiais (executáveis isolados)
├─ docs/            # ADRs, vigilância normativa, manual do operador
└─ fixtures/        # casos‑paradigma e casos sintéticos de validação
```

**`engine/` é sagrado.** Funções puras, entrada e saída como modelos Pydantic v2, zero dependência de infraestrutura. Recebe a data de cálculo como parâmetro — nunca lê o relógio. É onde vive 100% da lógica jurídica e onde vive 100% da cobertura de testes.

**Stack:**

- Python 3.12+, `uv`, `ruff`, `mypy --strict`, `pytest`, `hypothesis`
- FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, PostgreSQL 16
- React 19 + TypeScript + Vite + Tailwind CSS v4 + TanStack Query + TanStack Table
- PDF: Jinja2 → WeasyPrint (controle fino de CSS de impressão). XLSX: openpyxl
- Docker Compose para tudo

**Hospedagem: local / on‑premise.** Os dados são de clientes sob sigilo profissional (art. 34, VII, EOAB, e LGPD). Não proponha nuvem pública sem me perguntar antes.

---

## 7. Coletores de séries (`indices/`)

Cada série é coletada por script isolado e gravada com `(fonte, url, versao, data_coleta, hash_conteudo)`.

| Série | Fonte |
|---|---|
| Selic acumulada no mês | BCB/SGS série **4390** — `https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados?formato=json&dataInicial=dd/MM/aaaa&dataFinal=dd/MM/aaaa` |
| Selic diária | BCB/SGS série **11** |
| TR / poupança | BCB/SGS |
| IPCA e IPCA‑E | IBGE / SIDRA |
| Salário mínimo histórico | IPEAData |
| Tabela de correção monetária | CJF — Manual de Orientação de Procedimentos para os Cálculos na Justiça Federal. **Versão vigente: Resolução CJF nº 990, de 13/07/2026** (sucede a Res. CJF nº 963/2025). Verifique se houve edição posterior antes de fixar. |

A tabela do CJF é a fonte primária de correção — não recalcule IPCA‑E por conta própria. Divergência entre a tabela do CJF e o índice bruto do IBGE deve gerar alerta, não correção silenciosa.

---

## 8. Modelo de dados (esqueleto)

```
processo         (numero_cnj, comarca, ente_devedor, esfera, teto_rpv)
titulo           (processo_id, tipo, data_transito, hash_pdf, dispositivo_json)
exequente        (processo_id, matricula, data_admissao, data_efetivacao, regime)
marco            (processo_id, tipo[ajuizamento|citacao|transito|requisitorio], data, fonte_doc)
verba            (titulo_id, tipo, base_legal, parametros_json)
parcela          (verba_id, competencia, valor_originario, origem_do_valor, vencimento)
regime_temporal  (norma, escopo, vigencia_ini, vigencia_fim, regra_correcao, regra_juros)
serie_indice     (nome, competencia, valor, fonte, versao, hash, data_coleta)
execucao_calculo (snapshot_json, versao_motor, versoes_series, hash_entrada, hash_saida, emitido_por, revisado_por, emitido_em)
linha_memorial   (execucao_id, parcela_id, etapa, fator, valor, ref_dispositivo, ref_norma, ref_serie)
desfecho         (execucao_id, status[homologado|impugnado|pago], fundamento_impugnacao, data)
```

A tabela `desfecho` não é acessória — **é o mecanismo que faz o corpus de validação crescer sozinho.** Todo memorial emitido volta com resultado, e toda impugnação vira teste de regressão. Sem isso, o projeto morre de novo em dois anos por falta de referências.

Dados pessoais: CPF, RG e endereço são armazenados cifrados em repouso e **mascarados por padrão na interface**, com revelação sob log. Nenhum deles entra no cálculo.

---

## 9. Fluxo e controle de qualidade

```
ingestão do título (PDF) → OCR e extração assistida → CONFIRMAÇÃO HUMANA obrigatória
  → parametrização (Camada Título) → geração das parcelas → corte prescricional
  → correção → juros → regime pós‑2021 → cenários → honorários → consolidação
  → revisão por segundo usuário → emissão (snapshot congelado) → PDF + XLSX
```

**Regra dos quatro olhos**: o memorial só sai de `rascunho` para `emitido` com aprovação de um usuário **distinto** de quem o produziu. Papéis: `operador`, `revisor`, `admin`. Sem exceção configurável.

**Trilha de auditoria por célula**: toda linha do memorial carrega três ponteiros — (i) dispositivo do título que a autoriza, (ii) norma que rege a etapa, (iii) ponto da série oficial com versão. O PDF traz essa trilha em anexo. É isso que separa uma peça auditável de uma planilha de escritório.

---

## 10. Estratégia de testes — dois oráculos independentes

Esta separação é o que destrava o projeto. Trate como dois problemas distintos.

**Oráculo A — o motor está certo?**
Não precisa de processo real. Gere casos sintéticos cobrindo todas as janelas normativas e compare contra a calculadora oficial do CJF e as planilhas dos TRFs. Meta: 300+ casos, tolerância declarada de ±R$ 0,01 por parcela. Fixtures ilimitadas e gratuitas — comece por aqui.

**Oráculo B — a parametrização está certa?**
Precisa de títulos e memoriais reais. Recurso escasso. Ordem de peso probatório: cálculo da Contadoria Judicial > memorial homologado sem impugnação > memorial impugnado + decisão da impugnação > memorial do escritório ainda não testado.

**Testes de propriedade (hypothesis):** soma das parcelas = total; corte prescricional idempotente; monotonicidade temporal (mais tempo nunca reduz o valor); invariância à ordem das parcelas; recálculo do snapshot reproduz a saída original.

### Fixture nº 1 — caso‑paradigma (processo 0000392‑65.2011.8.18.0037)

Já reproduzi essa aritmética integralmente. Grave como `fixtures/paradigma_pasep_amarante.json` e faça o motor bater **ao centavo**.

Marcos: citação 25/10/2011 (juros excluem o mês inicial) · correção IPCA‑E até dez/2021 · juros de poupança simples, uniformes em **48,9165%** para todas as parcelas (a mora nasce da citação, não do vencimento de cada abono) · Selic dez/2021→jul/2026 de **55,3103%**.

| Ano | SM | Fator IPCA‑E | Corrigido | Juros | Base Selic | Selic | Atualizado |
|---|---|---|---|---|---|---|---|
| 2006 | 350,00 | 2,3492924649 | 822,25 | 402,22 | 1.224,47 | 677,26 | 1.901,73 |
| 2007 | 380,00 | 2,2711258509 | 863,03 | 422,17 | 1.285,19 | 710,84 | 1.996,03 |
| 2008 | 415,00 | 2,1447909444 | 890,09 | 435,40 | 1.325,49 | 733,13 | 2.058,62 |
| 2009 | 465,00 | 2,0447005225 | 950,79 | 465,09 | 1.415,88 | 783,12 | 2.199,00 |
| 2010 | 510,00 | 1,9462066354 | 992,57 | 485,53 | 1.478,10 | 817,54 | 2.295,63 |
| 2011 | 545,00 | 1,8265282269 | 995,46 | 486,95 | 1.482,40 | 819,92 | 2.302,32 |
| | | **Totais** | 5.514,18 | 2.697,36 | 8.211,53 | 4.541,80 | **12.753,33** |

Honorários (20% do valor da causa, fixados em sentença anterior ao CPC/2015): valor da causa R$ 5.000,00 (out/2011) × 1,8101960511 = 9.050,98 · juros 251,39 · base 9.302,37 · Selic 5.145,14 · atualizado 14.447,51 · **honorários 2.889,50**. Total: **R$ 15.642,83**.

**Cinco defeitos do paradigma que você deve corrigir, não replicar** — registre cada um como ADR:

1. O marco de juros dos honorários (2,7775%) diverge do principal (48,9165%) sem justificativa documentada. Precisa virar parâmetro explícito.
2. O rótulo "Índice de correção – ago/20" é falso: o fator 1,8101960511 tem base out/2011. Resíduo de planilha.
3. Somatório não normalizado: o total correto é 15.642,83; a planilha traz 15.642,84.
4. A fonte da Selic e o modo de acumulação não são declarados. Tornar reproduzível é requisito, não melhoria.
5. O critério do PASEP (SM cheio, ancorado no ano‑base) não está explicitado. Vira parâmetro de política.

---

## 11. Design da interface

**Direção fixada: referência Apple — premium e institucional.** Siga isto literalmente; não substitua por um visual genérico de dashboard.

**O que "Apple" significa aqui**, concretamente:

- Tipografia: `-apple-system, BlinkMacSystemFont, "SF Pro Text", Inter, system-ui` (renderiza como SF Pro em dispositivos Apple; Inter como fallback licenciável). Escala tipográfica restrita: 11 / 13 / 15 / 17 / 22 / 28 / 34 px. Pesos 400, 500, 600 — nunca 700+ em texto corrido.
- Grade de 8pt. Respiro generoso no invólucro (navegação, cabeçalhos, cartões), densidade alta nas tabelas de dados. Essa tensão é deliberada: a casca respira, o dado é compacto.
- Divisórias em fio de cabelo (1px, baixo contraste), não bordas pesadas. Sombras suaves e curtas, jamais difusas.
- Raio de canto consistente: 10px em cartões, 8px em controles, 6px em campos.
- Movimento curto e contido: 200–280ms, `cubic-bezier(0.4, 0, 0.2, 1)`. Respeite `prefers-reduced-motion`.
- Modo claro e escuro, ambos de primeira classe.

**Paleta** (nomeada, 6 valores — derive tudo daqui):

| Token | Claro | Escuro | Uso |
|---|---|---|---|
| `superficie-base` | `#FBFBFD` | `#1D1D1F` | fundo da aplicação |
| `superficie-elevada` | `#FFFFFF` | `#2C2C2E` | cartões, painéis |
| `fio` | `#D2D2D7` | `#3A3A3C` | divisórias |
| `texto-primario` | `#1D1D1F` | `#F5F5F7` | conteúdo |
| `texto-secundario` | `#6E6E73` | `#98989D` | rótulos, metadados |
| `acento` | `#6B2737` | `#A84D60` | ações primárias, selo |

O acento é um **oxblood profundo**, não o azul da Apple. Justificativa: a estrutura é Apple (respiro, fio de cabelo, contenção); a identidade cromática vem do mundo do assunto — encadernação jurídica, selo, tinta de carimbo. Se preferir aderência estrita à Apple, troque por `#0071E3` e me avise — mas a escolha acima é a recomendada, e é o que impede a interface de parecer um painel de SaaS qualquer.

Semânticos: `#1D6F42` conferido/homologado · `#B25E09` cenário alternativo ou tese controvertida · o próprio acento para divergência/impugnado.

**Números são o conteúdo.** Toda tabela financeira usa `font-variant-numeric: tabular-nums`, alinhamento à direita, e face de dados monoespaçada (`ui-monospace, "SF Mono", "JetBrains Mono"`). Colunas de valores precisam alinhar dígito a dígito — num sistema de cálculo isso não é estética, é legibilidade forense.

**Elemento‑assinatura: a faixa de proveniência.** Todo valor exibido carrega um marcador discreto. Ao acioná‑lo, abre‑se um inspetor lateral (painel fixo, separado por fio de cabelo — não modal) que mostra a cadeia completa: *dispositivo do título → norma vigente na janela → ponto da série oficial, com versão e hash*. É a coisa que este produto faz e nenhum outro faz. Toda a contenção do resto da interface existe para que esse gesto seja o momento memorável.

**Escrita da interface**: voz ativa, frases em caixa baixa após a primeira letra, sem floreio. O botão diz "Emitir memorial" e o aviso resultante diz "Memorial emitido". Erros explicam o que houve e como resolver, sem pedir desculpas. Tela vazia é convite à ação, não decoração.

**Piso de qualidade, sem anunciar**: navegação por teclado com foco visível, contraste AA, responsivo até tablet (não precisa de celular — é ferramenta de mesa).

---

## 12. O documento emitido

O PDF é a peça que vai aos autos. Trate‑o com o mesmo cuidado da interface, mas com gramática forense:

- Cabeçalho institucional do escritório, número CNJ, partes, comarca, juízo
- Notas explicativas declarando **cada** critério aplicado, com fundamento legal
- Tabelas de apuração por verba, resumo geral
- Anexo com a trilha de auditoria e as versões de séries usadas
- Rodapé com hash de verificação da emissão e data
- Quando houver cenários, quadro comparativo com delta em reais e fundamentação de cada tese

XLSX espelho com fórmulas vivas — a Contadoria frequentemente pede a planilha, e PDF perde as fórmulas.

---

## 13. Fases de execução

Pare ao fim de cada uma.

| Fase | Entrega | Critério de aceite |
|---|---|---|
| **1** | `indices/` completo, séries coletadas e versionadas | reproduz 55,3103% (Selic dez/21→jul/26) e os 6 fatores IPCA‑E do paradigma |
| **2** | `engine/` com regime temporal, correção, juros, prescrição | fixture nº 1 bate ao centavo; 300+ casos sintéticos contra a calculadora do CJF |
| **3** | política do escritório definida + cenários EC 136 | emite os três cenários com deltas corretos |
| **4** | `api/` + modelo de dados + papéis e quatro olhos | snapshot recalculado reproduz a saída original |
| **5** | geração de PDF e XLSX | memorial do paradigma reproduzido em PDF, revisado por mim |
| **6** | `web/` com o design da seção 11 | fluxo completo: ingestão → emissão, com faixa de proveniência funcionando |
| **7** | Docker Compose, backup, manual do operador | equipe usa sem você |

---

## 14. O que NÃO fazer

- Não implemente ATS, insalubridade ou URV na v1.
- Não use `float`, em lugar nenhum.
- Não deixe o motor ler o relógio do sistema.
- Não codifique regra normativa em `if`.
- Não escolha sozinho entre teses em disputa.
- Não atualize série de índice sobrescrevendo a anterior.
- Não exponha o sistema à internet pública.
- Não invente critério jurídico para preencher lacuna — pergunte.
- Não construa "modo rápido" que pule a revisão por segundo usuário.

---

## 15. Primeira ação

Não escreva código ainda. Comece assim:

1. Leia este documento inteiro e liste o que estiver ambíguo ou faltando.
2. Proponha o plano da **Fase 1** — estrutura de diretórios, esquema de versionamento das séries, e como pretende validar os coletores.
3. Liste as perguntas jurídicas que precisa que eu responda antes da Fase 2.
4. Crie `docs/adr/0001-arquitetura-em-camadas.md` registrando as decisões da seção 6.

Espere minha aprovação antes de implementar.
