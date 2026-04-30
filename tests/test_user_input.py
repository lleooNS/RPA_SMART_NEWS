"""Testes do modelo Pydantic `UserInput`."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.models.topics import Topic
from src.models.user_input import UserInput


class TestUserInputValido:
    """Cenários de input válido."""

    def test_cria_com_valores_validos(self) -> None:
        ui = UserInput(topic=3, days=5)
        assert ui.topic is Topic.ESPORTES
        assert ui.days == 5

    def test_topic_label_property(self) -> None:
        ui = UserInput(topic=1, days=1)
        assert ui.topic_label == "Economia"

    @pytest.mark.parametrize(
        ("topic_id", "label"),
        [
            (1, "Economia"),
            (5, "Saúde"),
            (9, "Crimes/Segurança"),
            (10, "Cotidiano"),
        ],
    )
    def test_topic_label_para_cada_tema(
        self, topic_id: int, label: str
    ) -> None:
        ui = UserInput(topic=topic_id, days=1)
        assert ui.topic_label == label

    @pytest.mark.parametrize("days", [1, 5, 10])
    def test_dias_no_intervalo_aceitos(self, days: int) -> None:
        ui = UserInput(topic=1, days=days)
        assert ui.days == days


class TestUserInputInvalido:
    """Cenários de input inválido — devem levantar `ValidationError`."""

    @pytest.mark.parametrize("topic_invalido", [0, -1, 11, 99])
    def test_topic_fora_do_range(self, topic_invalido: int) -> None:
        with pytest.raises(ValidationError):
            UserInput(topic=topic_invalido, days=5)

    @pytest.mark.parametrize("days_invalido", [0, -1, 11, 100])
    def test_days_fora_do_range(self, days_invalido: int) -> None:
        with pytest.raises(ValidationError):
            UserInput(topic=1, days=days_invalido)

    def test_topic_nao_inteiro_levanta_erro(self) -> None:
        with pytest.raises(ValidationError):
            UserInput(topic="abc", days=5)  # type: ignore[arg-type]

    def test_days_nao_inteiro_levanta_erro(self) -> None:
        with pytest.raises(ValidationError):
            UserInput(topic=1, days="cinco")  # type: ignore[arg-type]


class TestUserInputFrozen:
    """Garante que o modelo é imutável (`frozen=True`)."""

    def test_assignment_em_topic_falha(self) -> None:
        ui = UserInput(topic=1, days=1)
        with pytest.raises(ValidationError):
            ui.topic = Topic.POLITICA  # type: ignore[misc]

    def test_assignment_em_days_falha(self) -> None:
        ui = UserInput(topic=1, days=1)
        with pytest.raises(ValidationError):
            ui.days = 7  # type: ignore[misc]
