"""Base comum dos Page Objects de sites de notícias.

Implementa o fluxo "editoria → busca interna":

1. Se o site tem uma editoria mapeada para o `Topic`, abre a editoria
   e tenta extrair os cards de notícia.
2. Caso a editoria não exista, retorne 0 resultados ou levante uma
   exceção, cai no formulário de **busca interna** do site usando o
   rótulo do tema como query.

Cada Page Object subclasse precisa:
- Definir `name`, `domain` e `base_url`.
- Implementar `editorial_url(topic) -> str | None` e
  `search_url(topic) -> str`.
- Expor as listas de locators (`article_locators`, `title_locators`,
  `link_locators`, `time_locators`, `snippet_locators`).

Os artigos extraídos vêm como `NewsArticle` (Pydantic). Cards
inválidos (sem título ou sem URL absoluta) são descartados; cards
sem `published_at` parseável são mantidos com `published_at=None`.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, ClassVar
from urllib.parse import urljoin, urlparse

from src.models.news import NewsArticle
from src.models.topics import Topic, label_for
from src.pages.base_page import BasePage, Locator
from src.utils.date_filter import parse_date

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class BaseNewsPage(BasePage):
    """Base reaproveitável dos Page Objects de sites de notícias."""

    name: ClassVar[str] = ""
    domain: ClassVar[str] = ""
    base_url: ClassVar[str] = ""

    article_locators: ClassVar[list[Locator]] = []
    title_locators: ClassVar[list[Locator]] = []
    link_locators: ClassVar[list[Locator]] = []
    time_locators: ClassVar[list[Locator]] = []
    snippet_locators: ClassVar[list[Locator]] = []

    def editorial_url(self, topic: Topic) -> str | None:
        """URL da editoria do tema, se existir; `None` para cair na busca."""
        return None

    def search_url(self, topic: Topic) -> str:
        """URL da busca interna do site para o tema escolhido."""
        raise NotImplementedError

    def collect(self, topic: Topic, max_items: int) -> list[NewsArticle]:
        """Coleta notícias do tema usando editoria → busca interna."""
        articles: list[NewsArticle] = []

        edit_url = self.editorial_url(topic)
        if edit_url:
            try:
                articles = self._collect_from_url(
                    edit_url, topic, max_items, source="editoria"
                )
            except Exception as exc:
                self.logger.warning(
                    "%s: falha na editoria (%s) — caindo na busca interna.",
                    self.name,
                    exc,
                )

        if not articles:
            try:
                articles = self._collect_from_url(
                    self.search_url(topic),
                    topic,
                    max_items,
                    source="busca",
                )
            except Exception as exc:
                self.logger.error(
                    "%s: busca interna tambem falhou (%s).", self.name, exc
                )

        return articles

    def _collect_from_url(
        self,
        url: str,
        topic: Topic,
        max_items: int,
        *,
        source: str,
    ) -> list[NewsArticle]:
        """Abre `url`, faz scroll humanizado e extrai até `max_items` cards."""
        self.open(url)
        self.humanized_scroll(total_pixels=2400)

        cards = self.find_first(self.article_locators)
        self.logger.info(
            "%s [%s]: %d cards encontrados em %s",
            self.name,
            source,
            len(cards),
            url,
        )

        articles: list[NewsArticle] = []
        for card in cards:
            if len(articles) >= max_items:
                break
            article = self._extract_article(card, topic)
            if article is not None:
                articles.append(article)

        return articles

    def _extract_article(
        self,
        card: "WebElement",
        topic: Topic,
    ) -> NewsArticle | None:
        """Constrói um `NewsArticle` a partir do `card` (ou `None` se inválido)."""
        href = self._extract_href(card)
        if not href:
            return None

        title = self._first_text(card, self.title_locators, attr="aria-label")
        if not title or len(title.strip()) < 3:
            title = self._first_text(card, self.title_locators)
        if not title or len(title.strip()) < 3:
            return None

        absolute_url = self._absolutize(href)
        if not absolute_url.startswith("http"):
            return None

        published = self._extract_datetime(card)
        snippet = self._first_text(card, self.snippet_locators)

        try:
            return NewsArticle(
                title=title.strip(),
                url=absolute_url,
                source=self.name,
                topic=topic,
                published_at=published,
                snippet=(snippet or "")[:300],
            )
        except Exception as exc:
            self.logger.debug("%s: card descartado: %s", self.name, exc)
            return None

    def _extract_href(self, card: "WebElement") -> str:
        """Lê o primeiro `href` plausível dentre os locators de link."""
        for el in self.find_first_in(card, self.link_locators):
            href = self.safe_text(el, attribute="href")
            if href and not href.startswith(("javascript:", "#", "mailto:")):
                return href
        return ""

    def _extract_datetime(self, card: "WebElement") -> datetime | None:
        """Tenta extrair `published_at` do card via `<time datetime>` e texto."""
        elements = self.find_first_in(card, self.time_locators)
        for el in elements:
            iso = self.safe_text(el, attribute="datetime")
            if iso:
                parsed = parse_date(iso)
                if parsed is not None:
                    return _to_utc(parsed)
            text = self.safe_text(el)
            if text:
                parsed = parse_date(text)
                if parsed is not None:
                    return _to_utc(parsed)
        return None

    def _first_text(
        self,
        card: "WebElement",
        locators: list[Locator],
        *,
        attr: str | None = None,
    ) -> str:
        """Devolve o primeiro texto não-vazio entre os locators (atributo opcional)."""
        for loc in locators:
            els = self.find_first_in(card, [loc])
            for el in els:
                txt = self.safe_text(el, attribute=attr) if attr else self.safe_text(el)
                if txt:
                    return txt
        return ""

    def _absolutize(self, href: str) -> str:
        """Converte href relativo em URL absoluta usando `base_url` da classe."""
        if not href:
            return ""
        if href.startswith("http"):
            return href
        if href.startswith("//"):
            return f"https:{href}"
        return urljoin(self.base_url, href)

    @staticmethod
    def _matches_domain(url: str, domain: str) -> bool:
        """True se o host de `url` termina em `domain`."""
        host = (urlparse(url).hostname or "").lower()
        return host == domain or host.endswith(f".{domain}")


def _to_utc(dt: datetime) -> datetime:
    """Garante que o datetime tem timezone UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def label_for_query(topic: Topic) -> str:
    """Helper conveniente: rótulo do tema usado em URLs de busca interna."""
    return label_for(topic)
