"""Lista canônica dos 10 temas suportados pelo MVP."""

from enum import IntEnum


class Topic(IntEnum):
    """Tema de notícia suportado, mapeado por ID `1–10`."""

    ECONOMIA = 1
    POLITICA = 2
    ESPORTES = 3
    EVENTOS_GLOBAIS = 4
    SAUDE = 5
    TECNOLOGIA = 6
    ENTRETENIMENTO = 7
    CLIMA = 8
    CRIMES_SEGURANCA = 9
    COTIDIANO = 10


TOPIC_LABELS: dict[Topic, str] = {
    Topic.ECONOMIA: "Economia",
    Topic.POLITICA: "Política",
    Topic.ESPORTES: "Esportes",
    Topic.EVENTOS_GLOBAIS: "Eventos globais",
    Topic.SAUDE: "Saúde",
    Topic.TECNOLOGIA: "Tecnologia",
    Topic.ENTRETENIMENTO: "Entretenimento",
    Topic.CLIMA: "Clima",
    Topic.CRIMES_SEGURANCA: "Crimes/Segurança",
    Topic.COTIDIANO: "Cotidiano",
}


def label_for(topic: Topic) -> str:
    """Retorna o rótulo legível em pt-BR para o tema informado."""
    return TOPIC_LABELS[topic]
