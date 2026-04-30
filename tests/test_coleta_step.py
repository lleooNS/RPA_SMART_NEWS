"""Testes do `coletar_noticias`: itera sobre as páginas e tolera falhas."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any
from unittest.mock import MagicMock

import pytest

from src.models.news import NewsArticle
from src.models.topics import Topic
from src.pages.base_news_page import BaseNewsPage
from src.steps.coleta_step import coletar_noticias
from src.utils.config import Settings


@pytest.fixture
def settings() -> Settings:
    return Settings(_env_file=None, max_news_per_site=5)  # type: ignore[arg-type]


def _make_page_factory(name: str, articles: list[NewsArticle]) -> type[BaseNewsPage]:
    """Cria uma fábrica de página fake que devolve `articles` em `collect`."""

    class _FakePage(BaseNewsPage):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self.driver = args[0] if args else None
            self.settings = args[1] if len(args) > 1 else None
            self.name = name  # type: ignore[misc]
            self.logger = MagicMock()

        def collect(self, topic: Topic, max_items: int) -> list[NewsArticle]:
            return articles[:max_items]

    return _FakePage


def _make_failing_factory(name: str) -> type[BaseNewsPage]:
    """Cria uma fábrica cuja `collect` levanta exceção."""

    class _BrokenPage(BaseNewsPage):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self.name = name  # type: ignore[misc]
            self.logger = MagicMock()

        def collect(self, topic: Topic, max_items: int) -> list[NewsArticle]:
            raise RuntimeError(f"falha simulada em {name}")

    return _BrokenPage


def _article(*, source: str, url: str, days_ago: int | None = None) -> NewsArticle:
    """Helper: cria um NewsArticle válido para testes."""
    if days_ago is None:
        published = None
    else:
        published = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return NewsArticle(
        title=f"Manchete de {source}",
        url=url,
        source=source,
        topic=Topic.ECONOMIA,
        published_at=published,
    )


class TestColetarNoticias:
    """Cobertura do orquestrador de coleta."""

    def test_concatena_artigos_de_todas_as_fontes(
        self, settings: Settings
    ) -> None:
        f1 = _make_page_factory("G1", [_article(source="G1", url="https://g1.com/a")])
        f2 = _make_page_factory(
            "BBC", [_article(source="BBC", url="https://bbc.com/b")]
        )
        result = coletar_noticias(
            MagicMock(),
            Topic.ECONOMIA,
            settings=settings,
            page_factories=[f1, f2],
        )
        assert len(result) == 2
        sources = {a.source for a in result}
        assert sources == {"G1", "BBC"}

    def test_falha_em_uma_fonte_nao_interrompe_as_demais(
        self, settings: Settings
    ) -> None:
        broken = _make_failing_factory("Broken")
        ok = _make_page_factory("OK", [_article(source="OK", url="https://ok.com/x")])
        result = coletar_noticias(
            MagicMock(),
            Topic.ECONOMIA,
            settings=settings,
            page_factories=[broken, ok],
        )
        assert len(result) == 1
        assert result[0].source == "OK"

    def test_lista_vazia_quando_nada_coletado(
        self, settings: Settings
    ) -> None:
        empty = _make_page_factory("Vazio", [])
        result = coletar_noticias(
            MagicMock(),
            Topic.ECONOMIA,
            settings=settings,
            page_factories=[empty],
        )
        assert result == []

    def test_ordena_por_published_at_decrescente(
        self, settings: Settings
    ) -> None:
        recente = _article(source="Stub", url="https://a.com/1", days_ago=0)
        antiga = _article(source="Stub", url="https://a.com/2", days_ago=5)
        sem_data = _article(source="Stub", url="https://a.com/3", days_ago=None)
        f = _make_page_factory("Stub", [antiga, sem_data, recente])
        result = coletar_noticias(
            MagicMock(),
            Topic.ECONOMIA,
            settings=settings,
            page_factories=[f],
        )
        assert [str(a.url) for a in result[:2]] == [
            "https://a.com/1",
            "https://a.com/2",
        ]
        assert str(result[2].url) == "https://a.com/3"

    def test_respeita_max_news_per_site(self, settings: Settings) -> None:
        articles = [
            _article(source="Stub", url=f"https://a.com/{i}") for i in range(10)
        ]
        f = _make_page_factory("Stub", articles)
        result = coletar_noticias(
            MagicMock(),
            Topic.ECONOMIA,
            settings=settings,
            page_factories=[f],
        )
        assert len(result) == settings.max_news_per_site
