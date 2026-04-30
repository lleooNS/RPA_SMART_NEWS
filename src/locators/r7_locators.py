"""Locators e URLs do R7 (`r7.com`)."""

from __future__ import annotations

from urllib.parse import quote_plus

from src.models.topics import Topic
from src.pages.base_page import Locator

BASE_URL: str = "https://www.r7.com"

EDITORIAL_PATHS: dict[Topic, str] = {
    Topic.ECONOMIA: "/economia",
    Topic.POLITICA: "/politica",
    Topic.ESPORTES: "/esportes",
    Topic.EVENTOS_GLOBAIS: "/internacional",
    Topic.SAUDE: "/saude",
    Topic.TECNOLOGIA: "/tecnologia-e-ciencia",
    Topic.ENTRETENIMENTO: "/entretenimento",
    Topic.CRIMES_SEGURANCA: "/cidades",
}


def search_url(query: str) -> str:
    """URL da busca interna do R7."""
    return f"{BASE_URL}/busca?q={quote_plus(query)}"


ARTICLE_LOCATORS: list[Locator] = [
    ("css selector", "article"),
    ("css selector", "div.card"),
    ("css selector", "li.item-busca"),
    ("css selector", "div[class*='Card']"),
]

LINK_LOCATORS: list[Locator] = [
    ("css selector", "a[href*='/noticia']"),
    ("css selector", "a[href*='r7.com/']"),
    ("css selector", "h2 a"),
    ("css selector", "h3 a"),
    ("css selector", "a[href]"),
]

TITLE_LOCATORS: list[Locator] = [
    ("css selector", "h2 a"),
    ("css selector", "h3 a"),
    ("css selector", "h2"),
    ("css selector", "h3"),
    ("css selector", ".titulo-materia"),
]

TIME_LOCATORS: list[Locator] = [
    ("css selector", "time"),
    ("css selector", ".data"),
    ("css selector", "span.publicado"),
]

SNIPPET_LOCATORS: list[Locator] = [
    ("css selector", "p.chamada"),
    ("css selector", ".resumo"),
    ("css selector", "p"),
]
