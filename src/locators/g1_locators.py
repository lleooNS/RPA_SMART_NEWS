"""Locators e construtores de URL do G1 (`g1.globo.com`)."""

from __future__ import annotations

from urllib.parse import quote_plus

from src.models.topics import Topic
from src.pages.base_page import Locator

BASE_URL: str = "https://g1.globo.com"

EDITORIAL_PATHS: dict[Topic, str] = {
    Topic.ECONOMIA: "/economia/",
    Topic.POLITICA: "/politica/",
    Topic.ESPORTES: "/esporte/",
    Topic.EVENTOS_GLOBAIS: "/mundo/",
    Topic.SAUDE: "/saude/",
    Topic.TECNOLOGIA: "/tecnologia/",
    Topic.ENTRETENIMENTO: "/pop-arte/",
    Topic.CLIMA: "/meio-ambiente/",
}


def search_url(query: str) -> str:
    """URL da busca interna do G1 para o termo informado."""
    return f"{BASE_URL}/busca/?q={quote_plus(query)}"


ARTICLE_LOCATORS: list[Locator] = [
    ("css selector", "div.feed-post"),
    ("css selector", "div.bastian-feed-item"),
    ("css selector", "div.widget--info"),
    ("css selector", "li.widget--info"),
    ("css selector", "article"),
]

LINK_LOCATORS: list[Locator] = [
    ("css selector", "a.feed-post-link"),
    ("css selector", "a.gui-color-primary-link"),
    ("css selector", "h2 a"),
    ("css selector", "h3 a"),
    ("css selector", "a[href*='/noticia/']"),
    ("css selector", "a[href]"),
]

TITLE_LOCATORS: list[Locator] = [
    ("css selector", "a.feed-post-link"),
    ("css selector", ".feed-post-body-title"),
    ("css selector", "h2 a"),
    ("css selector", "h3 a"),
    ("css selector", "h2"),
    ("css selector", "h3"),
]

TIME_LOCATORS: list[Locator] = [
    ("css selector", "time"),
    ("css selector", ".feed-post-datetime"),
    ("css selector", ".bastian-page-section__date"),
]

SNIPPET_LOCATORS: list[Locator] = [
    ("css selector", ".feed-post-body-resumo"),
    ("css selector", ".bastian-page-section__resumo"),
    ("css selector", "p"),
]
