"""Testes do modelo Pydantic `UserInput`."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.models.topics import Topic
from src.models.user_input import UserInput


class TestUserInputValido:
    """Cenários de input válido."""

    def test_cria_com_valores_validos(self) -> None:
        ui = UserInput(topic=3)
        assert ui.topic is Topic.ESPORTES

    def test_topic_label_property(self) -> None:
        ui = UserInput(topic=1)
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
        ui = UserInput(topic=topic_id)
        assert ui.topic_label == label


class TestUserInputInvalido:
    """Cenários de input inválido — devem levantar `ValidationError`."""

    @pytest.mark.parametrize("topic_invalido", [0, -1, 11, 99])
    def test_topic_fora_do_range(self, topic_invalido: int) -> None:
        with pytest.raises(ValidationError):
            UserInput(topic=topic_invalido)

    def test_topic_nao_inteiro_levanta_erro(self) -> None:
        with pytest.raises(ValidationError):
            UserInput(topic="abc")  # type: ignore[arg-type]


class TestUserInputFrozen:
    """Garante que o modelo é imutável (`frozen=True`)."""

    def test_assignment_em_topic_falha(self) -> None:
        ui = UserInput(topic=1)
        with pytest.raises(ValidationError):
            ui.topic = Topic.POLITICA  # type: ignore[misc]
