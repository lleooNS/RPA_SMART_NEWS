"""Testes da deduplicação por URL canônica e título normalizado."""

from __future__ import annotations

from src.models.news import NewsArticle
from src.models.topics import Topic
from src.utils.dedupe import dedupe, normalize_title, normalize_url


class TestNormalizeUrl:
    def test_remove_querystring_e_fragmento(self) -> None:
        assert normalize_url("https://x.com/a/?utm=1#abc") == "https://x.com/a"

    def test_remove_barra_final(self) -> None:
        assert normalize_url("https://x.com/a/b/") == "https://x.com/a/b"

    def test_lowercase_no_host(self) -> None:
        assert normalize_url("https://X.COM/a") == "https://x.com/a"


class TestNormalizeTitle:
    def test_remove_acentos_e_pontuacao(self) -> None:
        assert (
            normalize_title("Política & Economia: análise!")
            == "politica economia analise"
        )

    def test_collapsa_espacos(self) -> None:
        assert normalize_title("  a   b  c ") == "a b c"


def _article(title: str, url: str) -> NewsArticle:
    return NewsArticle(
        title=title,
        url=url,
        source="Stub",
        topic=Topic.ECONOMIA,
    )


class TestDedupe:
    def test_remove_url_duplicada(self) -> None:
        articles = [
            _article("AAA primeira", "https://x.com/a"),
            _article("BBB outra", "https://x.com/a/?utm=1"),
        ]
        result = dedupe(articles)
        assert len(result) == 1
        assert result[0].title == "AAA primeira"

    def test_remove_titulo_duplicado(self) -> None:
        articles = [
            _article("Mesma manchete!", "https://x.com/a"),
            _article("MESMA MANCHETE", "https://y.com/b"),
        ]
        result = dedupe(articles)
        assert len(result) == 1

    def test_mantem_distintos(self) -> None:
        articles = [
            _article("Manchete um", "https://x.com/1"),
            _article("Manchete dois", "https://x.com/2"),
            _article("Manchete três", "https://x.com/3"),
        ]
        result = dedupe(articles)
        assert len(result) == 3
