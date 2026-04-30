"""Testes do logger central da aplicação."""

from __future__ import annotations

import logging

import pytest

from src.utils.logger import LOGGER_NAME, get_logger, setup_logger


class TestSetupLogger:
    """Cobertura de `setup_logger`."""

    def test_retorna_logger_nomeado(self) -> None:
        logger = setup_logger("INFO")
        assert isinstance(logger, logging.Logger)
        assert logger.name == LOGGER_NAME

    @pytest.mark.parametrize(
        ("nivel", "esperado"),
        [
            ("DEBUG", logging.DEBUG),
            ("INFO", logging.INFO),
            ("WARNING", logging.WARNING),
            ("ERROR", logging.ERROR),
        ],
    )
    def test_define_nivel_no_root(self, nivel: str, esperado: int) -> None:
        setup_logger(nivel)
        assert logging.getLogger().level == esperado

    def test_aceita_nivel_em_minusculas(self) -> None:
        setup_logger("info")
        assert logging.getLogger().level == logging.INFO


class TestGetLogger:
    """Cobertura de `get_logger`."""

    def test_retorna_mesma_instancia(self) -> None:
        setup_logger("INFO")
        a = get_logger()
        b = get_logger()
        assert a is b
        assert a.name == LOGGER_NAME
