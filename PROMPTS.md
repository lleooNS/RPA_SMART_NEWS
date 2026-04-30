# PROMPTS.md - RPA_SMART_NEWS

> Arquivo de **rastreabilidade** dos principais prompts utilizados na
> construção do projeto **RPA_SMART_NEWS**, mini-projeto do módulo
> *Laboratório Introdutório: Construindo um Mini-projeto com Inteligência
> Artificial Generativa* — Pós-graduação em Engenharia de Software:
> Automação e Inovação com IA Generativa (UFG).
>
> Cada entrada contém: **prompt enviado**, **objetivo**, **o que foi
> realizado** e **artefatos gerados**. O arquivo deve ser atualizado a
> cada nova interação relevante com a IA.

---

## Sumário

- [Convenções](#convenções)
- [0. Contexto inicial do projeto](#0-contexto-inicial-do-projeto)
- [1. Definição da ideia / escopo do MVP](#1-definição-da-ideia--escopo-do-mvp)
- [2. Bootstrap do projeto](#2-bootstrap-do-projeto)
- [3. Inicialização do repositório git](#3-inicialização-do-repositório-git)
- [4. Criação do README.md](#4-criação-do-readmemd)
- [5. Commit inicial](#5-commit-inicial)
- [6. Documento de escopo do MVP](#6-documento-de-escopo-do-mvp)
- [7. Backlog do projeto (R1/R2/R3)](#7-backlog-do-projeto-r1r2r3)
- [8. Diagramas de arquitetura (Mermaid)](#8-diagramas-de-arquitetura-mermaid)
- [Backlog de prompts (planejado)](#backlog-de-prompts-planejado)

---

## Convenções

- **Data**: data da interação (formato `YYYY-MM-DD`).
- **Etapa**: fase do ciclo de desenvolvimento (Concepção, Setup, Design,
  Implementação, Teste, Documentação, Refino).
- **Prompt**: resumo fiel do prompt enviado à IA.
- **Saída/Realizado**: resumo do que a IA produziu e foi efetivamente
  aceito/aplicado no projeto.
- **Artefatos**: arquivos criados ou modificados.

---

## 0. Contexto inicial do projeto

| Campo | Valor |
|---|---|
| **Data** | 2026-04-29 |
| **Etapa** | Concepção |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "Se torne um especialista no curso de pós-graduação da UFG: Engenharia
> de Software: Automação e Inovação com Inteligência Artificial
> Generativa. Seu objetivo é me auxiliar no módulo Laboratório
> Introdutório: Construindo um Mini-projeto com Inteligência Artificial
> Generativa."

### Saída / Realizado
- Definição do papel da IA como especialista no módulo.
- Listagem das frentes de apoio: planejamento, escolha de tecnologias,
  arquitetura, prompt engineering, implementação, avaliação, entrega.

### Artefatos
- _(nenhum — apenas alinhamento de contexto)_

---

## 1. Definição da ideia / escopo do MVP

| Campo | Valor |
|---|---|
| **Data** | 2026-04-29 |
| **Etapa** | Concepção |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "O objetivo é construir um MVP que permita explorar e aplicar as
> capacidades da GenAI em diferentes estágios do ciclo de vida do
> desenvolvimento de software. Ideia: um RPA em Python (Selenium + POM)
> que abre o navegador (visível, com scroll humanizado), pesquisa
> notícias de um tema informado pelo usuário em 3 sites confiáveis,
> dentro de um intervalo de datas, remove duplicatas, agrupa assuntos
> semelhantes, gera um resumo consolidado e salva em PDF. Se o tema for
> restrito, o RPA pede outro tema."

### Saída / Realizado
- Captura do escopo do MVP **RPA_SMART_NEWS**.
- Identificação de pontos de aplicação da GenAI: validação de tema,
  classificação de relevância, deduplicação semântica, agrupamento por
  similaridade, sumarização consolidada.
- Levantamento de decisões pendentes: provedor de LLM, sites-alvo,
  estratégia de busca, biblioteca de PDF, critérios de duplicata.

### Artefatos
- _(nenhum — definição de escopo)_

---

## 2. Bootstrap do projeto

| Campo | Valor |
|---|---|
| **Data** | 2026-04-29 |
| **Etapa** | Setup |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "Vamos iniciar o projeto. Chamei ele de RPA_SMART_NEWS. Crie o
> `PROMPTS.md` para rastreabilidade dos prompts (atualizável durante o
> projeto), o `.gitignore` para Python (incluindo `.venv` e cache de
> testes), o ambiente virtual `.venv`, o `requirements.txt` e o
> `main.py`."

### Saída / Realizado
- Criação da estrutura inicial do projeto na pasta `RPA_SMART_NEWS/`.
- `.gitignore` cobrindo: bytecode Python, `.venv`, caches de
  testes/lint/type-checkers, secrets, logs do Selenium, saídas do RPA
  (PDFs, screenshots), artefatos de IDE.
- `requirements.txt` com dependências base (Selenium, webdriver-manager,
  python-dotenv, rich, pytest) e placeholders comentados para LLM,
  embeddings e PDF (a serem definidos).
- `main.py` como entrypoint, com docstring descrevendo o objetivo do
  RPA.
- Ambiente virtual `.venv` criado e dependências instaladas.

### Artefatos
- `RPA_SMART_NEWS/.gitignore`
- `RPA_SMART_NEWS/requirements.txt`
- `RPA_SMART_NEWS/main.py`
- `RPA_SMART_NEWS/PROMPTS.md`
- `RPA_SMART_NEWS/.venv/` *(ambiente virtual — não versionado)*

---

## 3. Inicialização do repositório git

| Campo | Valor |
|---|---|
| **Data** | 2026-04-30 |
| **Etapa** | Setup |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "Este projeto ainda não está versionado, inicie o git."

### Saída / Realizado
- Inicialização do repositório git em `RPA_SMART_NEWS/` com branch
  padrão `main` (`git init -b main`).
- Validação do `.gitignore`: a pasta `.venv/` e demais artefatos
  ignorados **não aparecem** como untracked.
- Arquivos prontos para o primeiro commit: `.gitignore`, `PROMPTS.md`,
  `main.py`, `requirements.txt`.

### Artefatos
- `RPA_SMART_NEWS/.git/` *(repositório local — não versionado)*

---

## 4. Criação do README.md

| Campo | Valor |
|---|---|
| **Data** | 2026-04-30 |
| **Etapa** | Documentação |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "Crie o arquivo README.md para este projeto. Markdown simples,
> direto e profissional, forneça o README completo. Este arquivo deve
> ser atualizado no decorrer do projeto."

### Saída / Realizado
- Criação do `README.md` completo, em português, cobrindo:
  - Visão geral e contexto acadêmico (UFG).
  - Funcionalidades (entradas, fluxo, saídas).
  - Diagrama em alto nível da arquitetura (ASCII).
  - Stack tecnológica (com itens "a definir" sinalizados).
  - Estrutura atual e estrutura planejada do projeto.
  - Pré-requisitos, instalação (Windows/Linux/macOS), configuração
    (`.env` preliminar) e execução.
  - Estratégia de testes (pytest + pytest-cov).
  - Roadmap com checklist (itens de bootstrap já marcados).
  - Link para o `PROMPTS.md` (rastreabilidade).
  - Convenções de commit (Conventional Commits).
- Atualização do `PROMPTS.md` com este registro.

### Artefatos
- `RPA_SMART_NEWS/README.md`
- `RPA_SMART_NEWS/PROMPTS.md` *(atualizado)*

---

## 5. Commit inicial

| Campo | Valor |
|---|---|
| **Data** | 2026-04-30 |
| **Etapa** | Setup |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "Gere uma mensagem de commit no padrão Conventional Commits. Apenas
> uma linha de commit. Realize o commit inicial. Depois mostre o git
> history para que eu possa verificar se a mensagem foi commitada
> corretamente."

### Saída / Realizado
- Commit inicial realizado com a mensagem
  `chore: bootstrap inicial do projeto RPA_SMART_NEWS`.
- Hash do commit: `0b3e226` (root-commit, branch `main`).
- 5 arquivos versionados: `.gitignore`, `PROMPTS.md`, `README.md`,
  `main.py`, `requirements.txt` (717 inserções).
- `.venv/` corretamente ignorado pelo `.gitignore`.

### Artefatos
- Commit `0b3e226` no repositório local.

---

## 6. Documento de escopo do MVP

| Campo | Valor |
|---|---|
| **Data** | 2026-04-30 |
| **Etapa** | Concepção / Documentação |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "Crie um arquivo `docs/escopo_mvp.md` com o escopo do projeto,
> trazendo o objetivo, requisitos funcionais, não funcionais e fora de
> escopo. Linguagem técnica, direta, em Markdown. Forneça o conteúdo
> completo. Este arquivo também deve ser atualizado no decorrer do
> projeto."

### Saída / Realizado
- Criação da pasta `docs/` e do arquivo `docs/escopo_mvp.md`.
- Conteúdo estruturado em 9 seções: objetivo, personas/premissas,
  16 RFs, 18 RNFs, aplicação da GenAI no ciclo de desenvolvimento,
  15 itens fora de escopo, critérios de aceite, riscos e mitigações,
  glossário e histórico de revisões.
- Atualização do `PROMPTS.md` com este registro.

### Artefatos
- `RPA_SMART_NEWS/docs/escopo_mvp.md`
- `RPA_SMART_NEWS/PROMPTS.md` *(atualizado)*

---

## 7. Backlog do projeto (R1/R2/R3)

| Campo | Valor |
|---|---|
| **Data** | 2026-04-30 |
| **Etapa** | Planejamento |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "Crie o arquivo `docs/backlog.md`, utilize Checklist Markdown. O
> produto será entregue em 3 releases: core, qualidade e entrega final.
> Crie backlog mínimo com IDs RF/RT e critérios de aceite."

### Saída / Realizado
- Criação de `docs/backlog.md` em formato checklist Markdown.
- Definição de **10 Requisitos Técnicos (RT01–RT10)** complementares
  aos RFs do escopo.
- Estruturação em **3 releases**:
  - **R1 — Core**: 14 itens (`B-001` a `B-014`) cobrindo o fluxo
    end-to-end mínimo (estrutura modular, CLI, validação de tema, POs
    dos 3 sites, sumarização básica, PDF inicial).
  - **R2 — Qualidade**: 10 itens (`B-101` a `B-110`) cobrindo
    humanização, robustez, deduplicação semântica, clustering,
    sumarização por cluster, logs e testes (cobertura ≥60%).
  - **R3 — Entrega Final**: 7 itens (`B-201` a `B-207`) cobrindo
    polimento do PDF, atualização da documentação, tag de release,
    demo e apresentação acadêmica.
- Cada item traz **referências** aos `RF##` (escopo) e/ou `RT##`,
  além de **critérios de aceite aninhados** como sub-checklist.
- Definição de **DoD (Definition of Done)** unificada.
- Atualização do `PROMPTS.md` com este registro.

### Artefatos
- `RPA_SMART_NEWS/docs/backlog.md`
- `RPA_SMART_NEWS/PROMPTS.md` *(atualizado)*

---

## 8. Diagramas de arquitetura (Mermaid)

| Campo | Valor |
|---|---|
| **Data** | 2026-04-30 |
| **Etapa** | Design / Arquitetura |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "Crie o arquivo bloco Mermaid, simples, legível e versionável. Gere
> diagrama Mermaid de componentes e fluxo de dados."

### Saída / Realizado
- Criação de `docs/arquitetura.md` em Markdown com **dois diagramas
  Mermaid**:
  - **Diagrama de componentes** (`flowchart TB`): visão estática
    com 5 camadas agrupadas por `subgraph` — CLI/Bootstrap,
    Serviços/Orquestração, Automação Web (POM), GenAI e Saída.
  - **Diagrama de fluxo de dados** (`flowchart LR`): pipeline
    completo do input do usuário até a entrega do PDF, incluindo o
    desvio do guardrail para temas restritos.
- Inclusão de **legenda** explicando as notações Mermaid usadas.
- Histórico de revisões interno.
- Atualização do `PROMPTS.md` com este registro.

### Artefatos
- `RPA_SMART_NEWS/docs/arquitetura.md`
- `RPA_SMART_NEWS/PROMPTS.md` *(atualizado)*

---

## Backlog de prompts (planejado)

> Lista de prompts previstos para as próximas etapas. Será movida para
> as seções numeradas conforme cada interação for executada.

- [ ] **Arquitetura / POM** — Definir a estrutura de pastas (services,
  pages, genai, pdf, utils, tests) e diagrama do fluxo do RPA.
- [ ] **Validação de tema** — Prompt do guardrail para o LLM classificar
  se o tema é restrito/sensível.
- [ ] **Page Objects** — Geração inicial dos POs para cada um dos 3
  sites de notícias selecionados.
- [ ] **Coleta humanizada** — Helpers de scroll/espera/movimento do
  mouse para simular comportamento humano.
- [ ] **Deduplicação semântica** — Estratégia (URL + hash de título +
  similaridade de embeddings) e prompt de apoio.
- [ ] **Agrupamento (clustering)** — Algoritmo (KMeans, HDBSCAN,
  threshold por similaridade) + prompt para nomear os clusters.
- [ ] **Sumarização consolidada** — Prompt de sumarização por cluster e
  do resumo executivo final.
- [ ] **Geração do PDF** — Layout (capa, sumário executivo, seções por
  cluster, fontes/links).
- [ ] **Testes** — Estratégia de testes unitários (pytest) para
  utilitários e mocks do LLM/Selenium.
- [ ] **Documentação final** — Atualização do `README.md` com demo,
  capturas e instruções finais.

---

_Última atualização: 2026-04-30 (diagramas de arquitetura)_
