"""Deduplicação básica (URL canônica + título normalizado).

A camada **semântica** (embeddings) está prevista para o R2 (B-104).
Aqui cobrimos as duas primeiras camadas do RF09.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Iterable
from urllib.parse import urlparse, urlunparse

from src.models.news import NewsArticle

_PUNCT_RE = re.compile(r"[^\w\s]+", flags=re.UNICODE)
_WS_RE = re.compile(r"\s+")


def normalize_url(url: str) -> str:
    """Remove querystring, fragmento e barra final para canonizar a URL."""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/") or "/"
    canonical = parsed._replace(
        query="",
        fragment="",
        path=path,
        netloc=parsed.netloc.lower(),
    )
    return urlunparse(canonical)


def normalize_title(title: str) -> str:
    """Lowercase, sem acentos, sem pontuação, espaços colapsados."""
    nfkd = unicodedata.normalize("NFKD", title)
    no_accents = "".join(c for c in nfkd if not unicodedata.combining(c))
    cleaned = _PUNCT_RE.sub(" ", no_accents.lower())
    return _WS_RE.sub(" ", cleaned).strip()


def dedupe(articles: Iterable[NewsArticle]) -> list[NewsArticle]:
    """Remove duplicatas por URL canônica e por hash de título normalizado."""
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    unique: list[NewsArticle] = []
    for article in articles:
        url_key = normalize_url(str(article.url))
        title_key = normalize_title(article.title)
        if url_key in seen_urls or (title_key and title_key in seen_titles):
            continue
        seen_urls.add(url_key)
        if title_key:
            seen_titles.add(title_key)
        unique.append(article)
    return unique
