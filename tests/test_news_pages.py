"""Testes de sanidade dos Page Objects de cada site fixo.

Valida que cada Page sabe construir URLs de editoria/busca, mapeia
seus locators e expõe `name`/`domain` corretos. A coleta real (com
Selenium) é coberta na suíte de integração — fora do escopo do R1.
"""

from __future__ import annotations

import pytest

from src.models.topics import Topic
from src.pages.agencia_brasil_page import AgenciaBrasilPage
from src.pages.base_news_page import BaseNewsPage
from src.pages.bbc_brasil_page import BBCBrasilPage
from src.pages.g1_page import G1Page
from src.pages.r7_page import R7Page

ALL_PAGE_CLASSES: list[type[BaseNewsPage]] = [
    G1Page,
    BBCBrasilPage,
    AgenciaBrasilPage,
    R7Page,
]


@pytest.mark.parametrize("PageCls", ALL_PAGE_CLASSES)
class TestPageContract:
    """Cada Page Object deve respeitar o contrato comum."""

    def test_tem_name_e_domain(self, PageCls: type[BaseNewsPage]) -> None:
        assert PageCls.name
        assert PageCls.domain
        assert PageCls.base_url.startswith("https://")

    def test_locators_definidos(self, PageCls: type[BaseNewsPage]) -> None:
        assert PageCls.article_locators
        assert PageCls.title_locators
        assert PageCls.link_locators

    def test_search_url_para_todos_os_temas(
        self, PageCls: type[BaseNewsPage]
    ) -> None:
        page = PageCls.__new__(PageCls)
        for topic in Topic:
            url = page.search_url(topic)
            assert url.startswith("http")
            assert PageCls.domain.split("/")[0] in url


class TestG1Editorias:
    """G1: cobertura específica do mapeamento de editorias."""

    def test_economia_tem_editoria(self) -> None:
        page = G1Page.__new__(G1Page)
        url = page.editorial_url(Topic.ECONOMIA)
        assert url is not None
        assert "/economia/" in url

    def test_cotidiano_cai_na_busca(self) -> None:
        page = G1Page.__new__(G1Page)
        assert page.editorial_url(Topic.COTIDIANO) is None


class TestBBCBrasilSemEditoria:
    """BBC News Brasil: todos os temas usam busca interna."""

    @pytest.mark.parametrize("topic", list(Topic))
    def test_editorial_sempre_none(self, topic: Topic) -> None:
        page = BBCBrasilPage.__new__(BBCBrasilPage)
        assert page.editorial_url(topic) is None
