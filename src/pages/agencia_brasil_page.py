"""Page Object da Agência Brasil (`agenciabrasil.ebc.com.br`)."""

from __future__ import annotations

from src.locators import agencia_brasil_locators as L
from src.models.topics import Topic, label_for
from src.pages.base_news_page import BaseNewsPage


class AgenciaBrasilPage(BaseNewsPage):
    """Coleta na Agência Brasil: editoria mapeada por tema → busca interna."""

    name = "Agência Brasil"
    domain = "agenciabrasil.ebc.com.br"
    base_url = L.BASE_URL

    article_locators = L.ARTICLE_LOCATORS
    title_locators = L.TITLE_LOCATORS
    link_locators = L.LINK_LOCATORS
    time_locators = L.TIME_LOCATORS
    snippet_locators = L.SNIPPET_LOCATORS

    def editorial_url(self, topic: Topic) -> str | None:
        """Combina `BASE_URL` + path mapeado, ou `None` para cair na busca."""
        path = L.EDITORIAL_PATHS.get(topic)
        if not path:
            return None
        return f"{self.base_url}{path}"

    def search_url(self, topic: Topic) -> str:
        """Busca interna da Agência Brasil."""
        return L.search_url(label_for(topic))
