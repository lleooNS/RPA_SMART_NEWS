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
notícias sobre um tema informado pelo usuário, em um intervalo de
datas, executando o navegador de forma **visível** (simulando um
humano, com scroll e esperas naturais). Ao final, entrega um **PDF**
com um resumo consolidado, agrupado por assuntos semelhantes e livre de
duplicatas.

A IA Generativa é aplicada em **múltiplos estágios** do fluxo:

- **Validação do tema** (guardrail contra temas restritos/sensíveis).
- **Classificação de relevância** das notícias coletadas.
- **Deduplicação semântica** (além de URL/título).
- **Agrupamento de assuntos** semelhantes (clustering).
- **Sumarização consolidada** por cluster e do resumo executivo final.

O projeto também explora o uso de GenAI em diferentes etapas do **ciclo
de vida do desenvolvimento de software**: concepção, codificação
assistida, geração de testes, documentação e refino — toda essa
trajetória é registrada em [`PROMPTS.md`](./PROMPTS.md).

---

## Funcionalidades

### Entradas
- Tema/assunto de interesse.
- Intervalo de datas (ex.: últimos 5 dias).

### Fluxo
1. Validação prévia do tema (rejeita conteúdos restritos com mensagem
   amigável solicitando outro tema).
2. Abertura visível do navegador (modo não-headless).
3. Coleta em **3 sites confiáveis** de notícias.
4. Scroll e esperas humanizadas para simular um usuário real.
5. Deduplicação (URL → título → similaridade semântica).
6. Agrupamento de notícias por similaridade temática.
7. Sumarização consolidada via LLM.
8. Exportação em **PDF** com capa, sumário executivo, agrupamentos e
   fontes.

### Saídas
- Arquivo **PDF** com o relatório final.
- Logs de execução.

---

## Arquitetura

> Diagrama em alto nível do fluxo do RPA. Será detalhado conforme o
> projeto evolui.

```text
┌─────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Usuário   │──▶│  Validação   │──▶│   Coleta     │──▶│   Pipeline   │
│ (tema+data) │   │  do tema     │   │  (Selenium   │   │  GenAI       │
│             │   │  (LLM)       │   │   + POM)     │   │  (dedupe,    │
│             │   │              │   │              │   │   cluster,   │
│             │   │              │   │              │   │   resumo)    │
└─────────────┘   └──────────────┘   └──────────────┘   └──────┬───────┘
                                                               │
                                                               ▼
                                                       ┌───────────────┐
                                                       │  Geração PDF  │
                                                       │   (output/)   │
                                                       └───────────────┘
```

A automação web segue o padrão **Page Object Model (POM)**, com uma
`BasePage` reaproveitável e Page Objects específicos para cada site
de notícias.

---

## Stack tecnológica

| Camada | Tecnologia |
|---|---|
| Linguagem | Python **3.11+** |
| Automação Web | Selenium 4 + webdriver-manager |
| Padrão de design (web) | Page Object Model (POM) |
| IA Generativa (LLM) | _A definir_ (OpenAI / Anthropic / Gemini / Ollama) |
| Embeddings / Similaridade | _A definir_ (sentence-transformers / API) |
| Geração de PDF | _A definir_ (ReportLab / fpdf2) |
| Configuração | python-dotenv |
| CLI / Logs | rich |
| Testes | pytest + pytest-cov |

> Itens marcados como _a definir_ estão como **placeholders comentados**
> em `requirements.txt` e serão fixados conforme as decisões do
> projeto avançam.

---

## Estrutura do projeto

> A estrutura abaixo representa o estado atual e será expandida
> conforme novas etapas (POM, services, genai, pdf, tests) forem
> implementadas.

```text
RPA_SMART_NEWS/
├── .venv/                    # Ambiente virtual (não versionado)
├── .gitignore                # Regras de ignore (Python, venv, caches, saídas)
├── main.py                   # Ponto de entrada do RPA
├── requirements.txt          # Dependências do projeto
├── PROMPTS.md                # Rastreabilidade dos prompts utilizados
└── README.md                 # Este arquivo
```

### Estrutura planejada (próximas etapas)

```text
RPA_SMART_NEWS/
├── src/
│   ├── pages/                # Page Objects (POM) por site
│   │   ├── base_page.py
│   │   └── ...
│   ├── services/             # Orquestração do fluxo
│   ├── genai/                # Prompts, clientes LLM, dedupe e clustering
│   ├── pdf/                  # Geração do relatório final
│   └── utils/                # Helpers (scroll humanizado, logging, etc.)
├── tests/                    # Testes unitários (pytest)
├── output/                   # PDFs gerados (não versionado)
└── .env.example              # Variáveis de ambiente de exemplo
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

Variáveis de ambiente serão centralizadas em um arquivo `.env` (não
versionado). Um `.env.example` será disponibilizado quando o LLM for
definido.

Exemplo (preliminar):

```dotenv
# Provedor de LLM (a definir)
LLM_PROVIDER=openai
LLM_API_KEY=sua-chave-aqui
LLM_MODEL=gpt-4o-mini

# Comportamento do RPA
HEADLESS=false
HUMANIZE_DELAY_MIN=0.8
HUMANIZE_DELAY_MAX=2.5
OUTPUT_DIR=output
```

---

## Como executar

Com o ambiente virtual ativado:

```bash
python main.py
```

> No estado atual, `main.py` apenas exibe a mensagem de inicialização
> do projeto. O fluxo completo do RPA será habilitado conforme os
> módulos forem implementados (ver [Roadmap](#roadmap)).

---

## Testes

A estratégia de testes utiliza **pytest** com cobertura via
**pytest-cov**.

```bash
pytest -v
pytest --cov=src --cov-report=term-missing
```

> A suíte de testes será criada à medida que os módulos forem
> implementados.

---

## Roadmap

- [x] Bootstrap do projeto (`.gitignore`, `requirements.txt`,
      `main.py`, `PROMPTS.md`, `README.md`)
- [x] Inicialização do repositório git
- [ ] Definição da arquitetura e da estrutura de pastas (POM,
      services, genai, pdf, utils, tests)
- [ ] Escolha do provedor de LLM, biblioteca de embeddings e
      biblioteca de PDF
- [ ] Implementação da `BasePage` e dos Page Objects dos 3 sites
- [ ] Helpers de comportamento humanizado (scroll, esperas, mouse)
- [ ] Guardrail de validação de tema (LLM)
- [ ] Pipeline de coleta de notícias
- [ ] Deduplicação (URL + título + similaridade semântica)
- [ ] Agrupamento por similaridade (clustering)
- [ ] Sumarização consolidada (por cluster + executiva)
- [ ] Geração do PDF (capa, sumário, seções, fontes)
- [ ] Suíte de testes (pytest)
- [ ] Documentação final e demo

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
feat(genai): adiciona guardrail de validação de tema via LLM
```

---

## Autor

Projeto acadêmico desenvolvido por **Lucas Santos** no escopo da
pós-graduação **Engenharia de Software: Automação e Inovação com
Inteligência Artificial Generativa** — **UFG**.

---

_Última atualização: 2026-04-30_
