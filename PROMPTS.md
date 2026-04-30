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
- [9. Mudança no input do usuário — menu fixo de 10 temas](#9-mudança-no-input-do-usuário--menu-fixo-de-10-temas)
- [10. Limite de N (1–10 dias) e adoção de Pydantic v2](#10-limite-de-n-110-dias-e-adoção-de-pydantic-v2)
- [11. Briefing local para agentes (CURSOR_CONTEXT.md)](#11-briefing-local-para-agentes-cursor_contextmd)
- [12. Início da implementação — estrutura, config, logger, menu e validação](#12-início-da-implementação--estrutura-config-logger-menu-e-validação)
- [13. Suíte de testes (pytest) para os módulos de R1](#13-suíte-de-testes-pytest-para-os-módulos-de-r1)
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

## 9. Mudança no input do usuário — menu fixo de 10 temas

| Campo | Valor |
|---|---|
| **Data** | 2026-04-30 |
| **Etapa** | Refino de escopo / Design |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "Gostaria de alterar a parte da entrada do usuário. Para este MVP o
> RPA deve fornecer uma lista com os 10 assuntos de notícias mais
> buscados. Assim o usuário apenas irá escolher o tema e fornecer o
> número de dias que ele quer (ex.: últimas notícias dos 5 dias). Isso
> vai evitar entradas indesejadas. Lista de assuntos: Economia,
> Política, Esportes, Eventos globais, Saúde, Tecnologia,
> Entretenimento, Clima, Crimes/Segurança, Cotidiano. Faça a alteração
> desta parte no projeto e nos arquivos envolvidos."

### Saída / Realizado

**Decisão de design**: substituição do **input livre de tema + guardrail
LLM** por um **menu fixo de 10 temas** + **número de dias N**, com
**validação determinística**. A lista funciona como um *guardrail
determinístico* de input, eliminando a necessidade de chamada a LLM
nessa etapa.

**Arquivos atualizados:**

- `docs/escopo_mvp.md` (v0.2):
  - Nova seção **3. Temas suportados** com a tabela dos 10 temas.
  - Renumeração das demais seções (4 a 10 + sumário).
  - **RF01** reescrito (menu numerado de 10 temas).
  - **RF02** ajustado (número de dias N inteiro > 0).
  - **RF03** reescrito (validação determinística, sem LLM).
  - **RF04** reescrito (rejeição de input inválido + re-solicitação).
  - **Seção 6.1** (GenAI no produto): removido "Validação de tema
    (guardrail)"; adicionada nota sobre validação determinística.
  - **Critério de aceite** item 2 atualizado.
  - **Risco** "Tema ambíguo" reescrito como "Tema pré-definido amplo".
  - Item 16 adicionado em "Fora de escopo": tema livre.
  - Glossário de "Guardrail" complementado.

- `docs/backlog.md` (v0.2):
  - **B-004** reescrito: "CLI com menu de 10 temas + número de dias".
  - **B-006** reescrito: "Validação determinística de input
    (guardrail de menu)" — sem LLM.

- `docs/arquitetura.md` (v0.2):
  - **Diagrama de componentes**: nó `Theme Validator (Guardrail)`
    substituído por `Theme Menu + Validator (determinístico)`;
    aresta `VAL --> LLM` removida.
  - **Diagrama de fluxo de dados**: decisão `Guardrail LLM`
    substituída por `Validação determinística`; ramo de erro agora
    re-solicita a entrada (loop), em vez de encerrar.

- `README.md`:
  - Visão geral atualizada (menu fixo + N dias).
  - Bullet "Validação do tema (guardrail)" removido da lista de uso
    da GenAI no fluxo.
  - Seção **Funcionalidades > Entradas** lista os 10 temas e o
    número de dias.
  - Seção **Funcionalidades > Fluxo** atualizada.
  - **Diagrama ASCII** atualizado para refletir o menu determinístico.
  - Adicionada referência a `docs/arquitetura.md`.

- `PROMPTS.md` *(este registro)*.

### Artefatos
- `RPA_SMART_NEWS/docs/escopo_mvp.md` *(v0.2)*
- `RPA_SMART_NEWS/docs/backlog.md` *(v0.2)*
- `RPA_SMART_NEWS/docs/arquitetura.md` *(v0.2)*
- `RPA_SMART_NEWS/README.md` *(atualizado)*
- `RPA_SMART_NEWS/PROMPTS.md` *(atualizado)*

---

## 10. Limite de N (1–10 dias) e adoção de Pydantic v2

| Campo | Valor |
|---|---|
| **Data** | 2026-04-30 |
| **Etapa** | Refino de escopo / Decisão técnica |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "Preciso limitar também o número de dias. No máximo notícias dos
> últimos 10 dias. Nesta primeira versão, ficará limitado para não
> trazer muitas informações e prejudicar a performance.
> Como informação, vamos usar o Pydantic v2, com código limpo e
> docstrings curtas, caso seja necessário."

### Saída / Realizado

**Decisões aplicadas:**
1. **Limite de dias**: `1 ≤ N ≤ 10` para evitar volume excessivo de
   notícias e preservar a performance do MVP.
2. **Validação via Pydantic v2** — modelo `UserInput` (e demais
   modelos de configuração) usarão Pydantic v2 com validadores nativos.
3. **Convenção de código**: código limpo, type hints e **docstrings
   curtas e objetivas** (sem ruído narrativo).

**Arquivos atualizados:**

- `requirements.txt`: adicionada dependência `pydantic>=2.7.0` em uma
  nova seção *"Validação de inputs / modelos de dados"*.

- `docs/escopo_mvp.md` (v0.3):
  - Seção 3 (Temas suportados): nota explícita do limite de 10 dias.
  - **RF02** atualizado para `1 ≤ N ≤ 10`.
  - **RF03** menciona uso de **modelos Pydantic v2**.
  - **RF04** atualizado para "fora do intervalo `1–10`".
  - **RNF17** reforçado (código limpo + docstrings curtas).
  - Novo **RNF19**: Pydantic v2 como tecnologia de validação.
  - Critério de aceite #2 ajustado para o intervalo `1–10`.

- `docs/backlog.md` (v0.3):
  - Novo **RT11**: modelos Pydantic v2 para inputs e configuração.
  - **B-004** referencia `RT11` e fixa `1 ≤ N ≤ 10`.
  - **B-006** referencia `RT11` e detalha o modelo `UserInput`
    (`tema_id: int`, `dias: int`) com mapeamento de
    `ValidationError` → mensagem amigável.

- `docs/arquitetura.md` (v0.3):
  - Componentes: label do nó passou a `Theme Menu + Validator
    (Pydantic v2 — 10 temas + 1–10 dias)`.
  - Fluxo de dados: nó de validação passou a `Validação (Pydantic v2)`
    e o rótulo da aresta de input passou a `seleção 1–10 + N (1–10)`.

- `README.md`:
  - **Funcionalidades > Entradas**: limite `1 ≤ N ≤ 10` documentado
    com nota sobre a restrição desta versão.
  - **Stack tecnológica**: linha de **Pydantic v2** adicionada.
  - Nota de **convenção de código** (limpo, type hints, docstrings
    curtas) incluída logo abaixo da tabela de stack.

- `PROMPTS.md` *(este registro)*.

### Artefatos
- `RPA_SMART_NEWS/requirements.txt` *(atualizado)*
- `RPA_SMART_NEWS/docs/escopo_mvp.md` *(v0.3)*
- `RPA_SMART_NEWS/docs/backlog.md` *(v0.3)*
- `RPA_SMART_NEWS/docs/arquitetura.md` *(v0.3)*
- `RPA_SMART_NEWS/README.md` *(atualizado)*
- `RPA_SMART_NEWS/PROMPTS.md` *(atualizado)*

---

## 11. Briefing local para agentes (CURSOR_CONTEXT.md)

| Campo | Valor |
|---|---|
| **Data** | 2026-04-30 |
| **Etapa** | Setup / Produtividade |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "Crie um arquivo para o cursor conseguir obter o contexto de todo o
> projeto, caso seja necessário abrir um novo chat zerado com outro
> agente. Este arquivo deve ser atualizado no decorrer do projeto.
> Ele deve ser adicionado no `.gitignore`."

### Saída / Realizado
- Criação de **`CURSOR_CONTEXT.md`** na raiz do projeto, com 13
  seções cobrindo:
  - Como o agente deve usar o arquivo (instruções de bootstrap em
    chat novo).
  - Papel do agente (especialista no curso UFG / módulo).
  - Identidade do projeto (nome, curso, módulo, idioma, autor git).
  - Objetivo do produto e lista canônica dos 10 temas.
  - Stack decidida e a decidir.
  - Convenções (código, git, documentação, PowerShell).
  - Estrutura atual e planejada do projeto.
  - Decisões-chave já tomadas.
  - Estado atual (roadmap + histórico de commits + fase).
  - Mapa de referências dos arquivos-chave.
  - Próximas decisões pendentes (LLM, embeddings, PDF, sites,
    estratégia de busca, clustering).
  - Perfil de interação esperado pelo usuário.
  - Histórico de atualizações do próprio arquivo.
- Atualização do **`.gitignore`**: adicionada entrada
  `CURSOR_CONTEXT.md` na seção *Cursor*. Validado com
  `git check-ignore -v` que o arquivo está sendo ignorado.
- Atualização do `PROMPTS.md` com este registro.

### Artefatos
- `RPA_SMART_NEWS/CURSOR_CONTEXT.md` *(não versionado)*
- `RPA_SMART_NEWS/.gitignore` *(atualizado)*
- `RPA_SMART_NEWS/PROMPTS.md` *(atualizado)*

---

## 12. Início da implementação — estrutura, config, logger, menu e validação

| Campo | Valor |
|---|---|
| **Data** | 2026-04-30 |
| **Etapa** | Implementação (R1, primeira iteração) |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "Agora vamos iniciar o desenvolvimento seguindo os arquivos
> `backlog.md` e `escopo_mvp.md`. No Python, vamos utilizar o PEP8,
> docstring para documentação e tratamento de erros. No POM, vamos
> utilizar uma estrutura de pastas dentro de uma pasta `src/`. Podemos
> ter uma `BasePage`, pastas como: Locators, Pages, Steps. Utilizar o
> `chromedriver-autoinstaller`. Modifique o arquivo `backlog.md` antes,
> caso seja necessário. Nesta primeira etapa, vamos estruturar tudo,
> organizar e construir até a parte que obtem a entrada do usuário.
> Antes de abrir o navegador."

### Saída / Realizado

#### Decisões aplicadas
1. **Estrutura POM**: `src/locators/`, `src/pages/` (com `BasePage`),
   `src/steps/`, `src/services/`, `src/models/`, `src/utils/`,
   `src/genai/`, `src/pdf/` + `tests/` na raiz.
2. **Driver**: `chromedriver-autoinstaller` no lugar de
   `webdriver-manager`.
3. **Validação**: `pydantic-settings` para config + `pydantic` para
   `UserInput` e `Topic` (IntEnum).
4. **Convenções**: PEP8, type hints, docstrings curtas, tratamento
   de erros explícito (`MenuAbortedError`, `ValidationError`).

#### Backlog atualizado (v0.5)
- **RT01** detalhado com a nova estrutura.
- **RT05** trocado para `chromedriver-autoinstaller`.
- **B-001** atualizado com PEP8 + docstrings.
- **B-007** atualizado com Locators/Steps + `chromedriver-autoinstaller`.
- **B-001, B-002, B-003, B-004, B-006** marcados como **concluídos**.

#### Documentos atualizados
- `docs/backlog.md` (v0.4 → v0.5): RT01/RT05/B-001/B-007 + checklist
  de B-001..B-006 marcado.
- `docs/escopo_mvp.md` (v0.4): RNF04 troca para
  `chromedriver-autoinstaller`.
- `docs/arquitetura.md` (v0.4): nó `Driver Factory` atualizado.
- `README.md`: stack tecnológica + estrutura planejada atualizadas.
- `CURSOR_CONTEXT.md` (v0.2): stack, estrutura, fase atual.

#### Dependências
- **Removida**: `webdriver-manager`.
- **Adicionadas**: `chromedriver-autoinstaller>=0.6.4` e
  `pydantic-settings>=2.2.0`.

#### Código implementado
| Arquivo | Responsabilidade |
|---|---|
| `src/__init__.py` | Pacote raiz com `__version__`. |
| `src/locators/__init__.py` | Placeholder (seletores por site). |
| `src/pages/__init__.py` | Placeholder (Page Objects). |
| `src/pages/base_page.py` | `BasePage` placeholder (será expandida em B-007). |
| `src/steps/__init__.py` | Placeholder (fluxos de alto nível). |
| `src/services/__init__.py` | Placeholder. |
| `src/services/menu.py` | `display_topics()`, `collect_user_input()`, `MenuAbortedError`, formatação amigável de `ValidationError`. |
| `src/services/orchestrator.py` | `run()` com banner, menu, coleta, confirmação e exit codes. |
| `src/models/__init__.py` | Placeholder. |
| `src/models/topics.py` | `Topic` (IntEnum 1–10) e `TOPIC_LABELS` em pt-BR. |
| `src/models/user_input.py` | `UserInput` (Pydantic v2 frozen, `topic: Topic`, `days: int 1–10`). |
| `src/utils/__init__.py` | Placeholder. |
| `src/utils/config.py` | `Settings` (Pydantic Settings v2) + `get_settings()` cacheado. |
| `src/utils/logger.py` | `setup_logger()` e `get_logger()` com `RichHandler`. |
| `src/genai/__init__.py` | Placeholder. |
| `src/pdf/__init__.py` | Placeholder. |
| `tests/__init__.py` | Placeholder da suíte. |
| `main.py` | Entrypoint enxuto que delega para `orchestrator.run()`. |
| `.env.example` | Variáveis: `LOG_LEVEL`, `MAX_DAYS`, `MAX_RETRIES`, `OUTPUT_DIR`. |

#### Validação (smoke tests)
| Cenário | Exit code | Resultado |
|---|---|---|
| Input válido (`3`, `5`) | `0` | OK — confirma "Esportes / 5 dia(s)". |
| 2 inputs inválidos seguidos de válido | `0` | OK — exibe contagem de tentativas restantes. |
| 3 inputs inválidos consecutivos | `1` | OK — `MenuAbortedError` tratado. |

### Artefatos
- `RPA_SMART_NEWS/src/**` *(estrutura modular completa)*
- `RPA_SMART_NEWS/tests/__init__.py`
- `RPA_SMART_NEWS/main.py` *(reescrito)*
- `RPA_SMART_NEWS/.env.example`
- `RPA_SMART_NEWS/requirements.txt` *(atualizado)*
- `RPA_SMART_NEWS/docs/backlog.md` *(v0.5)*
- `RPA_SMART_NEWS/docs/escopo_mvp.md` *(v0.4)*
- `RPA_SMART_NEWS/docs/arquitetura.md` *(v0.4)*
- `RPA_SMART_NEWS/README.md` *(stack + estrutura atualizadas)*
- `RPA_SMART_NEWS/CURSOR_CONTEXT.md` *(v0.2)*
- `RPA_SMART_NEWS/PROMPTS.md` *(este registro)*

---

## 13. Suíte de testes (pytest) para os módulos de R1

| Campo | Valor |
|---|---|
| **Data** | 2026-04-30 |
| **Etapa** | Implementação / Qualidade (R1) |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "Utilizando o pytest, precisamos realizar os testes do que foi
> implementado até agora. Crie os arquivos de teste na pasta `tests/`.
> Depois de criar os arquivos de testes, atualize os arquivos de
> documentação, mostrando como executar os testes. Logo após, rode os
> testes."

### Saída / Realizado

#### Configuração de testes
- Criado **`pyproject.toml`** com:
  - `[tool.pytest.ini_options]` — `pythonpath = ["."]`,
    `testpaths = ["tests"]`, `addopts = ["-ra", "--strict-markers", "--strict-config"]`.
  - `[tool.coverage.run]` — `source = ["src"]`, `branch = true`,
    `omit = ["*/__init__.py"]`.
  - `[tool.coverage.report]` — `show_missing = true`, exclusões para
    `if __name__`, `pragma: no cover` e `raise NotImplementedError`.
- Criado **`tests/conftest.py`** com fixtures:
  - `_reset_logger` (autouse): zera handlers entre testes.
  - `mock_inputs`: monkeypatch de `console.input` do menu.
  - `clear_settings_cache`: limpa o `lru_cache` de `get_settings`.

#### Arquivos de teste criados (`tests/`)
| Arquivo | Cobertura |
|---|---|
| `test_topics.py` | `Topic` enum, `TOPIC_LABELS`, `label_for()` |
| `test_user_input.py` | Validação Pydantic v2 (válido, fora do range, frozen) |
| `test_config.py` | `Settings` (defaults, `max_days`/`max_retries` validação, singleton) |
| `test_logger.py` | `setup_logger` (níveis, case-insensitive), `get_logger` |
| `test_menu.py` | `_parse_int`, `_format_validation_error`, `display_topics`, `collect_user_input` (happy path, retries, abort) |
| `test_base_page.py` | Placeholder de `BasePage` (init com/sem driver) |

#### Resultado da execução
```
collected 73 items
73 passed in 1.20s

TOTAL coverage: 75% (limite RNF11: 60%)
```

| Módulo | Cobertura |
|---|---:|
| `src/models/topics.py` | 100% |
| `src/models/user_input.py` | 100% |
| `src/pages/base_page.py` | 100% |
| `src/services/menu.py` | 95% |
| `src/utils/config.py` | 100% |
| `src/utils/logger.py` | 100% |
| `src/services/orchestrator.py` | 0% _(glue UI — coberto nas próximas iterações)_ |

#### Documentação atualizada
- **`README.md`** — seção `Testes` reescrita com:
  - Comandos para suíte completa, cobertura (`--cov`, `--cov-report=html`)
    e filtros (`-k`, por arquivo, por classe).
  - Tabela do estado atual (73 testes, 75% cobertura) e por módulo.
- **`docs/backlog.md`** (v0.6) — histórico atualizado registrando que
  o **setup de testes (RT04) está concluído** e que B-001..B-006
  estão cobertos por testes.
- **`CURSOR_CONTEXT.md`** (v0.3) — fase atual + commits + nota sobre
  cobertura.

### Artefatos
- `RPA_SMART_NEWS/pyproject.toml`
- `RPA_SMART_NEWS/tests/conftest.py`
- `RPA_SMART_NEWS/tests/test_topics.py`
- `RPA_SMART_NEWS/tests/test_user_input.py`
- `RPA_SMART_NEWS/tests/test_config.py`
- `RPA_SMART_NEWS/tests/test_logger.py`
- `RPA_SMART_NEWS/tests/test_menu.py`
- `RPA_SMART_NEWS/tests/test_base_page.py`
- `RPA_SMART_NEWS/README.md` *(atualizado)*
- `RPA_SMART_NEWS/docs/backlog.md` *(v0.6)*
- `RPA_SMART_NEWS/CURSOR_CONTEXT.md` *(v0.3)*
- `RPA_SMART_NEWS/PROMPTS.md` *(este registro)*

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

_Última atualização: 2026-04-30 (suíte de testes — 73 testes / 75% cobertura)_
