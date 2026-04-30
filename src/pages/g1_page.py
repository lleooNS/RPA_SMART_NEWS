"""Page Object do G1 (`g1.globo.com`)."""

from __future__ import annotations

from src.locators import g1_locators as L
from src.models.topics import Topic, label_for
from src.pages.base_news_page import BaseNewsPage


class G1Page(BaseNewsPage):
    """Coleta no G1: editoria mapeada por tema → busca interna."""

    name = "G1"
    domain = "g1.globo.com"
    base_url = L.BASE_URL

    article_locators = L.ARTICLE_LOCATORS
    title_locators = L.TITLE_LOCATORS
    link_locators = L.LINK_LOCATORS
    time_locators = L.TIME_LOCATORS
    snippet_locators = L.SNIPPET_LOCATORS

    def editorial_url(self, topic: Topic) -> str | None:
        """Combina `BASE_URL` + path mapeado, ou `None` se o tema não tem editoria."""
        path = L.EDITORIAL_PATHS.get(topic)
        if not path:
            return None
        return f"{self.base_url}{path}"

    def search_url(self, topic: Topic) -> str:
        """Busca interna do G1 com o rótulo do tema."""
        return L.search_url(label_for(topic))
