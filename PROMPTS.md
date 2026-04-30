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
- [14. Implementação do navegador até a sumarização (POM + LLM stub)](#14-implementação-do-navegador-até-a-sumarização-pom--llm-stub)
- [15. Discovery dinâmico via Google + coleta dia-a-dia](#15-discovery-dinâmico-via-google--coleta-dia-a-dia)
- [16. Reset arquitetural — remove Google e o input de "número de dias"](#16-reset-arquitetural--remove-google-e-o-input-de-número-de-dias)
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

## 14. Implementação do navegador até a sumarização (POM + LLM stub)

| Campo | Valor |
|---|---|
| **Data** | 2026-04-30 |
| **Etapa** | Implementação (R1, segunda iteração) |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "Agora chegou a parte mais importante do projeto. Você vai implementar
> o código desde a abertura do navegador, até a parte antes da geração
> do pdf. Lembre de utilizar o POM, com Locators, Pages e Steps. Para
> buscar as notícias, busque somente de sites confiáveis, mais
> populares. Evite sites que bloqueiam scraping e pedem senhas."

### Saída / Realizado

#### Decisões aplicadas
1. **3 sites finais (RF07)**: G1, BBC News Brasil, Agência Brasil —
   sem paywall, sem login obrigatório, com editorias por tema.
2. **Estratégia de busca**: navegação direta para a editoria/seção
   correspondente ao tema (mais robusta que busca interna, evita
   captcha/rate-limit).
3. **Cliente LLM abstraído** (`Protocol`) com:
   - `StubLLMClient` (default, offline, determinístico — funciona sem
     API key, ideal para CI e dev).
   - `OpenAILLMClient` opcional, com **lazy import** do pacote
     `openai` (não vira dependência obrigatória).
   - `factory.get_llm_client()` resolve o provider via `LLM_PROVIDER`.
4. **Sem novas dependências**: parsing de datas próprio (ISO + pt-BR
   longo + `dd/mm/aaaa` + relativo).
5. **Tolerância a falhas por site** no `coleta_step`: exceção em um
   site não interrompe os outros (atende RF15 + B-102).

#### Backlog atualizado (v0.7)
- **B-005, B-007, B-008, B-009, B-010, B-011, B-012** marcados como
  concluídos.
- **B-101, B-102, B-103** do R2 marcados como adiantados (parcial).

#### Documentos atualizados
- `docs/escopo_mvp.md` (v0.5): RF07 fixa os 3 sites finais.
- `docs/backlog.md` (v0.7): itens R1 e R2 (parciais) marcados.
- `README.md`: stack, fluxo, sites, configuração, estrutura, testes
  e roadmap atualizados.
- `CURSOR_CONTEXT.md` (v0.4): nova estrutura, decisões e estado atual.
- `.env.example`: novas variáveis (HEADLESS, delays, MAX_NEWS_PER_SITE,
  SELENIUM_TIMEOUT, LLM_PROVIDER, LLM_MODEL, LLM_API_KEY,
  LLM_TEMPERATURE, LLM_MAX_TOKENS, USER_AGENT).

#### Código implementado

| Arquivo | Responsabilidade |
|---|---|
| `src/utils/config.py` | Novas settings: headless, delays, max_news, selenium_timeout, llm_*. |
| `src/utils/driver_factory.py` | `create_driver()` / `quit_driver()` com `chromedriver-autoinstaller`. |
| `src/utils/humanize.py` | `random_delay`, `smooth_scroll`, `scroll_to_top`. |
| `src/utils/date_filter.py` | `parse_date` (ISO/pt-BR/relativo) + `filter_recent`. |
| `src/utils/dedupe.py` | `normalize_url` + `normalize_title` + `dedupe`. |
| `src/pages/base_page.py` | `BasePage` real: waits, finds, scroll humanizado, click tolerante. |
| `src/locators/g1_locators.py` | Mapeamento Topic → editoria + seletores. |
| `src/locators/bbc_locators.py` | Idem (com fallback para a home em temas sem seção). |
| `src/locators/agencia_brasil_locators.py` | Idem. |
| `src/pages/g1_page.py` | `G1Page.collect(topic, max_items) -> list[NewsArticle]`. |
| `src/pages/bbc_page.py` | `BBCPage.collect(...)`. |
| `src/pages/agencia_brasil_page.py` | `AgenciaBrasilPage.collect(...)`. |
| `src/steps/coleta_step.py` | `coletar_noticias(driver, topic)` orquestra os 3 sites. |
| `src/models/news.py` | `NewsArticle` Pydantic v2 frozen. |
| `src/models/summary.py` | `Summary` + `SourceRef` Pydantic v2 frozen. |
| `src/genai/llm_client.py` | `Protocol LLMClient` (interface mínima). |
| `src/genai/factory.py` | `get_llm_client()` resolve provider via `.env`. |
| `src/genai/llm_clients/stub.py` | `StubLLMClient` offline determinístico. |
| `src/genai/llm_clients/openai_client.py` | Adapter OpenAI com lazy import. |
| `src/genai/prompts.py` | `SUMMARY_SYSTEM_PROMPT` + `build_summary_prompt`. |
| `src/genai/summarizer.py` | `summarize(...) -> Summary`. |
| `src/services/orchestrator.py` | Pipeline: input → driver → coleta → filtro → dedupe → sumarização → exibição (sem PDF). |

#### Suíte de testes
- **160 testes** passando (era 73).
- **Cobertura: 61%** (acima do mínimo RNF11 = 60%).
- Novos testes: `test_news`, `test_summary`, `test_humanize`,
  `test_date_filter`, `test_dedupe`, `test_llm_clients`,
  `test_summarizer`, `test_locators`, `test_coleta_step`.
- `test_base_page` reescrito para a `BasePage` real (driver mock).

### Artefatos
- `src/utils/{config,driver_factory,humanize,date_filter,dedupe}.py`
- `src/pages/{base_page,g1_page,bbc_page,agencia_brasil_page}.py`
- `src/locators/{g1,bbc,agencia_brasil}_locators.py`
- `src/steps/coleta_step.py`
- `src/models/{news,summary}.py`
- `src/genai/{llm_client,factory,prompts,summarizer}.py`
- `src/genai/llm_clients/{stub,openai_client}.py`
- `src/services/orchestrator.py` *(reescrito)*
- `tests/test_{base_page,news,summary,humanize,date_filter,dedupe,llm_clients,summarizer,locators,coleta_step}.py`
- `.env.example` *(atualizado)*
- `docs/escopo_mvp.md` *(v0.5)*
- `docs/backlog.md` *(v0.7)*
- `README.md` *(atualizado)*
- `CURSOR_CONTEXT.md` *(v0.4)*
- `PROMPTS.md` *(este registro)*

---

## 15. Discovery dinâmico via Google + coleta dia-a-dia

| Campo | Valor |
|---|---|
| **Data** | 2026-04-30 |
| **Etapa** | Refino de design / Reescrita arquitetural (R1) |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "Você deve pesquisar o tema no google primeiro. Após isso, você vai
> encontrar os sites mais confiáveis de notícia. Com relação aos dias,
> você deve procurar de acordo com as datas em cada site. Se o usuário
> passar o número = 2, você deve acessar o primeiro site procurando
> sobre o tema na data de hoje, depois na data de ontem e depois na
> data antes de ontem. Assim por diante. Só depois você passa para o
> outro site. Não precisa ser sites fixos. Mas os mais confiáveis de
> acordo com o tema da notícia."

### Saída / Realizado

#### Decisões aplicadas

1. **Discovery dinâmico via Google**: substitui a lista fixa
   (G1/BBC/Agência Brasil) por uma seleção via Google Search aba
   "Notícias". A lista de sites varia por tema.
2. **Coleta dia-a-dia**: para cada site descoberto, varre os últimos
   N dias **um a um** (`hoje`, `ontem`, `anteontem`, ...). Usa
   `site:dominio` + `tbs=cdr:1,cd_min:DD/MM/YYYY,cd_max:DD/MM/YYYY`.
3. **Sem whitelist de sites**: confiamos no ranking do Google. Apenas
   um *blacklist* leve descarta domínios não-jornalísticos (Wikipedia,
   YouTube, redes sociais, lojas, buscadores).
4. **Semântica de N**: `N=k → últimos k dias incluindo hoje` (N=1 →
   só hoje; N=2 → hoje + ontem; N=3 → hoje + ontem + anteontem).
5. **Detecção de captcha**: o `GoogleSearchPage` detecta o bloqueio
   (`form#captcha-form`, `div#sorry`, etc.) — discovery falho devolve
   lista vazia e o orquestrador aborta com mensagem amigável; coletas
   bloqueadas em pares `(site, dia)` são puladas com log.
6. **Limpeza**: removidos `g1_locators`, `bbc_locators`,
   `agencia_brasil_locators`, e respectivas `*_page.py` e o
   `tests/test_locators.py`.

#### Backlog atualizado (v0.8)
- **B-008** reescrito: discovery via Google.
- **B-009** reescrito: coleta dia-a-dia por site.
- **B-010** reescrito: tolerância a falhas + detecção de captcha.
- **B-011** ajustado: filtro de datas vira utilitário (Google já
  filtra na origem).

#### Documentos atualizados
- `docs/escopo_mvp.md` (v0.6): RF07/RF08 reescritos.
- `docs/backlog.md` (v0.8): itens R1 reescritos.
- `README.md`: fluxo, estrutura, configuração, testes e roadmap
  refletindo a nova arquitetura.
- `CURSOR_CONTEXT.md` (v0.5): pipeline, decisões, estrutura.
- `.env.example`: novas variáveis (`DISCOVERY_MAX_SOURCES`,
  `DISCOVERY_RESULTS_TO_SCAN`, `GOOGLE_LOCALE`, `GOOGLE_COUNTRY`).

#### Código implementado / removido

**Removido**:
- `src/locators/{g1,bbc,agencia_brasil}_locators.py`
- `src/pages/{g1,bbc,agencia_brasil}_page.py`
- `tests/test_locators.py`

**Criado / atualizado**:

| Arquivo | Responsabilidade |
|---|---|
| `src/utils/dates.py` | `today_local`, `iter_recent_dates(N)`, `format_brazilian_date`. |
| `src/utils/domains.py` | `extract_domain`, `root_domain`, `is_news_domain`, `rank_domains`, blacklist. |
| `src/utils/config.py` | Novas settings `discovery_max_sources`, `discovery_results_to_scan`, `google_locale`, `google_country`. |
| `src/locators/google_locators.py` | Seletores fallback + `discovery_url` + `site_day_url` + `CAPTCHA_INDICATORS`. |
| `src/pages/google_search_page.py` | `discover_top_sources` + `search_in_site_for_day` + `_is_blocked`. |
| `src/steps/discovery_step.py` | `descobrir_fontes(driver, topic) -> list[str]`. |
| `src/steps/coleta_step.py` | Reescrito: itera `(site × dia)` com tolerância a falhas. |
| `src/services/orchestrator.py` | Pipeline: input → discovery → coleta dia-a-dia → dedupe → sumarização. |

**Novos testes**:
- `tests/test_dates.py`, `tests/test_domains.py`,
  `tests/test_google_locators.py`, `tests/test_google_search_page.py`,
  `tests/test_discovery_step.py` e `tests/test_coleta_step.py`
  reescrito.

#### Suíte de testes
- **160 testes** passando.
- **Cobertura: 73%** (subiu de 61% — pages fixas removidas tinham
  cobertura baixa).

#### Risco conhecido
O **Google é hostil a scraping** e pode mostrar captcha rapidamente
em execuções com muitos pares `(site × dia)`. Mitigações já
implementadas:
- delays randomizados entre ações (`HUMANIZE_DELAY_MIN/MAX`),
- user-agent realista,
- detecção do captcha → log warning + skip + aborto controlado.

Em uma execução real, recomenda-se manter `MAX_DAYS` baixo nos
primeiros testes (e.g. 1–3) para validar o fluxo antes de subir o
volume de requests.

### Artefatos
- `src/utils/{dates,domains}.py`
- `src/locators/google_locators.py`
- `src/pages/google_search_page.py`
- `src/steps/{discovery,coleta}_step.py`
- `src/services/orchestrator.py` *(reescrito)*
- `src/utils/config.py` *(novas settings)*
- `.env.example` *(atualizado)*
- `tests/test_{dates,domains,google_locators,google_search_page,discovery_step,coleta_step}.py`
- `docs/escopo_mvp.md` *(v0.6)*
- `docs/backlog.md` *(v0.8)*
- `README.md` *(atualizado)*
- `CURSOR_CONTEXT.md` *(v0.5)*
- `PROMPTS.md` *(este registro)*

---

## 16. Opção E — Site Adapters via `news.google.com`

| Campo | Valor |
|---|---|
| **Data** | 2026-04-30 |
| **Etapa** | Refatoração arquitetural (R1) |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "A última parte implementada não funcionou. Nenhuma pesquisa
> funcionou, a abordagem não deu certo. Erro: A pesquisa não
> corresponde ao resultado de busca. (...) Apenas conserte. Use o
> arquivo backlog.md e escopo_mvp.md, você estava implementando desde
> a abertura do navegador, até antes da criação do arquivo pdf."

### Diagnóstico
A estratégia anterior (`§15`) usava `q=<tema> site:<dominio>` +
`tbs=cdr:1,cd_min:DD/MM/YYYY,cd_max:DD/MM/YYYY` no Google Web. A
tripla restrição (tema ∧ site ∧ janela de 1 dia) é estatisticamente
esparsa no índice e retornava "Sua pesquisa não corresponde a nenhum
documento" para a maioria dos pares `(site × dia)`. Pipeline ficava
com lista vazia desde a coleta.

### Decisões aplicadas (Opção E)

1. **Discovery via `news.google.com`** (1 query única por execução)
   substitui o `tbm=nws` do Google Web.
2. **Coleta via `SiteAdapter`** (Protocol) + `Adapter Registry`. No
   R1 só há o `GenericNewsAdapter`, que consulta o Google News com
   `site:<dominio>` (sem `tbs`).
3. **Janela de N dias aplicada localmente** sobre `published_at`
   (extraído do `<time datetime="...">` de cada card). A UX
   "site → hoje → ontem → anteontem" é preservada nos logs via
   agregação local.
4. **Resolver de redirect** (`./articles/<token>` → URL canônica) via
   nova aba do Selenium, controlado por `RESOLVE_ARTICLE_URLS`.
5. **Falha tolerante**: `AdapterError` é capturada pelo
   `coleta_step` — falha em um adapter não interrompe os demais.

### Código implementado / removido

**Removido**:
- `src/locators/google_locators.py`
- `src/pages/google_search_page.py`
- `tests/test_google_locators.py`
- `tests/test_google_search_page.py`

**Criado**:
| Arquivo | Responsabilidade |
|---|---|
| `src/locators/google_news_locators.py` | URLs (`discovery_url`, `site_search_url`) + locators (cards, links, `<time>`, captcha, consentimento). |
| `src/pages/google_news_page.py` | `GoogleNewsPage.discover_top_sources` + `search_in_site` + resolver de redirect. |
| `src/adapters/__init__.py` | Re-exports do contrato. |
| `src/adapters/base.py` | `SiteAdapter` (Protocol) + `AdapterError`. |
| `src/adapters/registry.py` | `get_adapter`, `register_adapter`, `clear_registry`. |
| `src/adapters/generic.py` | `GenericNewsAdapter` (R1). |
| `tests/test_google_news_locators.py` | URLs sem `tbs`, com `site:`, encoding correto. |
| `tests/test_google_news_page.py` | Discovery e coleta com `WebDriver` mockado. |
| `tests/test_adapters.py` | Contrato, registry, filtragem por janela, max_items, erro propagado. |

**Atualizado**:
| Arquivo | Mudança |
|---|---|
| `src/utils/config.py` | +`google_news_base_url`, +`google_news_ceid`, +`generic_adapter_results_to_scan`, +`resolve_article_urls`. |
| `src/steps/discovery_step.py` | Usa `GoogleNewsPage`. |
| `src/steps/coleta_step.py` | Delega ao `get_adapter(domain)` e loga quebra dia-a-dia local. |
| `tests/test_coleta_step.py` | Reescrito mockando o registry. |
| `tests/test_discovery_step.py` | Apontado para `GoogleNewsPage`. |
| `.env.example` | Novas vars + remoção implícita do `tbs`. |

### Documentos atualizados
- `docs/escopo_mvp.md` (v0.7): RF07/RF08 reescritos para Site Adapters.
- `docs/backlog.md` (v0.9): B-008..B-011 reabertos e marcados como
  concluídos com nova descrição.
- `docs/arquitetura.md` (v0.5): diagramas trocam `Site 1/2/3` por
  `GoogleNewsPage` + `Adapter Registry` + `GenericNewsAdapter` +
  (futuros) curados; fluxo de dados passa a ter "Filtro local por
  últimos N dias (published_at)".
- `README.md`: fluxo, estrutura, tabela de env vars, roadmap, cobertura.
- `CURSOR_CONTEXT.md` (v0.6): §14 finalmente escrita; estrutura,
  decisões D1..D7, fase atual.
- `PROMPTS.md`: este registro.

### Suíte de testes
- **179 testes** passando (de 160).
- **Cobertura: 74%** (de 73%).
- `google_news_page.py` em 62% — restante são caminhos do resolver de
  redirect que dependem de Selenium real (mesmo padrão do
  `base_page.py` em 81%).

### Risco conhecido
O `news.google.com` é mais tolerante a scraping que o Google Web, mas
o layout é gerado por hashes do `c-wiz` que podem mudar. Mitigações
implementadas:
- locators **resilientes** (atributos semânticos: `<article>`, `<time>`,
  `a[href^='./articles/']`) com múltiplos fallbacks.
- detecção de captcha → log warning + skip + aborto controlado no
  discovery.
- delays/scroll humanizados.

### Artefatos
- `src/locators/google_news_locators.py`
- `src/pages/google_news_page.py`
- `src/adapters/{__init__,base,registry,generic}.py`
- `src/steps/{discovery,coleta}_step.py` *(atualizados)*
- `src/utils/config.py` *(novas settings)*
- `.env.example` *(atualizado)*
- `tests/test_{adapters,coleta_step,discovery_step,google_news_locators,google_news_page}.py`
- `docs/{backlog,escopo_mvp,arquitetura}.md` *(atualizados)*
- `README.md` *(atualizado)*
- `CURSOR_CONTEXT.md` *(v0.6 — §14 escrita)*
- `PROMPTS.md` *(este registro)*

---

## 17. Hotfix do discovery — consent + estratégia por publishers

| Campo | Valor |
|---|---|
| **Data** | 2026-04-30 |
| **Etapa** | Hotfix do discovery (R1) |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "Erro: Discovery falhou: o Google não retornou fontes (provável
> bloqueio/captcha). Tente novamente em alguns minutos."

### Diagnóstico
A primeira execução real do `main.py` após a Opção E falhou no
discovery, retornando lista vazia. Duas causas confirmadas:

1. **Consent page do Google.** Em perfil novo do Chrome (sem cookies),
   `news.google.com` redireciona para `consent.google.com/m?...`.
   Os seletores de consent originais cobriam variantes de
   `accounts.google.com` mas **não casavam com o consent.google.com
   moderno** (botão `tHlp8d`, `<form action="/save">`, etc.).
   Resultado: a página fica travada na consent → zero cards → zero
   domínios.
2. **`_resolve_url` chamado em todos os ~20 cards do discovery.**
   Cada chamada abre/fecha aba. Se popup blocker do Chrome ativar
   ou redirect demorar, o domínio resolve para `news.google.com`,
   que é filtrado pela blacklist de `domains.py` → lista vazia.

### Correções aplicadas

1. **`_handle_consent` robusto** em `GoogleNewsPage`:
   - Detecta consent page por URL (`consent.google.com`) **e** por
     forma `<form action*='/save'>`, `<form action*='consent.google'>`,
     `<div role='dialog'> form>`.
   - Tenta múltiplos seletores: `button.tHlp8d`, `button[jsname='b3VHJd']`,
     `button[aria-label*='Aceitar']`, `button[aria-label*='Accept']`,
     XPath `//button[normalize-space()='Aceitar tudo']`, etc.
   - Faz até 3 tentativas e aguarda redirect saindo de
     `consent.google.com`.

2. **Discovery por publishers** (em vez de por hrefs):
   - `discover_top_sources` agora agrupa cards pelo nome do publisher
     (`<div data-n-tid>`, `<div.vr1PYe>`, etc.) e ranqueia por
     frequência.
   - Para cada um dos top K publishers, resolve **um único** redirect
     para descobrir o domínio canônico.
   - Custo: ~3 redirects (em vez de ~20) → 7× mais rápido e mais
     resiliente a falhas de popup.

3. **Logs detalhados** em cada etapa:
   - `URL apos consent`, `nº cards encontrados`, `nº publishers únicos`,
     `top publishers (por frequencia)`, `dominios selecionados`.
   - Falhas no `_resolve_url` agora vão pro log em DEBUG com motivo.

4. **Mensagem de erro útil** no orchestrator:
   - Lista as 4 causas mais prováveis (consent, captcha, layout,
     redirect) e direciona o usuário aos logs.

### Arquivos alterados
- `src/locators/google_news_locators.py` — `+CONSENT_PAGE_INDICATORS`,
  `CONSENT_LOCATORS` ampliado (12 fallbacks com CSS + XPath).
- `src/pages/google_news_page.py` — `+_handle_consent`,
  `+_is_consent_page`, `+_wait_for_url_change`,
  `+_resolve_publisher_domain`, `+_extract_external_href`. Discovery
  reescrito (estratégia por publishers).
- `src/services/orchestrator.py` — mensagem de discovery falho mais
  útil.
- `tests/test_google_news_page.py` — `+test_retorna_vazio_quando_consent_nao_resolve`,
  `test_extrai_dominios_dos_cards_via_publishers` (substitui o
  anterior), `+test_dedupa_dominios_de_publishers_diferentes_mesmo_dominio`.

### Suíte de testes
- **181 testes** passando (de 179).
- Cobertura mantida.

### Como validar manualmente
```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

Esperado nos logs:
```
INFO Abrindo URL: https://news.google.com/search?q=...
INFO Consent page detectada (tentativa 1): https://consent.google.com/m?continue=...
INFO Discovery: URL apos consent = https://news.google.com/search?q=...
INFO Discovery: 20 cards encontrados
INFO Discovery: 8 publishers unicos: ['g1', 'cnn brasil', ...]
INFO Discovery: top publishers (por frequencia) = ['g1', 'cnn brasil', 'uol']
INFO Discovery: dominios selecionados = ['globo.com', 'cnnbrasil.com.br', 'uol.com.br']
```

### Artefatos
- `src/locators/google_news_locators.py`
- `src/pages/google_news_page.py`
- `src/services/orchestrator.py`
- `tests/test_google_news_page.py`
- `PROMPTS.md` *(este registro)*

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

## 16. Reset arquitetural — remove Google e o input de "número de dias"

| Campo | Valor |
|---|---|
| **Data** | 2026-04-30 |
| **Etapa** | Refino / Refatoração |
| **Modelo/Ferramenta** | Cursor (Claude Opus 4.7) |

### Prompt
> "Certo, a implementação usando o google não funcionou. Vamos fazer
> uma mudança grande no projeto. Voltando no escopo_mvp.md e
> backlog.md, vamos remover a segunda entrada do usuário que trata
> dos dias. A única escolha do usuário será o tema da notícia. As
> noticia serão aquelas que forem encontradas no site de busca.
> Remova isso de todos os arquivos relacionados. Após isso, vamos
> voltar a implementação inicial. Após abrir o navegador, as
> principais notícias de acordo com o tema escolhido, serão
> pesquisadas nos sites de confiaça, que não bloqueiam scrapping e
> nem pedem senhas. Remova os relacionamentos com o google. Remova a
> pasta output e src/adapters."

### Confirmações coletadas (via menu)
- **Sites confiáveis**: G1, BBC News Brasil, Agência Brasil, R7.
- **Estratégia de coleta por site**: editoria → busca interna como
  fallback (instrução textual: "Se não encontrar registros direto na
  editoria, usar a busca interna do site").
- **Limite por site**: manter `MAX_NEWS_PER_SITE` (default `15`) no
  `.env`.
- **Datas**: extrair `published_at` quando possível e usar para
  ordenar (mais recentes primeiro).
- **Utils de datas**: manter só o mínimo útil (`parse_date`).

### Saída / Realizado

#### Documentação
- `docs/escopo_mvp.md` reescrito (v0.8): RFs renumerados (RF01–RF15),
  removidos todos os "N dias", nova seção §4 (lista fixa das 4 fontes),
  RNFs/RFs ajustados, "Fora de escopo" agora lista filtro por janela e
  discovery via Google explicitamente.
- `docs/backlog.md` reescrito (v1.0): RT01 atualizado (BaseNewsPage +
  POs por site); B-004/B-006/B-008/B-009/B-010/B-012 reabertos com a
  nova descrição; B-011 (dedupe URL+título) mantido concluído.
- `docs/arquitetura.md` reescrito (v0.6): nó `Google News`, `Adapter
  Registry` e `GenericNewsAdapter` removidos; substituídos por
  `BaseNewsPage` + 4 nós de Page Object (`G1Page`, `BBCBrasilPage`,
  `AgenciaBrasilPage`, `R7Page`); fluxo de dados sem "número de dias".
- `README.md` reescrito: nova seção "Fontes de notícias", roadmap
  atualizado (B-006/B-008/B-009/B-010/B-012 como pendentes na nova
  estrutura).
- `.env.example` enxugado (remove `GOOGLE_*`, `DISCOVERY_*`,
  `GENERIC_ADAPTER_*`, `RESOLVE_ARTICLE_URLS`, `MAX_DAYS`).

#### Código removido
- `src/adapters/` (pasta inteira: `base.py`, `registry.py`,
  `generic.py`, `__init__.py`).
- `src/pages/google_news_page.py`.
- `src/locators/google_news_locators.py`.
- `src/steps/discovery_step.py`.
- `src/utils/debug_dump.py` (debug dump específico do Google News).
- `src/utils/dates.py` (`iter_recent_dates`, `today_local`,
  `format_brazilian_date` — todos atrelados à janela de N dias).
- `src/utils/domains.py` (`extract_domain`, `root_domain`,
  `is_news_domain`, `rank_domains` — usados apenas pelo discovery).
- `output/` (pasta inteira).
- Testes correspondentes:
  `test_google_news_page.py`, `test_google_news_locators.py`,
  `test_discovery_step.py`, `test_adapters.py`, `test_dates.py`,
  `test_domains.py`, e o antigo `test_coleta_step.py`.

#### Código novo
- `src/pages/base_news_page.py` (`BaseNewsPage`): fluxo
  editoria → busca interna; helpers `_extract_article`,
  `_extract_href`, `_extract_datetime`, `_first_text`, `_absolutize`.
- `src/locators/g1_locators.py` + `src/pages/g1_page.py`
  (`G1Page`, editorias para 8 dos 10 temas).
- `src/locators/bbc_brasil_locators.py` + `src/pages/bbc_brasil_page.py`
  (`BBCBrasilPage`, sempre via busca interna).
- `src/locators/agencia_brasil_locators.py` +
  `src/pages/agencia_brasil_page.py` (`AgenciaBrasilPage`, editorias
  para 8 temas).
- `src/locators/r7_locators.py` + `src/pages/r7_page.py`
  (`R7Page`, editorias para 8 temas).
- `tests/test_base_news_page.py` (15 testes do fluxo
  editoria/busca/extração).
- `tests/test_news_pages.py` (testes de contrato dos 4 Page Objects).
- `tests/test_coleta_step.py` (reescrito: factories injetáveis,
  ordenação por data, tolerância a falhas).

#### Código atualizado
- `src/utils/config.py`: removidos `max_days`,
  `discovery_max_sources`, `discovery_results_to_scan`,
  `generic_adapter_results_to_scan`, `google_news_base_url`,
  `google_locale`, `google_country`, `google_news_ceid`,
  `resolve_article_urls`. Mantém `max_news_per_site`, `selenium_*`,
  `humanize_*`, `llm_*`.
- `src/utils/date_filter.py`: mantém apenas `parse_date`
  (`within_last_days`/`filter_recent` removidas).
- `src/models/user_input.py`: campo `days` removido.
- `src/models/summary.py`: campo `days` removido.
- `src/services/menu.py`: `collect_user_input` agora pede só o tema.
- `src/services/orchestrator.py`: pipeline reescrito sem
  discovery/janela; agora chama `coletar_noticias` direto nas 4
  fontes fixas.
- `src/steps/coleta_step.py`: itera nas 4 `BaseNewsPage`, ordena por
  `published_at` desc, tolera falhas.
- `src/genai/prompts.py` e `src/genai/summarizer.py`: assinatura sem
  `days`.
- Testes ajustados: `test_user_input.py`, `test_menu.py`,
  `test_config.py`, `test_summary.py`, `test_summarizer.py`,
  `test_date_filter.py`.

### Resultado
- **146 testes passando** (de 181 que existiam antes do reset — a
  diferença é a remoção dos testes do código deletado).
- **78% de cobertura** (acima do mínimo de 60% — RNF11).
- Pipeline atual: input do tema → driver → `G1Page`/`BBCBrasilPage`/
  `AgenciaBrasilPage`/`R7Page` (cada qual com fluxo editoria → busca
  interna) → ordenação por `published_at` → dedupe URL+título →
  sumarização (Stub LLM ou OpenAI).
- Próximos itens R1: `B-013` (PDF) e `B-014` (mensagem final).

### Artefatos
- `docs/escopo_mvp.md`, `docs/backlog.md`, `docs/arquitetura.md`,
  `README.md`, `.env.example`.
- `src/pages/base_news_page.py`, `src/pages/{g1,bbc_brasil,agencia_brasil,r7}_page.py`.
- `src/locators/{g1,bbc_brasil,agencia_brasil,r7}_locators.py`.
- `src/utils/config.py`, `src/utils/date_filter.py`.
- `src/models/user_input.py`, `src/models/summary.py`.
- `src/services/menu.py`, `src/services/orchestrator.py`.
- `src/steps/coleta_step.py`.
- `src/genai/prompts.py`, `src/genai/summarizer.py`.
- `tests/test_user_input.py`, `tests/test_menu.py`,
  `tests/test_config.py`, `tests/test_summary.py`,
  `tests/test_summarizer.py`, `tests/test_date_filter.py`,
  `tests/test_base_news_page.py`, `tests/test_news_pages.py`,
  `tests/test_coleta_step.py`.
- `CURSOR_CONTEXT.md`, `PROMPTS.md` *(este registro)*.

---

_Última atualização: 2026-04-30 (Reset arquitetural: remove Google + janela de N dias; volta para POs dedicados em G1, BBC News Brasil, Agência Brasil e R7. 146 testes / 78% cobertura)._
