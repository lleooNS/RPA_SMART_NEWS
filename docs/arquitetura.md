# Arquitetura — RPA_SMART_NEWS

> Diagramas de **componentes** e **fluxo de dados** do MVP, em
> **Mermaid** — simples, legível e versionável diretamente em
> Markdown.
>
> Documento **vivo** — atualizado conforme a arquitetura evolui.

---

## Sumário

- [1. Diagrama de componentes](#1-diagrama-de-componentes)
- [2. Diagrama de fluxo de dados](#2-diagrama-de-fluxo-de-dados)
- [3. Legenda](#3-legenda)
- [Histórico de revisões](#histórico-de-revisões)

---

## 1. Diagrama de componentes

Visão estática dos módulos do projeto, suas responsabilidades e
relacionamentos.

```mermaid
flowchart TB
    subgraph CLI["Camada CLI / Bootstrap"]
        MAIN["main.py<br/>(entrypoint)"]
        CFG["Config Loader<br/>(.env)"]
        LOG["Logger"]
    end

    subgraph SVC["Serviços / Orquestração"]
        ORCH["Orchestrator"]
        MENU["Theme Menu + Validator<br/>(Pydantic v2 — 10 temas)"]
        COLL["News Collector"]
        DEDUP["Deduplicator<br/>(URL + título + semântica)"]
        CLUS["Clusterer"]
        SUMM["Summarizer<br/>(por cluster + executivo)"]
    end

    subgraph WEB["Automação Web (POM — 1 Page Object por site)"]
        DRV["Driver Factory<br/>(Selenium + chromedriver-autoinstaller)"]
        BP["BasePage"]
        BNP["BaseNewsPage<br/>(editoria → busca interna)"]
        G1["G1Page<br/>(g1.globo.com)"]
        BBC["BBCBrasilPage<br/>(bbc.com/portuguese)"]
        AB["AgenciaBrasilPage<br/>(agenciabrasil.ebc.com.br)"]
        R7["R7Page<br/>(r7.com)"]
        HUM["Humanize Helper<br/>(scroll + delays)"]
    end

    subgraph AI["GenAI"]
        LLM["LLM Client<br/>(interface)"]
        EMB["Embeddings Client<br/>(interface)"]
    end

    subgraph OUT["Saída"]
        PDF["PDF Generator"]
        FS[("output/")]
    end

    MAIN --> CFG
    MAIN --> LOG
    MAIN --> ORCH

    ORCH --> MENU
    ORCH --> COLL
    ORCH --> DEDUP
    ORCH --> CLUS
    ORCH --> SUMM
    ORCH --> PDF

    COLL --> G1
    COLL --> BBC
    COLL --> AB
    COLL --> R7
    G1 --> BNP
    BBC --> BNP
    AB --> BNP
    R7 --> BNP
    BNP --> BP
    BP --> DRV
    BP --> HUM

    DEDUP --> EMB
    CLUS --> EMB
    CLUS --> LLM
    SUMM --> LLM

    PDF --> FS
```

---

## 2. Diagrama de fluxo de dados

Visão dinâmica de como os dados percorrem o pipeline, do input do
usuário até a entrega do PDF.

```mermaid
flowchart LR
    U([Usuário]) -->|escolha do menu| CLI["CLI<br/>(main.py)"]
    CLI -->|seleção 1–10| VG{"Validação<br/>(Pydantic v2)"}
    VG -->|inválido| ERR["Mensagem amigável<br/>+ re-solicita input"]
    ERR -.->|nova tentativa| CLI
    VG -->|válido| WEB["Coleta nas 4 fontes fixas<br/>(G1, BBC News Brasil,<br/>Agência Brasil, R7)"]
    WEB -->|notícias brutas| DD1["Dedupe<br/>URL + título"]
    DD1 -->|notícias únicas| DD2["Dedupe semântica<br/>(embeddings — R2)"]
    DD2 -->|notícias deduplicadas| CL["Clustering<br/>+ nomeação (LLM — R2)"]
    CL -->|grupos temáticos| SU1["Sumarização<br/>por cluster (LLM — R2)"]
    SU1 -->|resumos por grupo| SU2["Resumo executivo<br/>consolidado (LLM)"]
    SU2 -->|conteúdo final| PDF["Geração de PDF"]
    PDF -->|arquivo .pdf| OUT[("output/")]
    OUT -->|caminho do PDF| U
```

---

## 3. Legenda

| Notação | Significado |
|---|---|
| `[Texto]` | Componente / etapa de processamento |
| `([Texto])` | Ator externo (ex.: usuário) |
| `{Texto}` | Decisão / ramificação |
| `[(Texto)]` | Armazenamento (sistema de arquivos, base) |
| `subgraph` | Agrupamento lógico (camada / módulo) |
| `-->|label|` | Fluxo com rótulo descrevendo o dado/evento |

---

## Histórico de revisões

| Versão | Data | Autor | Descrição |
|---|---|---|---|
| 0.1 | 2026-04-30 | Leonardo Santos | Versão inicial: componentes e fluxo de dados. |
| 0.2 | 2026-04-30 | Leonardo Santos | Substitui guardrail LLM por **menu determinístico** (10 temas + N dias) nos dois diagramas. |
| 0.3 | 2026-04-30 | Leonardo Santos | Inclui **Pydantic v2** nos labels de validação e o limite **1–10 dias**. |
| 0.4 | 2026-04-30 | Leonardo Santos | Troca `webdriver-manager` por **`chromedriver-autoinstaller`** no nó `Driver Factory`. |
| 0.5 | 2026-04-30 | Leonardo Santos | **Opção E aplicada**: discovery e coleta migram para `news.google.com`; introduz nós `GoogleNewsPage`, `Adapter Registry`, `GenericNewsAdapter` e (futuros) adapters curados. Filtro de janela passa a ser **local** sobre `published_at`. |
| 0.6 | 2026-04-30 | Leonardo Santos | **Reset arquitetural**: remove integração com Google (`GoogleNewsPage`, `Adapter Registry`, `GenericNewsAdapter`, filtro de janela). Volta para **POM por site fixo** (G1, BBC News Brasil, Agência Brasil, R7), com `BaseNewsPage` que tenta editoria → busca interna. Remove o nó "número de dias" do fluxo — a única entrada do usuário é o tema. |
