"""Testes do serviço de menu CLI."""

from __future__ import annotations

from collections.abc import Callable

import pytest
from pydantic import ValidationError

from src.models.topics import Topic
from src.models.user_input import UserInput
from src.services.menu import (
    MenuAbortedError,
    _format_validation_error,
    _parse_int,
    collect_user_input,
    display_topics,
)


class TestParseInt:
    """Cobertura do helper `_parse_int`."""

    @pytest.mark.parametrize(("valor", "esperado"), [("5", 5), ("10", 10), ("1", 1)])
    def test_converte_inteiro_valido(self, valor: str, esperado: int) -> None:
        assert _parse_int(valor, field="dias") == esperado

    @pytest.mark.parametrize("invalido", ["abc", "", "1.5", " ", "9-"])
    def test_levanta_value_error_em_invalido(self, invalido: str) -> None:
        with pytest.raises(ValueError) as exc_info:
            _parse_int(invalido, field="tema")
        assert "tema" in str(exc_info.value)


class TestFormatValidationError:
    """Cobertura do helper `_format_validation_error`."""

    def test_formata_mensagem_de_erro(self) -> None:
        try:
            UserInput(topic=99, days=5)
        except ValidationError as exc:
            msg = _format_validation_error(exc)
            assert isinstance(msg, str)
            assert "topic" in msg
        else:  # pragma: no cover
            pytest.fail("ValidationError esperado")

    def test_formata_multiplos_erros(self) -> None:
        try:
            UserInput(topic=99, days=99)
        except ValidationError as exc:
            msg = _format_validation_error(exc)
            assert "topic" in msg
            assert "days" in msg
            assert "|" in msg


class TestDisplayTopics:
    """Cobertura de `display_topics`."""

    def test_executa_sem_erro(self) -> None:
        display_topics()


class TestCollectUserInput:
    """Cobertura de `collect_user_input` com inputs mockados."""

    def test_input_valido_retorna_user_input(
        self, mock_inputs: Callable[..., None]
    ) -> None:
        mock_inputs("3", "5")
        ui = collect_user_input(max_retries=3, max_days=10)
        assert ui.topic is Topic.ESPORTES
        assert ui.days == 5

    def test_retry_apos_input_nao_numerico(
        self, mock_inputs: Callable[..., None]
    ) -> None:
        mock_inputs("abc", "5", "3", "5")
        ui = collect_user_input(max_retries=3, max_days=10)
        assert ui.topic is Topic.ESPORTES
        assert ui.days == 5

    def test_retry_apos_topic_fora_do_range(
        self, mock_inputs: Callable[..., None]
    ) -> None:
        mock_inputs("99", "5", "1", "5")
        ui = collect_user_input(max_retries=3, max_days=10)
        assert ui.topic is Topic.ECONOMIA

    def test_retry_apos_days_fora_do_range(
        self, mock_inputs: Callable[..., None]
    ) -> None:
        mock_inputs("3", "99", "3", "5")
        ui = collect_user_input(max_retries=3, max_days=10)
        assert ui.days == 5

    def test_aborta_apos_max_retries(
        self, mock_inputs: Callable[..., None]
    ) -> None:
        mock_inputs("abc", "5", "abc", "5", "abc", "5")
        with pytest.raises(MenuAbortedError) as exc_info:
            collect_user_input(max_retries=3, max_days=10)
        assert "3" in str(exc_info.value)

    def test_unica_tentativa_pode_ser_configurada(
        self, mock_inputs: Callable[..., None]
    ) -> None:
        mock_inputs("abc", "5")
        with pytest.raises(MenuAbortedError):
            collect_user_input(max_retries=1, max_days=10)
