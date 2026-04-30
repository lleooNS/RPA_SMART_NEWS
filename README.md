# RPA_SMART_NEWS

> RPA em Python para coleta, deduplicação, agrupamento e sumarização
> inteligente de notícias usando **IA Generativa**, com exportação em
> PDF.

Projeto desenvolvido no módulo **Laboratório Introdutório: Construindo
um Mini-projeto com Inteligência Artificial Generativa** da
pós-graduação em **Engenharia de Software: Automação e Inovação com
Inteligência Artificial Generativa** — **UFG**.

---

## Sumário

- [Visão geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Fontes de notícias](#fontes-de-notícias)
- [Arquitetura](#arquitetura)
- [Stack tecnológica](#stack-tecnológica)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Como executar](#como-executar)
- [Testes](#testes)
- [Roadmap](#roadmap)
- [Rastreabilidade dos prompts](#rastreabilidade-dos-prompts)
- [Convenções de commit](#convenções-de-commit)
- [Autor](#autor)

---

## Visão geral

O **RPA_SMART_NEWS** é um robô (RPA) que automatiza a pesquisa de
notícias sobre um **tema escolhido pelo usuário a partir de uma lista
fixa de 10 assuntos**, executando o navegador de forma **visível**
(simulando um humano, com scroll e esperas naturais). A coleta é feita
em uma **lista fixa de 4 sites de confiança** (que não bloqueiam
scraping nem exigem login). Ao final, entrega um **PDF** com um resumo
consolidado, agrupado por assuntos semelhantes e livre de duplicatas.

A IA Generativa é aplicada em **múltiplos estágios** do fluxo:

- **Classificação de relevância** das notícias coletadas frente ao
  tema escolhido.
- **Deduplicação semântica** (além de URL/título).
- **Agrupamento de assuntos** semelhantes (clustering).
- **Sumarização consolidada** por cluster e do resumo executivo final.

> A **validação do input** é **determinística** (menu fixo de 10
> temas), funcionando como um *guardrail* simples e previsível, sem
> custo de chamada a LLM.

O projeto também explora o uso de GenAI em diferentes etapas do **ciclo
de vida do desenvolvimento de software**: concepção, codificação
assistida, geração de testes, documentação e refino — toda essa
trajetória é registrada em [`PROMPTS.md`](./PROMPTS.md).

---

## Funcionalidades

### Entrada do usuário
- **Tema** selecionado de uma **lista fixa de 10 assuntos** (1–10):
  Economia, Política, Esportes, Eventos globais, Saúde, Tecnologia,
  Entretenimento, Clima, Crimes/Segurança, Cotidiano.

> O MVP **não pede mais um intervalo de dias**. A coleta devolve as
> notícias mais recentes que cada site exibir para o tema escolhido.

### Fluxo
1. Exibição do **menu de 10 temas** + leitura da escolha do usuário.
2. **Validação determinística** do input (re-solicita em caso de
   entrada inválida).
3. Abertura visível do navegador (modo não-headless por default).
4. **Coleta nas 4 fontes fixas** (G1, BBC News Brasil, Agência Brasil
   e R7). Cada Page Object tenta primeiro a **editoria correspondente
   ao tema** e cai para a **busca interna** do site se a editoria não
   estiver mapeada ou retornar zero resultados.
5. Scroll e esperas humanizadas para simular um usuário real.
6. Deduplicação por URL canônica + título normalizado (camada
   semântica fica para o R2).
7. Sumarização consolidada via LLM (provedor abstraído; default `stub`
   offline; suporte opcional ao OpenAI).
8. Agrupamento de notícias por similaridade temática *(R2)*.
9. **Exportação em PDF** (`output/<timestamp>_<tema>.pdf`) com tema,
   metadados, resumo executivo, pontos-chave e lista de fontes com URL
   clicável.
10. Exibição do **caminho absoluto do PDF** no terminal ao final.

### Saídas
- Arquivo **PDF** com o relatório final.
- Logs de execução.

---

## Fontes de notícias

A lista de fontes é **fixa** no MVP, escolhida por:
- não exigir **login** ou **paywall** na listagem das matérias;
- ser razoavelmente **tolerante a scraping** (sem bloqueios agressivos
  por anti-bot);
- ter boa **cobertura editorial** dos 10 temas em pt-BR.

| Site | Domínio raiz | Estratégia |
|---|---|---|
| **G1** | `g1.globo.com` | Editoria (`/economia/`, `/politica/`, etc.) → busca interna |
| **BBC News Brasil** | `bbc.com/portuguese` | Busca interna |
| **Agência Brasil** | `agenciabrasil.ebc.com.br` | Editoria → busca interna |
| **R7** | `r7.com` | Editoria → busca interna |

Cada fonte tem seu **Page Object dedicado** em `src/pages/<site>_page.py`
e seus locators em `src/locators/<site>_locators.py`.

---

## Arquitetura

> Diagrama em alto nível do fluxo do RPA. Será detalhado conforme o
> projeto evolui.

```text
┌─────────────┐   ┌──────────────┐   ┌─────────────────┐   ┌──────────────┐
│   Usuário   │──▶│  Menu fixo   │──▶│  Coleta nas 4   │──▶│   Pipeline   │
│ (escolha o  │   │  (10 temas)  │   │  fontes fixas   │   │  GenAI       │
│  tema)      │   │ + validação  │   │  (Selenium +    │   │  (dedupe,    │
│             │   │ determinís-  │   │   POM por site) │   │   cluster,   │
│             │   │ tica         │   │                 │   │   resumo)    │
└─────────────┘   └──────────────┘   └─────────────────┘   └──────┬───────┘
                                                                  │
                                                                  ▼
                                                          ┌───────────────┐
                                                          │  Geração PDF  │
                                                          │   (output/)   │
                                                          └───────────────┘
```

> Para diagramas detalhados (componentes e fluxo de dados em
> Mermaid), ver [`docs/arquitetura.md`](./docs/arquitetura.md).

A automação web segue o padrão **Page Object Model (POM)**, com uma
`BasePage` reaproveitável, uma `BaseNewsPage` que implementa a
estratégia "editoria primeiro, busca interna como fallback", e Page
Objects específicos para cada um dos 4 sites de notícias.

---

## Stack tecnológica

| Camada | Tecnologia |
|---|---|
| Linguagem | Python **3.11+** |
| Automação Web | Selenium 4 + `chromedriver-autoinstaller` |
| Padrão de design (web) | Page Object Model (POM) com `locators/` + `pages/` + `steps/` |
| Validação de inputs / modelos | **Pydantic v2** + `pydantic-settings` |
| IA Generativa (LLM) | Interface `LLMClient` + `StubLLMClient` (default, offline) + `OpenAILLMClient` opcional |
| Embeddings / Similaridade | _A definir no R2_ (sentence-transformers / API) |
| Geração de PDF | **`fpdf2`** (`src/pdf/report.py` — capa textual, tema, resumo, bullets, fontes com URL clicável) |
| Configuração | `pydantic-settings` + `.env` |
| CLI / Logs | rich |
| Testes | pytest + pytest-cov |

> Convenção de código: **código limpo**, type hints e **docstrings
> curtas e objetivas** (sem ruído).

> Itens marcados como _a definir_ estão como **placeholders comentados**
> em `requirements.txt` e serão fixados conforme as decisões do
> projeto avançam.

---

## Estrutura do projeto

> A estrutura abaixo representa o estado atual e será expandida
> conforme novas etapas (PDF, embeddings, clustering) forem
> implementadas.

```text
RPA_SMART_NEWS/
├── src/
│   ├── locators/                    # Seletores CSS por site
│   │   ├── g1_locators.py
│   │   ├── bbc_brasil_locators.py
│   │   ├── agencia_brasil_locators.py
│   │   └── r7_locators.py
│   ├── pages/                       # Page Objects (POM)
│   │   ├── base_page.py             # waits, find helpers, scroll humanizado
│   │   ├── base_news_page.py        # fluxo editoria → busca interna
│   │   ├── g1_page.py
│   │   ├── bbc_brasil_page.py
│   │   ├── agencia_brasil_page.py
│   │   └── r7_page.py
│   ├── steps/                       # Fluxos de alto nível
│   │   └── coleta_step.py           # itera sobre os 4 Page Objects
│   ├── services/                    # CLI + orquestração
│   │   ├── menu.py
│   │   └── orchestrator.py
│   ├── models/                      # Modelos Pydantic v2
│   │   ├── topics.py
│   │   ├── user_input.py
│   │   ├── news.py
│   │   └── summary.py
│   ├── utils/                       # config, logger, driver factory, helpers
│   │   ├── config.py
│   │   ├── logger.py
│   │   ├── driver_factory.py
│   │   ├── humanize.py
│   │   ├── date_filter.py           # parse_date pt-BR/ISO (best effort)
│   │   └── dedupe.py
│   ├── genai/                       # LLM client, factory, prompts, summarizer
│   │   ├── llm_client.py            # Protocol abstrato
│   │   ├── factory.py               # resolve provider via .env
│   │   ├── llm_clients/
│   │   │   ├── stub.py              # offline (default)
│   │   │   └── openai_client.py     # opcional, lazy import
│   │   ├── prompts.py
│   │   └── summarizer.py
│   └── pdf/                         # Geração do PDF (fpdf2)
│       └── report.py                # generate_pdf(summary) → caminho absoluto
├── output/                          # PDFs gerados em runtime
├── tests/                           # Suíte pytest
├── .env.example                     # Variáveis de ambiente de exemplo
├── pyproject.toml                   # Config do pytest + coverage
└── requirements.txt                 # Dependências fixadas
```

---

## Pré-requisitos

- **Python 3.11+** instalado e disponível no `PATH`.
- **Google Chrome** (ou outro navegador suportado pelo Selenium)
  instalado.
- Acesso à internet.
- _(Quando o LLM for definido)_ Chave de API do provedor escolhido.

---

## Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone <url-do-repositorio>
cd RPA_SMART_NEWS
```

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Configuração

Copie o `.env.example` para `.env` e ajuste o que precisar:

```powershell
Copy-Item .env.example .env
```

| Variável | Default | Descrição |
|---|---|---|
| `LOG_LEVEL` | `INFO` | Nível de log (`DEBUG`/`INFO`/`WARNING`/`ERROR`) |
| `MAX_RETRIES` | `3` | Tentativas de input antes de abortar |
| `OUTPUT_DIR` | `output` | Diretório de saída do PDF |
| `HEADLESS` | `false` | Se `true`, abre Chrome sem interface |
| `SELENIUM_TIMEOUT` | `15` | Timeout (s) das esperas explícitas |
| `HUMANIZE_DELAY_MIN`/`MAX` | `0.8`/`2.5` | Faixa de delays randomizados (s) |
| `MAX_NEWS_PER_SITE` | `15` | Máximo de notícias coletadas por site |
| `LLM_PROVIDER` | `stub` | `stub` (offline) ou `openai` |
| `LLM_MODEL` | `gpt-4o-mini` | Modelo LLM (quando `LLM_PROVIDER != stub`) |
| `LLM_API_KEY` | *(vazio)* | API key do provedor (deixe vazio para o `stub`) |
| `LLM_TEMPERATURE` | `0.2` | Temperatura da chamada |
| `LLM_MAX_TOKENS` | `800` | Tokens máximos por resposta |

---

## Como executar

Com o ambiente virtual ativado:

```bash
python main.py
```

> Estado atual (R1 — Core completo): `main.py` executa o pipeline
> **end-to-end**:
>
> input → driver → coleta nas 4 fontes fixas → dedupe URL+título →
> sumarização (LLM) → **geração do PDF** → exibição do caminho
> absoluto.
>
> O arquivo é salvo em `output/<YYYYMMDD_HHMMSS>_<tema>.pdf`. Caso já
> exista (mesmo segundo + mesmo tema), `overwrite=False` adiciona
> sufixo `_2`, `_3`, ... evitando perder a execução anterior.

---

## Testes

A estratégia de testes utiliza **pytest** com cobertura via
**pytest-cov**, configurados em `pyproject.toml`. As fixtures comuns
ficam em `tests/conftest.py`.

> ⚠️ **Importante**: ative o `.venv` antes de executar qualquer comando
> abaixo (ver seção [Como executar](#como-executar)).

### Suíte completa

```powershell
pytest                              # roda todos os testes
pytest -v                           # modo verboso
```

### Com relatório de cobertura

```powershell
pytest --cov                                       # cobertura no terminal
pytest --cov --cov-report=term-missing             # mostra linhas faltantes
pytest --cov --cov-report=html                     # gera HTML em htmlcov/
```

### Filtros úteis

```powershell
pytest tests/test_topics.py                        # apenas um arquivo
pytest tests/test_menu.py::TestCollectUserInput    # uma classe específica
pytest -k "valido"                                 # filtra por nome
```

---

## Roadmap

- [x] Bootstrap do projeto (`.gitignore`, `requirements.txt`,
      `main.py`, `PROMPTS.md`, `README.md`)
- [x] Inicialização do repositório git
- [x] Definição da arquitetura e da estrutura de pastas (POM,
      services, genai, pdf, utils, tests)
- [x] **Cliente LLM abstraído** + provider `stub` (default) e `openai`
      opcional; embeddings/PDF a definir
- [x] Implementação da `BasePage` real
- [x] Helpers de comportamento humanizado (scroll, delays)
- [x] Deduplicação por **URL + título** (similaridade semântica fica
      para o R2)
- [x] Validação determinística de input (sem dias) — **B-006**
- [x] Page Objects das 4 fontes fixas — **B-008**
- [x] Coleta orquestrada nas 4 fontes — **B-009**
- [x] Tolerância a falhas (1 site cai → demais seguem) — **B-010**
- [x] Sumarização consolidada (sem `days`) — **B-012**
- [x] Geração do PDF (`fpdf2`: tema, resumo, bullets, fontes) — **B-013**
- [x] Mensagem final com caminho absoluto do PDF — **B-014**
- [ ] Robustez ampliada (retry + screenshot/HTML em zero coletas) — R2
- [ ] Deduplicação semântica via embeddings — R2
- [ ] Agrupamento por similaridade (clustering) — R2
- [ ] Sumarização por cluster + resumo executivo final — R2
- [ ] PDF apresentável (capa, sumário, paginação) — R3
- [ ] Documentação final e demo — R3

---

## Rastreabilidade dos prompts

Todos os prompts relevantes utilizados na construção do projeto estão
registrados em [`PROMPTS.md`](./PROMPTS.md), com:

- Data, etapa e ferramenta/modelo utilizado.
- Resumo do prompt enviado.
- O que foi efetivamente realizado/aceito.
- Artefatos gerados ou modificados.

Esse arquivo é **atualizado a cada interação relevante** com a IA
durante o projeto.

---

## Convenções de commit

O projeto adota o padrão **Conventional Commits**:

| Tipo | Uso |
|---|---|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Apenas documentação |
| `chore` | Tarefas de manutenção/configuração |
| `refactor` | Refatoração sem mudança de comportamento |
| `test` | Adição ou ajuste de testes |
| `style` | Formatação (sem mudança lógica) |
| `perf` | Melhorias de performance |

Exemplo:

```text
feat(pages): adiciona G1Page com fluxo editoria + busca interna
```

---

## Autor

Projeto acadêmico desenvolvido por **Leonardo Santos** no escopo da
pós-graduação **Engenharia de Software: Automação e Inovação com
Inteligência Artificial Generativa** — **UFG**.

---

_Última atualização: 2026-04-30 (R1 — Core completo: pipeline end-to-end com geração de PDF via `fpdf2`, 164 testes / 79% cobertura)._
