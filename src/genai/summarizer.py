"""Sumarização consolidada (B-012, versão simples).

A versão por cluster (B-105) e o resumo executivo final (B-106) são do R2.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

from src.genai.factory import get_llm_client
from src.genai.llm_client import LLMClient
from src.genai.prompts import SUMMARY_SYSTEM_PROMPT, build_summary_prompt
from src.models.news import NewsArticle
from src.models.summary import SourceRef, Summary
from src.models.topics import Topic
from src.utils.config import Settings, get_settings
from src.utils.logger import get_logger

logger = get_logger()

_BULLET_LINE_RE = re.compile(r"^\s*[-*\u2022]\s*(.+)$", flags=re.MULTILINE)


def summarize(
    articles: list[NewsArticle],
    topic: Topic,
    *,
    settings: Settings | None = None,
    client: LLMClient | None = None,
) -> Summary:
    """Gera o `Summary` consolidado a partir da lista de notícias."""
    cfg = settings or get_settings()
    llm = client or get_llm_client(cfg)

    prompt = build_summary_prompt(articles, topic)
    raw = llm.complete(
        system=SUMMARY_SYSTEM_PROMPT,
        prompt=prompt,
        temperature=cfg.llm_temperature,
        max_tokens=cfg.llm_max_tokens,
    )

    bullets = [m.group(1).strip() for m in _BULLET_LINE_RE.finditer(raw)]
    sources = [
        SourceRef(title=a.title, url=a.url, source=a.source)
        for a in articles
    ]

    summary = Summary(
        topic=topic,
        generated_at=datetime.now(timezone.utc),
        executive_summary=raw,
        bullets=bullets,
        sources=sources,
        metadata={
            "llm_provider": llm.name,
            "articles_total": len(articles),
        },
    )
    logger.info(
        "Sumarização concluída | provider=%s | bullets=%d | sources=%d",
        llm.name,
        len(bullets),
        len(sources),
    )
    return summary
