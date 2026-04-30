"""Testes do modelo `NewsArticle`."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from src.models.news import NewsArticle
from src.models.topics import Topic


class TestNewsArticle:
    """Validação Pydantic + frozen + tipos."""

    def test_constroi_artigo_minimo(self) -> None:
        article = NewsArticle(
            title="Teste de manchete",
            url="https://exemplo.com/x",
            source="G1",
            topic=Topic.ECONOMIA,
        )
        assert article.title == "Teste de manchete"
        assert str(article.url).startswith("https://exemplo.com/x")
        assert article.source == "G1"
        assert article.topic is Topic.ECONOMIA
        assert article.published_at is None
        assert article.snippet == ""

    def test_armazena_data_quando_fornecida(self) -> None:
        when = datetime(2026, 4, 30, tzinfo=timezone.utc)
        article = NewsArticle(
            title="Outra",
            url="https://exemplo.com/y",
            source="BBC",
            topic=Topic.SAUDE,
            published_at=when,
        )
        assert article.published_at == when

    def test_titulo_curto_invalido(self) -> None:
        with pytest.raises(ValidationError):
            NewsArticle(
                title="oi",
                url="https://exemplo.com",
                source="G1",
                topic=Topic.ECONOMIA,
            )

    def test_url_invalida(self) -> None:
        with pytest.raises(ValidationError):
            NewsArticle(
                title="Manchete válida",
                url="nao-eh-url",
                source="G1",
                topic=Topic.ECONOMIA,
            )

    def test_frozen_imutavel(self) -> None:
        article = NewsArticle(
            title="Manchete válida",
            url="https://exemplo.com",
            source="G1",
            topic=Topic.ECONOMIA,
        )
        with pytest.raises(ValidationError):
            article.title = "outra coisa"  # type: ignore[misc]
