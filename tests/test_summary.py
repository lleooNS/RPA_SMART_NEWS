"""Testes dos modelos `Summary` e `SourceRef`."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from src.models.summary import SourceRef, Summary
from src.models.topics import Topic


class TestSourceRef:
    def test_constroi(self) -> None:
        ref = SourceRef(
            title="X",
            url="https://x.com/a",
            source="G1",
        )
        assert ref.title == "X"
        assert ref.source == "G1"


class TestSummary:
    def _summary(self, **overrides: object) -> Summary:
        defaults: dict[str, object] = dict(
            topic=Topic.ECONOMIA,
            generated_at=datetime(2026, 4, 30, 12, 0, tzinfo=timezone.utc),
            executive_summary="resumo",
            bullets=["x", "y"],
            sources=[],
            metadata={"llm_provider": "stub"},
        )
        defaults.update(overrides)
        return Summary(**defaults)  # type: ignore[arg-type]

    def test_constroi_com_metadata(self) -> None:
        summary = self._summary()
        assert summary.bullets == ["x", "y"]
        assert summary.metadata["llm_provider"] == "stub"

    def test_executive_summary_vazio_falha(self) -> None:
        with pytest.raises(ValidationError):
            self._summary(executive_summary="")

    def test_topic_obrigatorio(self) -> None:
        with pytest.raises(ValidationError):
            Summary(  # type: ignore[call-arg]
                generated_at=datetime.now(timezone.utc),
                executive_summary="resumo",
            )
