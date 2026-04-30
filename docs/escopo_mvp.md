# Escopo do MVP — RPA_SMART_NEWS

> Documento de **escopo do MVP** do projeto RPA_SMART_NEWS, mini-projeto
> do módulo *Laboratório Introdutório: Construindo um Mini-projeto com
> Inteligência Artificial Generativa* — Pós-graduação em Engenharia de
> Software: Automação e Inovação com IA Generativa (UFG).
>
> Este documento é **vivo** e será atualizado conforme o projeto evolui.

---

## Sumário

- [1. Objetivo](#1-objetivo)
- [2. Personas e premissas](#2-personas-e-premissas)
- [3. Temas suportados](#3-temas-suportados)
- [4. Requisitos funcionais (RF)](#4-requisitos-funcionais-rf)
- [5. Requisitos não funcionais (RNF)](#5-requisitos-não-funcionais-rnf)
- [6. Aplicação da GenAI no ciclo de desenvolvimento](#6-aplicação-da-genai-no-ciclo-de-desenvolvimento)
- [7. Fora de escopo](#7-fora-de-escopo)
- [8. Critérios de aceite do MVP](#8-critérios-de-aceite-do-mvp)
- [9. Riscos e mitigações](#9-riscos-e-mitigações)
- [10. Glossário](#10-glossário)
- [Histórico de revisões](#histórico-de-revisões)

---

## 1. Objetivo

Construir um **MVP de RPA**, em Python, que automatize a **pesquisa,
consolidação e sumarização de notícias** sobre um **tema escolhido pelo
usuário a partir de uma lista pré-definida**, considerando os **últimos
N dias**, executando o navegador de forma **visível** (simulando um
humano) e entregando um **relatório em PDF**.

O projeto explora a aplicação de **IA Generativa em múltiplos estágios
do ciclo de vida do desenvolvimento de software** (concepção,
codificação, sumarização semântica, agrupamento, validação de conteúdo,
testes e documentação).

---

## 2. Personas e premissas

### Persona principal
- **Usuário leigo** (não-técnico) que quer obter um panorama rápido
  de notícias sobre um tema, sem precisar abrir vários sites
  manualmente.

### Premissas
- Execução **local**, em máquina pessoal (Windows, Linux ou macOS).
- Usuário possui **Python 3.11+** e **Google Chrome** instalados.
- Conexão à internet disponível durante a execução.
- Para o uso da GenAI, o usuário fornece uma **chave de API** do
  provedor escolhido (definido no decorrer do projeto).
- Idioma das notícias-alvo: **Português (Brasil)**.

---

## 3. Temas suportados

Para **evitar entradas indesejadas** e manter a experiência do usuário
simples e previsível, o MVP trabalha com uma **lista fixa** de **10
temas** baseados nos assuntos de notícias mais buscados. O usuário
**seleciona um tema da lista** e informa **quantos dias** (últimos N
dias) deseja consultar, dentro do limite **1 ≤ N ≤ 10**.

> **Limite de N nesta versão**: o intervalo está restrito a **no
> máximo 10 dias** para evitar volume excessivo de notícias e
> preservar a performance do MVP. Esse limite poderá ser flexibilizado
> em versões futuras.

| # | Tema |
|---|---|
| 1 | Economia |
| 2 | Política |
| 3 | Esportes |
| 4 | Eventos globais |
| 5 | Saúde |
| 6 | Tecnologia |
| 7 | Entretenimento |
| 8 | Clima |
| 9 | Crimes/Segurança |
| 10 | Cotidiano |

> A lista funciona como um **guardrail determinístico** de entrada,
> dispensando a necessidade de validação via LLM no runtime para os
> inputs do usuário.

---

## 4. Requisitos funcionais (RF)

| ID | Descrição | Prioridade |
|---|---|---|
| **RF01** | O sistema deve **exibir um menu numerado** com os **10 temas pré-definidos** (ver seção [Temas suportados](#3-temas-suportados)) e permitir ao usuário **selecionar um deles** via CLI. | Alta |
| **RF02** | O sistema deve permitir que o usuário informe o **número de dias N** (inteiro com **1 ≤ N ≤ 10**), correspondendo aos **últimos N dias** a partir de hoje. O **limite máximo de 10 dias** é uma restrição desta versão para preservar performance. | Alta |
| **RF03** | O sistema deve **validar deterministicamente os inputs** do usuário (seleção entre **1–10** para tema e **1–10** para dias), sem depender de LLM. A validação deve usar **modelos Pydantic v2**. | Alta |
| **RF04** | O sistema deve **rejeitar inputs inválidos** (fora do menu ou fora do intervalo `1–10` de dias) com **mensagem amigável** e **re-solicitar** a entrada (com limite de tentativas). | Alta |
| **RF05** | O sistema deve **abrir o navegador em modo visível** (não-headless) para o usuário acompanhar a execução. | Alta |
| **RF06** | O sistema deve **simular comportamento humano** durante a navegação: scroll suave, pequenas pausas randomizadas, movimentos não-instantâneos. | Alta |
| **RF07** | O sistema deve **coletar notícias em 3 sites confiáveis** previamente definidos (ex.: G1, BBC Brasil, Agência Brasil — lista final a ser definida). | Alta |
| **RF08** | O sistema deve **filtrar as notícias coletadas** pelo intervalo dos **últimos N dias** informado. | Alta |
| **RF09** | O sistema deve **remover notícias duplicadas**, em camadas: URL → hash de título → similaridade semântica via embeddings. | Alta |
| **RF10** | O sistema deve **agrupar notícias por similaridade temática** (clustering) e nomear cada cluster (via LLM). | Alta |
| **RF11** | O sistema deve **gerar um resumo por cluster** utilizando LLM. | Alta |
| **RF12** | O sistema deve **gerar um resumo executivo consolidado** do conjunto de notícias. | Alta |
| **RF13** | O sistema deve **exportar o resultado em PDF**, contendo: capa, sumário executivo, seções por cluster (com resumo + fontes), data/hora de geração, tema e intervalo pesquisados. | Alta |
| **RF14** | O sistema deve **registrar logs de execução** (início/fim de cada etapa, sites visitados, contagem de notícias coletadas/filtradas/deduplicadas). | Média |
| **RF15** | O sistema deve **tratar falhas** comuns (timeout, site indisponível, mudança de seletor) com mensagens claras e, quando possível, prosseguir com os demais sites. | Média |
| **RF16** | O sistema deve **informar ao usuário o caminho do PDF gerado** ao final da execução. | Alta |

---

## 5. Requisitos não funcionais (RNF)

| ID | Categoria | Descrição |
|---|---|---|
| **RNF01** | Tecnologia | Implementado em **Python 3.11+**. |
| **RNF02** | Compatibilidade | Executável em **Windows, Linux e macOS**. |
| **RNF03** | Arquitetura | A automação web deve seguir o padrão **Page Object Model (POM)**, com `BasePage` reaproveitável. |
| **RNF04** | Tecnologia | Automação web baseada em **Selenium 4** com `webdriver-manager` (gestão automática do driver). |
| **RNF05** | Configuração | Parâmetros sensíveis (API keys) e de comportamento (delays, headless, output dir) **devem ser carregados via `.env`** (não versionado), com `.env.example` documentado. |
| **RNF06** | Observabilidade | Logs **estruturados** (níveis INFO/WARNING/ERROR), com timestamps. |
| **RNF07** | Performance | Execução completa em até **5 minutos** para um tema comum, considerando 3 sites e ~30 notícias coletadas (alvo, não bloqueante). |
| **RNF08** | UX | Mensagens ao usuário em **português**, claras e acionáveis. |
| **RNF09** | Segurança | **Nenhuma credencial** deve ser hardcoded; segredos somente via `.env`. |
| **RNF10** | Rastreabilidade | Os prompts utilizados durante a construção do projeto devem ser registrados em `PROMPTS.md`. |
| **RNF11** | Qualidade | Cobertura mínima de testes unitários de **60%** nas funções utilitárias e na camada GenAI (com mocks). |
| **RNF12** | Robustez | Tolerância a falhas com **timeouts explícitos** e **retries** controlados. |
| **RNF13** | Documentação | `README.md`, `PROMPTS.md` e `docs/escopo_mvp.md` mantidos atualizados. |
| **RNF14** | Comportamento humanizado | Delays randomizados dentro de uma faixa configurável (default: 0,8s a 2,5s). |
| **RNF15** | Ética e responsabilidade | Respeito a `robots.txt` quando aplicável; sem coleta abusiva; uso responsável de LLM (sem alucinações sem fonte). |
| **RNF16** | Reprodutibilidade | Dependências fixadas em `requirements.txt`; instalação reproduzível em `.venv`. |
| **RNF17** | Manutenibilidade | **Código limpo**: tipado (type hints), modular, **docstrings curtas e objetivas**, sem comentários redundantes. |
| **RNF18** | Versionamento | Repositório git com mensagens no padrão **Conventional Commits**. |
| **RNF19** | Validação | **Pydantic v2** para modelos de dados e validação de inputs (menu, dias, configuração via `.env`). |

---

## 6. Aplicação da GenAI no ciclo de desenvolvimento

A GenAI atua em **dois eixos** do projeto:

### 6.1. GenAI **dentro do produto** (runtime)
- **Classificação de relevância** das notícias frente ao tema
  selecionado (ex.: filtrar notícias de "Esportes" de baixa
  aderência ao escopo).
- **Deduplicação semântica** — comparação de embeddings para
  identificar conteúdos equivalentes.
- **Clustering temático** + **nomeação automática** de clusters.
- **Sumarização** por cluster e **resumo executivo** consolidado.

> A **validação de input** do usuário **não usa LLM** no MVP — é
> feita de forma **determinística** sobre o menu de [Temas
> suportados](#3-temas-suportados) e o número de dias.

### 6.2. GenAI **na construção** do produto (ciclo de desenvolvimento)
- **Concepção e refinamento** do escopo (este documento).
- **Geração de código** assistida (POM, helpers, parsers).
- **Geração e revisão de testes** unitários.
- **Documentação** (README, escopo, PROMPTS, docstrings).
- **Refatoração** e revisão de qualidade.

> O uso da GenAI no ciclo é registrado em `PROMPTS.md`, garantindo
> rastreabilidade acadêmica.

---

## 7. Fora de escopo

Os itens abaixo **não fazem parte** do MVP, podendo ser considerados
em evoluções futuras:

| # | Item | Motivo |
|---|---|---|
| 1 | Deploy em produção (cloud, container, SaaS). | MVP de uso local. |
| 2 | Interface gráfica web ou desktop. | Foco em CLI; UI não é objetivo do módulo. |
| 3 | Autenticação / autorização de usuários. | Uso pessoal/local. |
| 4 | Persistência em banco de dados (histórico de pesquisas). | Não agrega ao objetivo do MVP. |
| 5 | Agendamento automático (cron, scheduler). | Execução sob demanda. |
| 6 | Suporte a notícias em **outros idiomas** além de pt-BR. | Limitação de escopo do MVP. |
| 7 | Coleta em **mais de 3 sites** ou em redes sociais. | Definido como 3 sites confiáveis. |
| 8 | **Fact-checking** automatizado das notícias coletadas. | Fora do escopo acadêmico do MVP. |
| 9 | Notificações (e-mail, push, webhook). | Não previsto. |
| 10 | Geração de saídas em **outros formatos** (DOCX, HTML, JSON). | Apenas PDF. |
| 11 | API REST para consumo externo. | Sem ganho para o MVP. |
| 12 | Treinamento ou fine-tuning de modelos. | Apenas uso de modelos prontos. |
| 13 | Cache persistente entre execuções. | Cada execução é independente. |
| 14 | Tradução automática das notícias. | Mantém o idioma original. |
| 15 | Análise de sentimento / classificação política. | Pode introduzir viés; fora do escopo. |
| 16 | **Tema livre** (texto aberto) digitado pelo usuário. | Substituído pelo menu fixo de 10 temas (ver seção 3). |

---

## 8. Critérios de aceite do MVP

O MVP será considerado **concluído** quando, em uma execução
end-to-end:

1. O usuário consegue **selecionar um tema** da lista e informar o
   **número de dias** via CLI.
2. Um input **inválido** (fora do menu `1–10` ou dias fora de `1–10`)
   é **rejeitado** com mensagem amigável e o sistema **re-solicita**
   a entrada.
3. O navegador abre **visivelmente** e percorre os 3 sites com scroll.
4. Pelo menos **um conjunto de notícias** é coletado, deduplicado e
   agrupado.
5. Um **PDF** é gerado em `output/`, contendo capa, sumário
   executivo, seções por cluster e fontes.
6. O caminho do PDF é exibido ao final da execução.
7. A execução completa não levanta exceções não tratadas.
8. `README.md`, `PROMPTS.md` e `docs/escopo_mvp.md` refletem o estado
   final do projeto.

---

## 9. Riscos e mitigações

| Risco | Impacto | Mitigação |
|---|---|---|
| Mudanças de layout dos sites quebram os Page Objects. | Alto | POM bem isolado, seletores configuráveis, logs claros. |
| Bloqueio por anti-bot dos sites. | Alto | Comportamento humanizado (delays, scroll), respeito a `robots.txt`, fallback para outro site. |
| Custos com API de LLM excedem o esperado. | Médio | Uso de modelos econômicos (ex.: `gpt-4o-mini` ou similar), limite de tokens, cache em memória durante a execução. |
| Alucinações do LLM no resumo. | Médio | Prompt com instrução explícita de "apenas com base nas fontes"; inclusão de links das fontes no PDF. |
| Tema pré-definido amplo (ex.: "Esportes") gera coleta heterogênea. | Médio | Classificação de relevância via LLM e clustering por sub-assunto. |
| Tempo de execução longo. | Baixo | Limite de notícias por site; paralelização futura (fora deste MVP). |
| Conteúdo coletado com restrições autorais. | Médio | Sumarização própria + citação clara da fonte/URL. |

---

## 10. Glossário

| Termo | Definição |
|---|---|
| **RPA** | *Robotic Process Automation* — automação de processos repetitivos via software. |
| **GenAI** | *Generative AI* — IA generativa, capaz de produzir texto, código, imagens etc. |
| **LLM** | *Large Language Model* — modelo de linguagem de grande porte (ex.: GPT, Claude, Gemini). |
| **POM** | *Page Object Model* — padrão de design para automação web que isola a interação com cada página em uma classe. |
| **Embedding** | Representação vetorial de um texto, usada para medir similaridade semântica. |
| **Clustering** | Agrupamento não supervisionado de itens similares. |
| **Guardrail** | Mecanismo de proteção/filtragem aplicado antes ou depois de uma chamada ao LLM. Neste MVP, usamos um **guardrail determinístico** (menu fixo) para o input do usuário. |
| **Headless** | Execução do navegador sem interface gráfica. Neste MVP, **não** é utilizado. |

---

## Histórico de revisões

| Versão | Data | Autor | Descrição |
|---|---|---|---|
| 0.1 | 2026-04-30 | Leonardo Santos | Versão inicial do escopo do MVP. |
| 0.2 | 2026-04-30 | Leonardo Santos | Substitui input livre de tema por **menu fixo de 10 temas**; remove guardrail LLM no input; ajusta RF01/RF03/RF04, critérios de aceite e riscos. |
| 0.3 | 2026-04-30 | Leonardo Santos | Limita N a **1–10 dias** (RF02); adiciona **RNF19 (Pydantic v2)**; reforça RNF17 (código limpo + docstrings curtas); ajusta RF03/RF04 e critério de aceite #2. |
