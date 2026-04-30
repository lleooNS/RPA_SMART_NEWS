"""Testes do `summarize` (B-012, versão simples)."""

from __future__ import annotations

from datetime import datetime, timezone

from src.genai.prompts import build_summary_prompt
from src.genai.summarizer import summarize
from src.models.news import NewsArticle
from src.models.topics import Topic
from src.utils.config import Settings


class _RecorderClient:
    """LLM stub que registra a chamada e devolve um texto fixo."""

    name = "recorder"

    def __init__(self, response: str = "- a\n- b\n- c\nTexto final.") -> None:
        self.response = response
        self.last_system: str | None = None
        self.last_prompt: str | None = None

    def complete(
        self,
        *,
        system: str,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 800,
    ) -> str:
        self.last_system = system
        self.last_prompt = prompt
        return self.response


def _articles() -> list[NewsArticle]:
    return [
        NewsArticle(
            title="Selic mantida em 10,75%",
            url="https://exemplo.com/1",
            source="G1",
            topic=Topic.ECONOMIA,
            published_at=datetime(2026, 4, 30, tzinfo=timezone.utc),
        ),
        NewsArticle(
            title="Dólar fecha em alta",
            url="https://exemplo.com/2",
            source="BBC",
            topic=Topic.ECONOMIA,
        ),
    ]


def _settings() -> Settings:
    return Settings(_env_file=None, llm_provider="stub")  # type: ignore[arg-type]


class TestBuildSummaryPrompt:
    def test_inclui_tema_e_manchetes(self) -> None:
        prompt = build_summary_prompt(_articles(), Topic.ECONOMIA)
        assert "Economia" in prompt
        assert "Selic" in prompt
        assert "Dólar" in prompt

    def test_lista_vazia_inclui_marcador(self) -> None:
        prompt = build_summary_prompt([], Topic.ECONOMIA)
        assert "(nenhuma notícia coletada)" in prompt


class TestSummarize:
    def test_usa_o_client_passado(self) -> None:
        client = _RecorderClient()
        summary = summarize(
            _articles(), Topic.ECONOMIA,
            settings=_settings(),
            client=client,
        )
        assert summary.metadata["llm_provider"] == "recorder"
        assert summary.metadata["articles_total"] == 2
        assert summary.bullets == ["a", "b", "c"]
        assert client.last_system is not None
        assert client.last_prompt is not None

    def test_inclui_sources(self) -> None:
        client = _RecorderClient()
        summary = summarize(
            _articles(), Topic.ECONOMIA,
            settings=_settings(),
            client=client,
        )
        assert len(summary.sources) == 2
        assert summary.sources[0].source == "G1"
