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
| **RT01** | Estrutura modular (`src/pages`, `src/services`, `src/genai`, `src/pdf`, `src/utils`, `tests`). |
| **RT02** | Carregamento de configuração via `.env` (`python-dotenv`) + `.env.example`. |
| **RT03** | Logging estruturado (níveis, timestamps, módulo de origem). |
| **RT04** | Setup de testes com `pytest` + `pytest-cov`. |
| **RT05** | Camada base do Selenium (driver factory, opções, `webdriver-manager`). |
| **RT06** | Cliente LLM **abstraído** por interface (permite trocar provedor). |
| **RT07** | Cliente de embeddings abstraído (similaridade semântica). |
| **RT08** | Integração com biblioteca de geração de PDF. |
| **RT09** | Tipagem (`type hints`) e linter (`ruff`) — opcional. |
| **RT10** | Conventional Commits e branch protection local. |

---

## Release 1 — Core (fluxo end-to-end mínimo)

> **Objetivo**: rodar o fluxo completo *happy path* — usuário informa tema
> e datas → RPA coleta em 3 sites → gera um PDF simples com sumarização
> básica. Sem deduplicação semântica, sem clustering, sem polimento.

- [ ] **B-001** `[RT01]` — Definir estrutura modular do projeto
  - [ ] Pastas `src/pages`, `src/services`, `src/genai`, `src/pdf`, `src/utils`, `tests` criadas
  - [ ] `__init__.py` em cada pacote
  - [ ] `main.py` passa a chamar o orquestrador em `src/services`

- [ ] **B-002** `[RT02]` — Carregamento de configuração via `.env`
  - [ ] `.env.example` versionado com chaves esperadas
  - [ ] Módulo `src/utils/config.py` lê e valida as variáveis
  - [ ] Falha amigável se variável obrigatória estiver ausente

- [ ] **B-003** `[RT03]` — Logging estruturado
  - [ ] Logger central em `src/utils/logger.py`
  - [ ] Níveis INFO/WARNING/ERROR habilitados
  - [ ] Timestamps em cada linha de log

- [ ] **B-004** `[RF01, RF02]` — CLI para captura de tema e intervalo
  - [ ] CLI aceita `--tema "<texto>"` e `--dias N` (ou `--de/--ate`)
  - [ ] Validação dos parâmetros (não vazio, intervalo válido)
  - [ ] Exibe os parâmetros recebidos antes de iniciar

- [ ] **B-005** `[RT06]` — Cliente LLM abstraído
  - [ ] Interface `LLMClient` em `src/genai/llm_client.py`
  - [ ] Pelo menos uma implementação concreta funcional
  - [ ] API key carregada do `.env`

- [ ] **B-006** `[RF03, RF04]` — Guardrail de validação de tema (versão simples)
  - [ ] Prompt classifica tema em `permitido` / `restrito`
  - [ ] Tema restrito: exibe mensagem amigável e encerra com código != 0
  - [ ] Tema permitido: prossegue para a coleta

- [ ] **B-007** `[RT05, RF05]` — Camada base do Selenium (driver factory)
  - [ ] `src/pages/base_page.py` com `BasePage`
  - [ ] Driver factory com `webdriver-manager`
  - [ ] Browser abre em modo **visível** (não-headless)

- [ ] **B-008** `[RF07]` — Page Object do **Site 1** (coleta básica)
  - [ ] PO específico com seletores isolados
  - [ ] Método `buscar(tema)` retorna lista de notícias (URL, título, data, snippet)
  - [ ] Filtragem por intervalo de datas aplicada
  - [ ] Limite máximo de notícias por site configurável

- [ ] **B-009** `[RF07]` — Page Object do **Site 2** (coleta básica)
  - [ ] Mesmos critérios de aceite do B-008

- [ ] **B-010** `[RF07]` — Page Object do **Site 3** (coleta básica)
  - [ ] Mesmos critérios de aceite do B-008

- [ ] **B-011** `[RF08]` — Filtro por intervalo de datas
  - [ ] Função utilitária centralizada para parsing de datas
  - [ ] Notícias fora do intervalo são descartadas

