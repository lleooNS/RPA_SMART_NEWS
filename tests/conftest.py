"""Fixtures comuns da suíte de testes."""

from __future__ import annotations

import logging
from collections.abc import Callable, Iterator
from typing import Any

import pytest


@pytest.fixture(autouse=True)
def _reset_logger() -> Iterator[None]:
    """Garante que o logger raiz da aplicação fica limpo entre os testes."""
    yield
    logging.getLogger("rpa_smart_news").handlers.clear()
    logging.getLogger().handlers.clear()


@pytest.fixture
def mock_inputs(monkeypatch: pytest.MonkeyPatch) -> Callable[..., None]:
    """Mocka `console.input` do menu com uma sequência de respostas."""

    def _apply(*responses: str) -> None:
        iterator = iter(responses)

        def _fake_input(*_args: Any, **_kwargs: Any) -> str:
            return next(iterator)

        monkeypatch.setattr("src.services.menu.console.input", _fake_input)

    return _apply


@pytest.fixture
def clear_settings_cache() -> Iterator[None]:
    """Limpa o cache do `get_settings` para isolar testes de config."""
    from src.utils.config import get_settings

    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
