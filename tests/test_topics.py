"""Testes da enumeração `Topic` e do mapeamento de rótulos."""

from __future__ import annotations

import pytest

from src.models.topics import TOPIC_LABELS, Topic, label_for


class TestTopic:
    """Cobertura da `IntEnum` `Topic`."""

    def test_quantidade_de_temas(self) -> None:
        assert len(Topic) == 10

    def test_valores_de_1_a_10(self) -> None:
        valores = sorted(t.value for t in Topic)
        assert valores == list(range(1, 11))

    @pytest.mark.parametrize(
        ("topic_id", "esperado"),
        [
            (1, Topic.ECONOMIA),
            (2, Topic.POLITICA),
            (3, Topic.ESPORTES),
            (10, Topic.COTIDIANO),
        ],
    )
    def test_acesso_por_id(self, topic_id: int, esperado: Topic) -> None:
        assert Topic(topic_id) is esperado

    @pytest.mark.parametrize("invalido", [0, -1, 11, 99])
    def test_id_invalido_levanta_value_error(self, invalido: int) -> None:
        with pytest.raises(ValueError):
            Topic(invalido)


class TestTopicLabels:
    """Cobertura do dicionário `TOPIC_LABELS`."""

    def test_todos_os_temas_tem_label(self) -> None:
        assert all(t in TOPIC_LABELS for t in Topic)

    def test_labels_em_pt_br(self) -> None:
        assert TOPIC_LABELS[Topic.SAUDE] == "Saúde"
        assert TOPIC_LABELS[Topic.CRIMES_SEGURANCA] == "Crimes/Segurança"
        assert TOPIC_LABELS[Topic.EVENTOS_GLOBAIS] == "Eventos globais"

    def test_labels_nao_vazias(self) -> None:
        for label in TOPIC_LABELS.values():
            assert label.strip() != ""


class TestLabelFor:
    """Cobertura da função `label_for`."""

    @pytest.mark.parametrize(
        ("topic", "esperado"),
        [
            (Topic.ECONOMIA, "Economia"),
            (Topic.TECNOLOGIA, "Tecnologia"),
            (Topic.COTIDIANO, "Cotidiano"),
        ],
    )
    def test_retorna_rotulo_correto(self, topic: Topic, esperado: str) -> None:
        assert label_for(topic) == esperado
