"""Locators e construtores de URL da BBC News Brasil (`bbc.com/portuguese`)."""

from __future__ import annotations

from urllib.parse import quote_plus

from src.pages.base_page import Locator

BASE_URL: str = "https://www.bbc.com"


def search_url(query: str) -> str:
    """URL da busca interna da BBC para o termo informado."""
    return f"{BASE_URL}/portuguese/search?q={quote_plus(query)}"


ARTICLE_LOCATORS: list[Locator] = [
    ("css selector", "li[class*='ssrcss-']"),
    ("css selector", "div[data-testid*='card']"),
    ("css selector", "div[data-entityid]"),
    ("css selector", "article"),
    ("css selector", "li.gel-layout__item"),
]

LINK_LOCATORS: list[Locator] = [
    ("css selector", "a[href*='/portuguese/']"),
    ("css selector", "a.gs-c-promo-heading"),
    ("css selector", "h2 a"),
    ("css selector", "h3 a"),
    ("css selector", "a[href]"),
]

TITLE_LOCATORS: list[Locator] = [
    ("css selector", "a.gs-c-promo-heading"),
    ("css selector", "h3"),
    ("css selector", "h2"),
    ("css selector", "[data-testid='card-headline']"),
]

TIME_LOCATORS: list[Locator] = [
    ("css selector", "time"),
    ("css selector", "[data-testid='card-metadata-lastupdated']"),
    ("css selector", ".gs-c-timestamp"),
]

SNIPPET_LOCATORS: list[Locator] = [
    ("css selector", "[data-testid='card-description']"),
    ("css selector", ".gs-c-promo-summary"),
    ("css selector", "p"),
]
