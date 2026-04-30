"""Modelo Pydantic da notícia coletada."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from src.models.topics import Topic


class NewsArticle(BaseModel):
    """Notícia coletada de um dos sites de origem."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    title: str = Field(min_length=3, description="Título da notícia.")
    url: HttpUrl = Field(description="URL canônica da notícia.")
    source: str = Field(min_length=2, description="Nome do site de origem.")
    topic: Topic = Field(description="Tema escolhido pelo usuário.")
    published_at: datetime | None = Field(
        default=None,
        description="Data/hora de publicação (None se não pôde ser parseada).",
    )
    snippet: str = Field(
        default="",
        description="Trecho/lead curto da notícia, quando disponível.",
    )
