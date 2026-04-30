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
        assert s.max_days == 10
        assert s.max_retries == 3
        assert s.output_dir.name == "output"


class TestSettingsValidacao:
    """Validação dos campos do `Settings`."""

    @pytest.mark.parametrize("max_days_invalido", [0, -1, 11, 100])
    def test_max_days_fora_do_intervalo(self, max_days_invalido: int) -> None:
        with pytest.raises(ValidationError):
            _build_settings(max_days=max_days_invalido)

    @pytest.mark.parametrize("max_retries_invalido", [0, -1, -10])
    def test_max_retries_invalido(self, max_retries_invalido: int) -> None:
        with pytest.raises(ValidationError):
            _build_settings(max_retries=max_retries_invalido)

    def test_max_days_nos_limites(self) -> None:
        assert _build_settings(max_days=1).max_days == 1
        assert _build_settings(max_days=10).max_days == 10


class TestGetSettings:
    """Cobertura do singleton `get_settings`."""

    def test_retorna_singleton(self, clear_settings_cache: None) -> None:
        a = get_settings()
        b = get_settings()
        assert a is b
