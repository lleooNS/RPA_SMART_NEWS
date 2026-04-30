"""Modelo Pydantic da sumarização consolidada (versão R1)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from src.models.topics import Topic


class SourceRef(BaseModel):
    """Referência simplificada de uma fonte usada no resumo."""

    model_config = ConfigDict(frozen=True)

    title: str = Field(min_length=1)
    url: HttpUrl
    source: str = Field(min_length=1)


class Summary(BaseModel):
    """Resultado da sumarização aplicada ao conjunto de notícias."""

    model_config = ConfigDict(frozen=True)

    topic: Topic
    generated_at: datetime
    executive_summary: str = Field(min_length=1)
    bullets: list[str] = Field(default_factory=list)
    sources: list[SourceRef] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