- [ ] **B-012** `[RF11, RF12]` — Sumarização consolidada (versão simples)
  - [ ] Prompt de sumarização recebe a lista bruta de notícias
  - [ ] Retorna um único bloco de resumo executivo
  - [ ] Mantém referência às fontes (URLs)

- [ ] **B-013** `[RT08, RF13]` — Geração de PDF (versão básica)
  - [ ] PDF gerado em `output/<timestamp>_<tema>.pdf`
  - [ ] Conteúdo: título, tema, intervalo, resumo executivo, lista de fontes
  - [ ] Sobrescrita controlada (não duplica em uma mesma execução)

- [ ] **B-014** `[RF16]` — Mensagem final ao usuário
  - [ ] Caminho absoluto do PDF é exibido no terminal ao final

**Critério de release R1:** executar `python main.py --tema "..." --dias 5` e
obter um PDF válido em `output/`, sem exceções não tratadas.

---

## Release 2 — Qualidade (robustez + GenAI avançada)

> **Objetivo**: elevar o nível do MVP — comportamento humanizado,
> deduplicação semântica, clustering, sumarização por grupo, robustez,
> testes e logs estruturados.

- [ ] **B-101** `[RF06]` — Comportamento humanizado na navegação
  - [ ] Helper de scroll suave em `src/utils/humanize.py`
  - [ ] Delays randomizados entre `HUMANIZE_DELAY_MIN/MAX`
  - [ ] Aplicado em **todos** os Page Objects

- [ ] **B-102** `[RF15, RNF12]` — Robustez na coleta
  - [ ] Timeouts explícitos em todas as ações Selenium
  - [ ] `try/except` por site: falha em um não interrompe os demais
  - [ ] Log de erro com nome do site e exceção

- [ ] **B-103** `[RF09]` — Deduplicação por URL e título
  - [ ] Normalização de URL (querystring, trailing slash)
  - [ ] Hash de título normalizado (lowercase, sem acentos, sem pontuação)
  - [ ] Itens duplicados são removidos antes da sumarização

- [ ] **B-104** `[RT07, RF09]` — Deduplicação semântica via embeddings
  - [ ] Cliente de embeddings em `src/genai/embeddings.py`
  - [ ] Similaridade de cosseno acima de threshold configurável (`DEDUP_THRESHOLD`) marca duplicata
  - [ ] Logs informam quantas duplicatas foram removidas em cada camada

- [ ] **B-105** `[RF10]` — Agrupamento (clustering) das notícias
  - [ ] Algoritmo escolhido (KMeans / HDBSCAN / threshold de similaridade)
  - [ ] Cada cluster recebe um nome gerado pelo LLM
  - [ ] Notícias órfãs (sem cluster) ficam em uma seção "Outros"

- [ ] **B-106** `[RF11]` — Sumarização **por cluster**
  - [ ] Prompt dedicado por cluster (recebe títulos + snippets do grupo)
  - [ ] Resumo cita as fontes do próprio cluster
  - [ ] Substitui o resumo único do R1 (B-012 vira input do R2)

- [ ] **B-107** `[RF12]` — Resumo executivo final consolidado
  - [ ] Recebe os resumos de cada cluster como entrada
  - [ ] Retorna visão geral curta (3 a 5 parágrafos)

- [ ] **B-108** `[RF14]` — Logs de execução estruturados
  - [ ] Log de início/fim de cada etapa (validação, coleta, dedupe, cluster, resumo, PDF)
  - [ ] Contagens: notícias coletadas, filtradas, deduplicadas, agrupadas

- [ ] **B-109** `[RT04, RNF11]` — Testes unitários (pytest)
  - [ ] Testes para utilitários de datas, normalização e dedupe
  - [ ] Testes da camada GenAI com mocks do LLM e embeddings
  - [ ] Cobertura mínima de **60%** (`pytest --cov`)

- [ ] **B-110** `[RT09]` — Padrão de código (opcional, recomendado)
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

- [ ] **B-201** `[RF13]` — PDF apresentável
  - [ ] Capa com título, tema, intervalo, data de geração e autor
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
listados em [`escopo_mvp.md`](./escopo_mvp.md#7-critérios-de-aceite-do-mvp).

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
