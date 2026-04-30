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
        VAL["Theme Validator<br/>(Guardrail)"]
        COLL["News Collector"]
        FILT["Date Filter"]
        DEDUP["Deduplicator<br/>(URL + título + semântica)"]
        CLUS["Clusterer"]
        SUMM["Summarizer<br/>(por cluster + executivo)"]
    end

    subgraph WEB["Automação Web (POM)"]
        DRV["Driver Factory<br/>(Selenium + webdriver-manager)"]
        BP["BasePage"]
        S1["Site 1 — Page Object"]
        S2["Site 2 — Page Object"]
        S3["Site 3 — Page Object"]
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

    ORCH --> VAL
    ORCH --> COLL
    ORCH --> FILT
    ORCH --> DEDUP
    ORCH --> CLUS
    ORCH --> SUMM
    ORCH --> PDF

    VAL --> LLM

    COLL --> DRV
    DRV --> BP
    BP --> S1
    BP --> S2
    BP --> S3
    S1 --> HUM
    S2 --> HUM
    S3 --> HUM

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
    U([Usuário]) -->|tema + intervalo| CLI["CLI<br/>(main.py)"]
    CLI -->|parâmetros validados| VG{Guardrail<br/>LLM}
    VG -->|restrito| ERR["Mensagem amigável<br/>+ encerra"]
    VG -->|permitido| WEB["Coleta Web<br/>(3 sites — POM)"]
    WEB -->|notícias brutas| FD["Filtro<br/>por intervalo de datas"]
    FD -->|notícias filtradas| DD1["Dedupe<br/>URL + título"]
    DD1 -->|notícias únicas| DD2["Dedupe semântica<br/>(embeddings)"]
    DD2 -->|notícias deduplicadas| CL["Clustering<br/>+ nomeação (LLM)"]
    CL -->|grupos temáticos| SU1["Sumarização<br/>por cluster (LLM)"]
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
