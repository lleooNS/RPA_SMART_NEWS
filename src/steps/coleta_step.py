"""Step de coleta: itera sobre os Page Objects das 4 fontes fixas.

Cada Page Object aplica a estratégia "editoria → busca interna"
internamente (`BaseNewsPage.collect`). Falha em um site é logada e
não interrompe os demais.

Ao final, as notícias com `published_at` parseado vão **antes** das
sem data, e dentro de cada grupo a ordem é por data decrescente
(mais recentes primeiro).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from src.models.news import NewsArticle
from src.models.topics import Topic, label_for
from src.pages.agencia_brasil_page import AgenciaBrasilPage
from src.pages.base_news_page import BaseNewsPage
from src.pages.bbc_brasil_page import BBCBrasilPage
from src.pages.g1_page import G1Page
from src.pages.r7_page import R7Page
from src.utils.config import Settings, get_settings
from src.utils.logger import get_logger

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver

logger = get_logger()

_DEFAULT_PAGE_FACTORIES: list[type[BaseNewsPage]] = [
    G1Page,
    BBCBrasilPage,
    AgenciaBrasilPage,
    R7Page,
]


def coletar_noticias(
    driver: "WebDriver",
    topic: Topic,
    *,
    settings: Settings | None = None,
    page_factories: list[type[BaseNewsPage]] | None = None,
) -> list[NewsArticle]:
    """Coleta notícias do `topic` em cada fonte fixa e devolve a lista plana."""
    cfg = settings or get_settings()
    factories = page_factories or _DEFAULT_PAGE_FACTORIES

    logger.info(
        "Coleta nas %d fontes fixas | tema=%s | max_por_site=%d",
        len(factories),
        label_for(topic),
        cfg.max_news_per_site,
    )

    coletadas: list[NewsArticle] = []
    for factory in factories:
        page = factory(driver, cfg)
        try:
            articles = page.collect(topic, max_items=cfg.max_news_per_site)
        except Exception as exc:
            logger.error("Falha em %s: %s", page.name, exc)
            continue
        logger.info("  → %s: %d notícias coletadas", page.name, len(articles))
        coletadas.extend(articles)

    coletadas.sort(key=_sort_key, reverse=True)
    logger.info("Coleta concluída: %d notícias (antes do dedupe)", len(coletadas))
    return coletadas


def _sort_key(article: NewsArticle) -> datetime:
    """Ordena artigos por `published_at` desc, com datados à frente."""
    if article.published_at is None:
        return datetime.min.replace(tzinfo=timezone.utc)
    pub = article.published_at
    if pub.tzinfo is None:
        pub = pub.replace(tzinfo=timezone.utc)
    return pub
