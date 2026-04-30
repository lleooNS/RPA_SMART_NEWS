"""Testes da `BasePage` (waits, helpers de busca, scroll)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.pages.base_page import BasePage
from src.utils.config import Settings


@pytest.fixture
def fake_driver() -> MagicMock:
    """Driver mock com a interface mínima usada pela `BasePage`."""
    driver = MagicMock(name="WebDriver")
    driver.find_elements.return_value = []
    driver.execute_script.return_value = None
    driver.get.return_value = None
    return driver


@pytest.fixture
def settings() -> Settings:
    """Settings rápidos para acelerar os testes (delays mínimos)."""
    return Settings(
        _env_file=None,  # type: ignore[arg-type]
        humanize_delay_min=0.0,
        humanize_delay_max=0.0,
        selenium_timeout=0.5,
    )


class TestBasePageBasics:
    """Inicialização e atributos básicos."""

    def test_init_armazena_driver_e_settings(
        self, fake_driver: MagicMock, settings: Settings
    ) -> None:
        page = BasePage(fake_driver, settings)
        assert page.driver is fake_driver
        assert page.settings is settings


class TestFindHelpers:
    """Helpers de busca de elementos."""

    def test_find_all_devolve_lista_vazia_quando_sem_resultados(
        self, fake_driver: MagicMock, settings: Settings
    ) -> None:
        page = BasePage(fake_driver, settings)
        assert page.find_all(("css selector", ".x")) == []

    def test_find_first_usa_o_primeiro_locator_com_resultado(
        self, fake_driver: MagicMock, settings: Settings
    ) -> None:
        elemento = MagicMock(name="WebElement")
        fake_driver.find_elements.side_effect = [[], [elemento]]
        page = BasePage(fake_driver, settings)
        result = page.find_first([
            ("css selector", ".inexistente"),
            ("css selector", ".existente"),
        ])
        assert result == [elemento]

    def test_find_first_in_busca_dentro_de_container(
        self, fake_driver: MagicMock, settings: Settings
    ) -> None:
        container = MagicMock(name="Container")
        elemento = MagicMock(name="Filho")
        container.find_elements.side_effect = [[], [elemento]]
        page = BasePage(fake_driver, settings)
        result = page.find_first_in(
            container,
            [("css selector", ".a"), ("css selector", ".b")],
        )
        assert result == [elemento]

    def test_safe_text_le_texto_e_atributo(
        self, fake_driver: MagicMock, settings: Settings
    ) -> None:
        el = MagicMock()
        el.text = "  Olá  "
        el.get_attribute.return_value = "  https://x.com  "
        page = BasePage(fake_driver, settings)
        assert page.safe_text(el) == "Olá"
        assert page.safe_text(el, attribute="href") == "https://x.com"

    def test_safe_text_resiliente_a_excecao(
        self, fake_driver: MagicMock, settings: Settings
    ) -> None:
        el = MagicMock()
        type(el).text = property(lambda self: (_ for _ in ()).throw(RuntimeError()))
        page = BasePage(fake_driver, settings)
        assert page.safe_text(el) == ""


class TestClickIfPresent:
    """Cliques tolerantes para overlays."""

    def test_click_if_present_devolve_true_no_primeiro_match(
        self, fake_driver: MagicMock, settings: Settings
    ) -> None:
        el = MagicMock()
        fake_driver.find_elements.side_effect = [[], [el]]
        page = BasePage(fake_driver, settings)
        assert page.click_if_present([
            ("css selector", ".a"),
            ("css selector", ".b"),
        ])
        el.click.assert_called_once()

    def test_click_if_present_devolve_false_quando_nada_existe(
        self, fake_driver: MagicMock, settings: Settings
    ) -> None:
        page = BasePage(fake_driver, settings)
        assert page.click_if_present([("css selector", ".x")]) is False
