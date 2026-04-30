"""Page Object da BBC News Brasil (`bbc.com/portuguese`)."""

from __future__ import annotations

from src.locators import bbc_brasil_locators as L
from src.models.topics import Topic, label_for
from src.pages.base_news_page import BaseNewsPage


class BBCBrasilPage(BaseNewsPage):
    """Coleta na BBC News Brasil: usa apenas a busca interna.

    A BBC indexa o conteúdo em pt-BR atrás de uma busca, sem páginas de
    editoria estáveis para os 10 temas. A busca é robusta e cobre todos
    eles com qualidade razoável.
    """

    name = "BBC News Brasil"
    domain = "bbc.com"
    base_url = L.BASE_URL

    article_locators = L.ARTICLE_LOCATORS
    title_locators = L.TITLE_LOCATORS
    link_locators = L.LINK_LOCATORS
    time_locators = L.TIME_LOCATORS
    snippet_locators = L.SNIPPET_LOCATORS

    def editorial_url(self, topic: Topic) -> str | None:
        """A BBC News Brasil sempre cai na busca interna."""
        return None

    def search_url(self, topic: Topic) -> str:
        """Busca interna da BBC News Brasil."""
        return L.search_url(label_for(topic))
