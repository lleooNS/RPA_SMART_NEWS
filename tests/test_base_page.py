"""Testes do `BasePage` (placeholder até a implementação completa em B-007)."""

from __future__ import annotations

from src.pages.base_page import BasePage


class TestBasePagePlaceholder:
    """Garante o contrato mínimo do placeholder."""

    def test_instancia_sem_driver(self) -> None:
        page = BasePage()
        assert page.driver is None

    def test_instancia_com_driver_qualquer(self) -> None:
        driver = object()
        page = BasePage(driver=driver)
        assert page.driver is driver
