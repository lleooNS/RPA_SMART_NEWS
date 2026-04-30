"""Page Object do R7 (`r7.com`)."""

from __future__ import annotations

from src.locators import r7_locators as L
from src.models.topics import Topic, label_for
from src.pages.base_news_page import BaseNewsPage


class R7Page(BaseNewsPage):
    """Coleta no R7: editoria mapeada por tema → busca interna."""

    name = "R7"
    domain = "r7.com"
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
        """Busca interna do R7."""
        return L.search_url(label_for(topic))
