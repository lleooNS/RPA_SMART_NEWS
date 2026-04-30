"""Testes das configurações via Pydantic Settings."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.utils.config import Settings, get_settings


def _build_settings(**overrides: object) -> Settings:
    """Helper: cria `Settings` ignorando o `.env` da raiz."""
    return Settings(_env_file=None, **overrides)  # type: ignore[arg-type]


class TestSettingsDefaults:
    """Valores padrão quando nenhum override é passado."""

    def test_defaults(self) -> None:
        s = _build_settings()
        assert s.log_level == "INFO"
        assert s.max_retries == 3
        assert s.output_dir.name == "output"
        assert s.max_news_per_site == 15
        assert s.headless is False


class TestSettingsValidacao:
    """Validação dos campos do `Settings`."""

    @pytest.mark.parametrize("max_retries_invalido", [0, -1, -10])
    def test_max_retries_invalido(self, max_retries_invalido: int) -> None:
        with pytest.raises(ValidationError):
            _build_settings(max_retries=max_retries_invalido)

    @pytest.mark.parametrize("max_news_invalido", [0, -1, 999])
    def test_max_news_per_site_fora_do_intervalo(
        self, max_news_invalido: int
    ) -> None:
        with pytest.raises(ValidationError):
            _build_settings(max_news_per_site=max_news_invalido)

    def test_humanize_max_menor_que_min_falha(self) -> None:
        with pytest.raises(ValidationError):
            _build_settings(humanize_delay_min=2.0, humanize_delay_max=1.0)


class TestGetSettings:
    """Cobertura do singleton `get_settings`."""

    def test_retorna_singleton(self, clear_settings_cache: None) -> None:
        a = get_settings()
        b = get_settings()
        assert a is b
