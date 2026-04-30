"""Prompts (system + user) usados pela camada de sumarização."""

from __future__ import annotations

from src.models.news import NewsArticle
from src.models.topics import Topic, label_for

SUMMARY_SYSTEM_PROMPT: str = (
    "Você é um analista de notícias em português do Brasil. Resuma as "
    "manchetes a seguir de forma objetiva, neutra e factual. "
    "REGRAS: (1) NÃO invente fatos — use apenas o conteúdo das manchetes; "
    "(2) cite os pontos principais em até 8 bullets curtos; "
    "(3) escreva em português brasileiro, em tom jornalístico; "
    "(4) inclua um parágrafo final de visão geral em 2-3 frases."
)


def build_summary_prompt(
    articles: list[NewsArticle],
    topic: Topic,
) -> str:
    """Monta o prompt do usuário com o tema e a lista de manchetes."""
    if not articles:
        return (
            f"Tema: {label_for(topic)}\n\n"
            "NOTÍCIAS:\n(nenhuma notícia coletada)\n"
        )

    lines: list[str] = []
    for idx, article in enumerate(articles, start=1):
        snippet = f" — {article.snippet}" if article.snippet else ""
        date = (
            article.published_at.strftime("%d/%m/%Y")
            if article.published_at
            else "data não identificada"
        )
        lines.append(
            f"{idx}. [{article.source} | {date}] {article.title}{snippet}"
        )

    return (
        f"Tema: {label_for(topic)}\n\n"
        "NOTÍCIAS:\n" + "\n".join(lines) + "\n\n"
        "RESPOSTA: produza o resumo seguindo as REGRAS do sistema."
    )
