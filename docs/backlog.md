# Backlog — RPA_SMART_NEWS

> Backlog mínimo do MVP **RPA_SMART_NEWS**, organizado em **3 releases**:
> `R1 — Core`, `R2 — Qualidade` e `R3 — Entrega Final`.
>
> Cada item referencia os IDs de **Requisitos Funcionais (RF)** definidos
> em [`escopo_mvp.md`](./escopo_mvp.md) e/ou os **Requisitos Técnicos (RT)**
> declarados neste documento (seção [Requisitos Técnicos](#requisitos-técnicos-rt)).
>
> Documento **vivo** — atualizado conforme o projeto evolui.

---

## Sumário

- [Convenções](#convenções)
- [Requisitos Técnicos (RT)](#requisitos-técnicos-rt)
- [Release 1 — Core (fluxo end-to-end mínimo)](#release-1--core-fluxo-end-to-end-mínimo)
- [Release 2 — Qualidade (robustez + GenAI avançada)](#release-2--qualidade-robustez--genai-avançada)
- [Release 3 — Entrega Final (polimento + documentação)](#release-3--entrega-final-polimento--documentação)
- [Definition of Done (DoD)](#definition-of-done-dod)
- [Histórico de revisões](#histórico-de-revisões)

---

## Convenções

- **ID do item**: `B-###` (Backlog item).
- **Refs**: lista de `RF##` (escopo) e/ou `RT##` (técnicos) atendidos.
- **Status**:
  - `[ ]` pendente
  - `[x]` concluído
- **Critérios de aceite (CA)** ficam aninhados como sub-checklist.

---

## Requisitos Técnicos (RT)

Itens de natureza técnica/transversal, não cobertos diretamente pelos
RFs do escopo, mas necessários para a entrega.

| ID | Descrição |
|---|---|
| **RT01** | Estrutura modular dentro de `src/`: `locators/`, `pages/` (com `BasePage` + `BaseNewsPage` + um Page Object por site), `steps/`, `services/`, `models/`, `genai/`, `pdf/`, `utils/`, mais `tests/` na raiz. Padrão **PEP8** + docstrings. |
| **RT02** | Carregamento de configuração via `.env` (`pydantic-settings`) + `.env.example`. |
| **RT03** | Logging estruturado (níveis, timestamps, módulo de origem). |
| **RT04** | Setup de testes com `pytest` + `pytest-cov`. |
| **RT05** | Camada base do Selenium (driver factory, opções) usando **`chromedriver-autoinstaller`**. |
| **RT06** | Cliente LLM **abstraído** por interface (permite trocar provedor). |
| **RT07** | Cliente de embeddings abstraído (similaridade semântica). |
| **RT08** | Integração com biblioteca de geração de PDF. |
| **RT09** | Tipagem (`type hints`) e linter (`ruff`) — opcional. |
| **RT10** | Conventional Commits e branch protection local. |
| **RT11** | Modelos **Pydantic v2** para validação de inputs do usuário e configuração (`.env`). |

---

## Release 1 — Core (fluxo end-to-end mínimo)

> **Objetivo**: rodar o fluxo completo *happy path* — usuário escolhe o
> tema → RPA coleta nas 4 fontes fixas (G1, BBC News Brasil, Agência
> Brasil, R7) → gera um PDF simples com sumarização básica. Sem
> deduplicação semântica, sem clustering, sem polimento.

- [x] **B-001** `[RT01]` — Definir estrutura modular do projeto
  - [x] Pastas em `src/`: `locators/`, `pages/`, `steps/`, `services/`, `models/`, `utils/`, `genai/`, `pdf/` criadas
  - [x] Pasta `tests/` na raiz criada
  - [x] `__init__.py` em cada pacote
  - [x] Código em conformidade com **PEP8** e com **docstrings** (curtas e objetivas)
  - [x] `main.py` passa a chamar o orquestrador em `src/services`

- [x] **B-002** `[RT02]` — Carregamento de configuração via `.env`
  - [x] `.env.example` versionado com chaves esperadas
  - [x] Módulo `src/utils/config.py` lê e valida as variáveis (Pydantic Settings v2)
  - [x] Falha amigável se variável obrigatória estiver ausente (defaults seguros)

- [x] **B-003** `[RT03]` — Logging estruturado
  - [x] Logger central em `src/utils/logger.py`
  - [x] Níveis INFO/WARNING/ERROR habilitados
  - [x] Timestamps em cada linha de log (via `RichHandler`)

- [x] **B-004** `[RF01, RT11]` — CLI com menu de 10 temas
  - [x] Exibe **menu numerado (1–10)** com os temas pré-definidos (ver `docs/escopo_mvp.md` §3)
  - [x] Aceita seleção do usuário (entrada `1` a `10`)
  - [x] Exibe o tema confirmado antes de iniciar a coleta
  - [x] **Sem entrada de número de dias** — única entrada é o tema

- [x] **B-005** `[RT06]` — Cliente LLM abstraído
  - [x] Interface `LLMClient` (Protocol) em `src/genai/llm_client.py`
  - [x] **`StubLLMClient`** offline (default, determinístico)
  - [x] **`OpenAILLMClient`** com lazy-import do pacote `openai`
  - [x] Factory em `src/genai/factory.py` resolve provider via `LLM_PROVIDER`
  - [x] API key carregada do `.env` (`LLM_API_KEY`)

- [x] **B-006** `[RF02, RF03, RT11]` — Validação determinística do tema
  - [x] Modelo **Pydantic v2** (`UserInput`) com campo `topic: Topic`
  - [x] Validação da seleção (somente valores `1–10` aceitos via `IntEnum`)
  - [x] Mensagens de erro amigáveis em pt-BR (mapeando `ValidationError` → texto)
  - [x] **Re-solicita** a entrada em caso de input inválido (com limite de tentativas)
  - [x] **Sem chamada a LLM** — validação puramente determinística

- [x] **B-007** `[RT05, RF04]` — Camada base do Selenium (driver factory)
  - [x] `src/pages/base_page.py` com `BasePage` real (waits, find helpers, scroll humanizado, click tolerante)
  - [x] Driver factory em `src/utils/driver_factory.py` com **`chromedriver-autoinstaller`**
  - [x] Browser abre em modo **visível** (HEADLESS configurável; default `false`)
  - [x] Helpers de humanização em `src/utils/humanize.py` (scroll incremental + delays)

- [x] **B-008** `[RF06, RF07, RT01]` — Page Objects das 4 fontes fixas
  - [x] `src/pages/base_news_page.py` com `BaseNewsPage` (editoria → busca interna; extrai título, URL, fonte, `published_at`, snippet)
  - [x] `src/pages/g1_page.py` (`G1Page`) cobrindo as editorias suportadas e a busca de `g1.globo.com/busca`
  - [x] `src/pages/bbc_brasil_page.py` (`BBCBrasilPage`) com a busca interna `bbc.com/portuguese/search`
  - [x] `src/pages/agencia_brasil_page.py` (`AgenciaBrasilPage`) com editorias e busca interna
  - [x] `src/pages/r7_page.py` (`R7Page`) com editorias e busca interna
  - [x] Locators isolados em `src/locators/<site>_locators.py` (1 arquivo por site)

- [x] **B-009** `[RF06, RF07]` — Coleta orquestrada nas 4 fontes
  - [x] `src/steps/coleta_step.py` itera sobre os Page Objects das 4 fontes
  - [x] Limite máximo configurável por site (`MAX_NEWS_PER_SITE`)
  - [x] Logs por site informam: estratégia usada (editoria/busca) + contagem coletada
  - [x] Notícias com `published_at` extraído são ordenadas por data (mais recentes primeiro)

- [x] **B-010** `[RF14, RNF12]` — Tolerância a falhas
  - [x] Falha em um site é capturada e logada — os demais continuam
  - [x] Timeouts explícitos via `WebDriverWait` (configurável por `SELENIUM_TIMEOUT`)
  - [x] Pipeline aborta com mensagem amigável apenas se **todas** as fontes falharem

- [x] **B-011** `[RF08]` — Deduplicação por URL e título
  - [x] Normalização de URL (`src/utils/dedupe.py`: lowercase host, sem querystring/fragmento, sem trailing slash)
  - [x] Hash de título normalizado (lowercase, sem acentos, sem pontuação, espaços colapsados)
  - [x] Itens duplicados são removidos no orquestrador antes da sumarização

- [x] **B-012** `[RF10, RF11]` — Sumarização consolidada (versão simples)
  - [x] Prompt em `src/genai/prompts.py` (system + user) sem alucinação ("apenas com base nas manchetes")
  - [x] `summarize(...)` em `src/genai/summarizer.py` produz `Summary` (Pydantic) — **sem campo `days`**
  - [x] Resumo, bullets extraídos e lista de `SourceRef` para o PDF (R1)
  - [x] Versão por cluster fica para o R2 (B-106)

- [x] **B-013** `[RT08, RF12]` — Geração de PDF (versão básica)
  - [x] PDF gerado em `output/<timestamp>_<tema>.pdf` (via `fpdf2` em `src/pdf/report.py`)
  - [x] Conteúdo: título, tema, resumo executivo, pontos-chave (bullets) e lista de fontes (com URL clicável)
  - [x] Sobrescrita controlada (param `overwrite`; quando `False` adiciona sufixo `_2`, `_3`, ...)

- [x] **B-014** `[RF15]` — Mensagem final ao usuário
  - [x] Caminho absoluto do PDF é exibido no terminal ao final (painel verde "Relatório final")

**Critério de release R1:** executar `python main.py`, escolher um
tema, e obter um PDF válido em `output/`, sem exceções não tratadas.

---

## Release 2 — Qualidade (robustez + GenAI avançada)

> **Objetivo**: elevar o nível do MVP — comportamento humanizado,
> deduplicação semântica, clustering, sumarização por grupo, robustez,
> testes e logs estruturados.

- [x] **B-101** `[RF05]` — Comportamento humanizado na navegação (adiantado em R1)
  - [x] Helper de scroll suave em `src/utils/humanize.py` (`smooth_scroll`)
  - [x] Delays randomizados entre `HUMANIZE_DELAY_MIN/MAX`
  - [x] Aplicado em **todos** os Page Objects via `BasePage.humanized_scroll()`

- [ ] **B-102** `[RF14, RNF12]` — Robustez ampliada na coleta
  - [ ] Retry leve (1 tentativa extra) por site quando a primeira falha
  - [ ] Snapshot do HTML/screenshot em `output/debug/` quando a coleta retorna 0 notícias

- [ ] **B-103** `[RT07, RF08]` — Deduplicação semântica via embeddings
  - [ ] Cliente de embeddings em `src/genai/embeddings.py`
  - [ ] Similaridade de cosseno acima de threshold configurável (`DEDUP_THRESHOLD`) marca duplicata
  - [ ] Logs informam quantas duplicatas foram removidas em cada camada

- [ ] **B-104** `[RF09]` — Agrupamento (clustering) das notícias
  - [ ] Algoritmo escolhido (KMeans / HDBSCAN / threshold de similaridade)
  - [ ] Cada cluster recebe um nome gerado pelo LLM
  - [ ] Notícias órfãs (sem cluster) ficam em uma seção "Outros"

- [ ] **B-105** `[RF10]` — Sumarização **por cluster**
  - [ ] Prompt dedicado por cluster (recebe títulos + snippets do grupo)
  - [ ] Resumo cita as fontes do próprio cluster
  - [ ] Substitui o resumo único do R1 (B-012 vira input do R2)

- [ ] **B-106** `[RF11]` — Resumo executivo final consolidado
  - [ ] Recebe os resumos de cada cluster como entrada
  - [ ] Retorna visão geral curta (3 a 5 parágrafos)

- [ ] **B-107** `[RF13]` — Logs de execução estruturados
  - [ ] Log de início/fim de cada etapa (validação, coleta, dedupe, cluster, resumo, PDF)
  - [ ] Contagens: notícias coletadas, deduplicadas, agrupadas

- [ ] **B-108** `[RT04, RNF11]` — Testes unitários (pytest)
  - [ ] Testes para utilitários de normalização, dedupe e parsing de datas
  - [ ] Testes da camada GenAI com mocks do LLM e embeddings
  - [ ] Cobertura mínima de **60%** (`pytest --cov`)

- [ ] **B-109** `[RT09]` — Padrão de código (opcional, recomendado)
  - [ ] `ruff` configurado em `pyproject.toml`
  - [ ] `ruff check .` sem erros
  - [ ] `type hints` em funções públicas

**Critério de release R2:** mesma execução do R1, agora com PDF
**agrupado** por temas, **sem duplicatas**, **com logs detalhados** e
**testes verdes**.

---

## Release 3 — Entrega Final (polimento + documentação)

> **Objetivo**: deixar o projeto pronto para apresentação acadêmica —
> PDF visualmente apresentável, documentação final completa, demo e
> revisão geral.

- [ ] **B-201** `[RF12]` — PDF apresentável
  - [ ] Capa com título, tema, data de geração e autor
  - [ ] Sumário (índice) clicável (quando suportado)
  - [ ] Seções por cluster com título, resumo e lista de fontes (com link)
  - [ ] Rodapé com numeração de páginas

- [ ] **B-202** `[RNF13]` — Atualização do `README.md`
  - [ ] Capturas de tela de execução
  - [ ] Trecho de exemplo de PDF gerado (link ou imagem)
  - [ ] Roadmap atualizado com R1/R2/R3 marcados como concluídos

- [ ] **B-203** `[RNF10]` — `PROMPTS.md` finalizado
  - [ ] Todos os prompts relevantes registrados
  - [ ] Backlog de prompts movido/zerado

- [ ] **B-204** `[RNF13]` — `docs/escopo_mvp.md` revisado
  - [ ] Atualização de eventuais decisões pendentes (LLM, embeddings, PDF)
  - [ ] Histórico de revisões atualizado

- [ ] **B-205** `[RT10]` — Revisão final do versionamento
  - [ ] Histórico de commits com Conventional Commits consistentes
  - [ ] Tag `v1.0.0` criada na entrega

- [ ] **B-206** — Demo / vídeo curto da execução *(opcional, recomendado)*
  - [ ] Gravação de tela de uma execução end-to-end
  - [ ] Link disponível no `README.md`

- [ ] **B-207** — Apresentação acadêmica
  - [ ] Slides ou roteiro de demonstração
  - [ ] Mapa do uso da GenAI (produto + ciclo de desenvolvimento)

**Critério de release R3:** projeto **versionado**, **documentado**,
**testado** e **demonstrável**, atendendo aos critérios de aceite do MVP
listados em [`escopo_mvp.md`](./escopo_mvp.md#9-critérios-de-aceite-do-mvp).

---

## Definition of Done (DoD)

Para qualquer item ser considerado **concluído (`[x]`)**, deve atender:

- [ ] Todos os **critérios de aceite** marcados.
- [ ] Código segue a **estrutura modular** (RT01) e **type hints**.
- [ ] **Sem credenciais** ou segredos no código.
- [ ] **Logs** das principais etapas presentes.
- [ ] **Commit** no padrão **Conventional Commits**.
- [ ] **Documentação** afetada (`README.md`, `PROMPTS.md`,
      `docs/escopo_mvp.md`, `docs/backlog.md`) **atualizada**.
- [ ] Quando aplicável: **testes** verdes (`pytest`).

---

## Histórico de revisões

| Versão | Data | Autor | Descrição |
|---|---|---|---|
| 0.1 | 2026-04-30 | Leonardo Santos | Versão inicial do backlog (R1, R2, R3). |
| 0.2 | 2026-04-30 | Leonardo Santos | Atualiza B-004 (menu de 10 temas + N dias) e B-006 (validação determinística no lugar do guardrail LLM). |
| 0.3 | 2026-04-30 | Leonardo Santos | Adiciona **RT11 (Pydantic v2)**; limita N a `1–10` em B-004; reforça B-006 com modelo Pydantic. |
| 0.4 | 2026-04-30 | Leonardo Santos | Refina **RT01** (POM com `locators/`, `pages/`, `steps/`, `models/`); troca **RT05** para `chromedriver-autoinstaller`; adiciona requisitos PEP8/docstrings em B-001 e Locators/Steps em B-007. |
| 0.5 | 2026-04-30 | Leonardo Santos | Marca **B-001, B-002, B-003, B-004 e B-006 como concluídos** (estrutura modular, config via `.env`, logger, menu CLI e validação Pydantic implementados e testados). |
| 0.6 | 2026-04-30 | Leonardo Santos | **Setup de testes do RT04 concluído** (`pyproject.toml`, `conftest.py`); **73 testes** cobrindo B-001..B-006 com **75% de cobertura** (acima do mínimo de 60% — RNF11). |
| 0.7 | 2026-04-30 | Leonardo Santos | **R1 quase completo**: marca **B-005, B-007, B-008, B-009, B-010, B-011, B-012** como concluídos. Adianta **B-101 (humanize)**, **B-102 (robustez)** e **B-103 (dedupe URL+título)** do R2. **160 testes / 61% cobertura**. Restam B-013 (PDF) e B-014 (mensagem final) do R1. |
| 0.8 | 2026-04-30 | Leonardo Santos | **Reescreve a estratégia de coleta**: substitui sites fixos (G1/BBC/Agência Brasil) por **discovery dinâmico via Google Search** + **coleta dia-a-dia por site**. Reescreve B-008/B-009/B-010/B-011. Remove pages/locators/testes fixos. Adiciona `dates.py`, `domains.py`, `google_locators.py`, `google_search_page.py`, `discovery_step.py`. **160 testes / 73% cobertura**. |
| 0.9 | 2026-04-30 | Leonardo Santos | **Opção E aplicada**: a estratégia `site:dominio + tbs=cdr:1` falhou em produção (zero resultados). Migra discovery e coleta para `news.google.com`, introduz `src/adapters/` (`SiteAdapter` Protocol + registry + `GenericNewsAdapter`) e aplica filtro de janela **localmente** sobre `published_at`. Remove `google_locators.py` e `google_search_page.py`. **B-008/B-009/B-010/B-011 reabertos e concluídos** com a nova estratégia. **179 testes / 74% cobertura**. |
| 1.0 | 2026-04-30 | Leonardo Santos | **Reset arquitetural**: a integração com Google (discovery + adapter via `news.google.com`) foi removida por instabilidade em produção. Volta para a **lista fixa de 4 sites de confiança** (G1, BBC News Brasil, Agência Brasil, R7) com Page Objects dedicados. **Remove o input de "número de dias"** — entrada única passa a ser o tema. RFs do escopo renumerados (RF01–RF15). B-004/B-006/B-008/B-009/B-010/B-012 reabertos com a nova descrição; **B-011 (dedupe URL+título)** mantido como já concluído. Itens removidos: `B-101 (humanize)` permanece concluído; o antigo B-102 (robustez parcial) e o antigo B-103 (dedupe URL+título) foram absorvidos por B-010 e B-011 respectivamente. |
| 1.1 | 2026-04-30 | Leonardo Santos | **Release 1 (Core) concluído**: marca como concluídos **B-004, B-006, B-008, B-009, B-010, B-012, B-013 e B-014**. Implementa `src/pdf/report.py` com `fpdf2` (capa textual, tema, metadados, resumo executivo, bullets, fontes com URL clicável), com filename `output/<timestamp>_<tema>.pdf` e sobrescrita controlada (`overwrite`). Orchestrator chama `generate_pdf` no fim do pipeline e exibe o caminho absoluto ao usuário. **164 testes / 79% cobertura** (módulo PDF: **100%**). |
