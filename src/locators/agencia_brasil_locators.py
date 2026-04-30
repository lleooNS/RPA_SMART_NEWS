"""Locators e URLs da Agência Brasil (`agenciabrasil.ebc.com.br`)."""

from __future__ import annotations

from urllib.parse import quote_plus

from src.models.topics import Topic
from src.pages.base_page import Locator

BASE_URL: str = "https://agenciabrasil.ebc.com.br"

EDITORIAL_PATHS: dict[Topic, str] = {
    Topic.ECONOMIA: "/economia",
    Topic.POLITICA: "/politica",
    Topic.ESPORTES: "/esportes",
    Topic.EVENTOS_GLOBAIS: "/internacional",
    Topic.SAUDE: "/saude",
    Topic.ENTRETENIMENTO: "/cultura",
    Topic.COTIDIANO: "/geral",
    Topic.CRIMES_SEGURANCA: "/justica",
}


def search_url(query: str) -> str:
    """URL da busca interna da Agência Brasil."""
    return f"{BASE_URL}/busca?q={quote_plus(query)}"


ARTICLE_LOCATORS: list[Locator] = [
    ("css selector", "article.materia-listagem"),
    ("css selector", "div.materia"),
    ("css selector", "li.list-item-noticia"),
    ("css selector", "div.col-busca"),
    ("css selector", "article"),
]

LINK_LOCATORS: list[Locator] = [
    ("css selector", "a.titulo-materia"),
    ("css selector", "h2 a"),
    ("css selector", "h3 a"),
    ("css selector", "a[href*='/noticia/']"),
    ("css selector", "a[href]"),
]

TITLE_LOCATORS: list[Locator] = [
    ("css selector", "a.titulo-materia"),
    ("css selector", "h2 a"),
    ("css selector", "h3 a"),
    ("css selector", "h2"),
    ("css selector", "h3"),
]

TIME_LOCATORS: list[Locator] = [
    ("css selector", "time"),
    ("css selector", "span.data-publicacao"),
    ("css selector", "[itemprop='datePublished']"),
]

SNIPPET_LOCATORS: list[Locator] = [
    ("css selector", "p.subtitulo"),
    ("css selector", ".chamada"),
    ("css selector", "p"),
]
