"""Testes da `BaseNewsPage`: estratégia editoria → busca interna."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from src.models.news import NewsArticle
from src.models.topics import Topic
from src.pages.base_news_page import BaseNewsPage
from src.pages.base_page import Locator
from src.utils.config import Settings


@pytest.fixture
def settings() -> Settings:
    """Settings rápidos (delays mínimos) para acelerar os testes."""
    return Settings(
        _env_file=None,  # type: ignore[arg-type]
        humanize_delay_min=0.0,
        humanize_delay_max=0.0,
        selenium_timeout=0.5,
    )


def _fake_card(
    *,
    href: str = "https://exemplo.com/noticia/1",
    title: str = "Manchete teste",
    iso_datetime: str | None = "2026-04-30T10:00:00+00:00",
    snippet: str = "",
) -> MagicMock:
    """Cria um card mockado que devolve elementos com os textos esperados."""
    link_el = MagicMock(name="link")
    link_el.text = title
    link_el.get_attribute.side_effect = lambda attr: {
        "href": href,
        "aria-label": title,
        "datetime": "",
    }.get(attr, "")

    title_el = MagicMock(name="title")
    title_el.text = title
    title_el.get_attribute.return_value = ""

    time_el = MagicMock(name="time")
    time_el.text = ""
    time_el.get_attribute.side_effect = lambda attr: (
        iso_datetime if attr == "datetime" else ""
    )

    snippet_el = MagicMock(name="snippet")
    snippet_el.text = snippet
    snippet_el.get_attribute.return_value = ""

    card = MagicMock(name="card")

    def _find(by: str, value: str) -> list[MagicMock]:
        if "a[href" in value or value == "a":
            return [link_el]
        if value in {"h2", "h3"} or "headline" in value or "titulo" in value:
            return [title_el]
        if value == "time" or "datetime" in value:
            return [time_el]
        if "snippet" in value or value == "p" or "resumo" in value:
            return [snippet_el]
        return []

    card.find_elements.side_effect = _find
    return card


class _FakeNewsPage(BaseNewsPage):
    """Subclasse mínima para testar o fluxo da `BaseNewsPage`."""

    name = "Fake"
    domain = "exemplo.com"
    base_url = "https://exemplo.com"

    article_locators: list[Locator] = [("css selector", "article")]
    title_locators: list[Locator] = [("css selector", "h2")]
    link_locators: list[Locator] = [("css selector", "a[href]")]
    time_locators: list[Locator] = [("css selector", "time")]
    snippet_locators: list[Locator] = [("css selector", "p")]

    def __init__(self, *args: Any, editoria: str | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._editoria = editoria

    def editorial_url(self, topic: Topic) -> str | None:
        return self._editoria

    def search_url(self, topic: Topic) -> str:
        return f"{self.base_url}/busca?q={topic.name.lower()}"


class TestEditorialFallback:
    """Editoria primeiro; busca interna como fallback."""

    def test_usa_editoria_quando_retorna_artigos(
        self, settings: Settings
    ) -> None:
        driver = MagicMock(name="WebDriver")
        driver.find_elements.return_value = [_fake_card()]
        page = _FakeNewsPage(
            driver, settings, editoria="https://exemplo.com/economia/"
        )
        result = page.collect(Topic.ECONOMIA, max_items=5)
        assert len(result) == 1
        assert result[0].source == "Fake"
        # Apenas a editoria foi aberta
        urls = [call.args[0] for call in driver.get.call_args_list]
        assert urls == ["https://exemplo.com/economia/"]

    def test_cai_na_busca_quando_editoria_vazia(
        self, settings: Settings
    ) -> None:
        driver = MagicMock(name="WebDriver")
        driver.find_elements.side_effect = [
            [], [_fake_card()],
        ]
        page = _FakeNewsPage(
            driver, settings, editoria="https://exemplo.com/economia/"
        )
        result = page.collect(Topic.ECONOMIA, max_items=5)
        assert len(result) == 1
        urls = [call.args[0] for call in driver.get.call_args_list]
        assert urls[0] == "https://exemplo.com/economia/"
        assert "busca" in urls[1]

    def test_pula_editoria_quando_inexistente(
        self, settings: Settings
    ) -> None:
        driver = MagicMock(name="WebDriver")
        driver.find_elements.return_value = [_fake_card()]
        page = _FakeNewsPage(driver, settings, editoria=None)
        page.collect(Topic.SAUDE, max_items=5)
        urls = [call.args[0] for call in driver.get.call_args_list]
        assert len(urls) == 1
        assert "busca" in urls[0]


class TestArticleExtraction:
    """Extração de campos a partir do card."""

    def test_descarta_card_sem_titulo(self, settings: Settings) -> None:
        driver = MagicMock(name="WebDriver")
        card = _fake_card(title="ab")
        driver.find_elements.return_value = [card]
        page = _FakeNewsPage(driver, settings, editoria=None)
        result = page.collect(Topic.ECONOMIA, max_items=5)
        assert result == []

    def test_descarta_card_sem_url(self, settings: Settings) -> None:
        driver = MagicMock(name="WebDriver")
        card = _fake_card(href="javascript:void(0)")
        driver.find_elements.return_value = [card]
        page = _FakeNewsPage(driver, settings, editoria=None)
        result = page.collect(Topic.ECONOMIA, max_items=5)
        assert result == []

    def test_absolutiza_href_relativo(self, settings: Settings) -> None:
        driver = MagicMock(name="WebDriver")
        driver.find_elements.return_value = [
            _fake_card(href="/economia/2026/manchete.ghtml")
        ]
        page = _FakeNewsPage(driver, settings, editoria=None)
        result = page.collect(Topic.ECONOMIA, max_items=5)
        assert len(result) == 1
        assert str(result[0].url).startswith("https://exemplo.com/")

    def test_respeita_max_items(self, settings: Settings) -> None:
        driver = MagicMock(name="WebDriver")
        driver.find_elements.return_value = [
            _fake_card(href=f"https://exemplo.com/n/{i}") for i in range(10)
        ]
        page = _FakeNewsPage(driver, settings, editoria=None)
        result = page.collect(Topic.ECONOMIA, max_items=3)
        assert len(result) == 3

    def test_articles_sao_news_articles_pydantic(
        self, settings: Settings
    ) -> None:
        driver = MagicMock(name="WebDriver")
        driver.find_elements.return_value = [_fake_card()]
        page = _FakeNewsPage(driver, settings, editoria=None)
        result = page.collect(Topic.ECONOMIA, max_items=5)
        assert all(isinstance(a, NewsArticle) for a in result)
        assert result[0].published_at is not None
