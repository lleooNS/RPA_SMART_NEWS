"""Base do Page Object Model: navegação, esperas, busca e scroll."""

from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.utils.config import Settings, get_settings
from src.utils.humanize import random_delay, scroll_to_top, smooth_scroll
from src.utils.logger import get_logger

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement

Locator = tuple[str, str]


class BasePage:
    """Classe base para todos os Page Objects do projeto."""

    def __init__(
        self,
        driver: "WebDriver",
        settings: Settings | None = None,
    ) -> None:
        """Inicializa a página com driver + settings."""
        self.driver = driver
        self.settings = settings or get_settings()
        self.logger = get_logger()
        self._wait = WebDriverWait(driver, self.settings.selenium_timeout)

    def open(self, url: str) -> None:
        """Navega até a URL informada e aguarda o body carregar."""
        self.logger.info("Abrindo URL: %s", url)
        self.driver.get(url)
        try:
            self._wait.until(EC.presence_of_element_located(("css selector", "body")))
        except TimeoutException:
            self.logger.warning("Timeout esperando <body> em %s", url)
        random_delay(
            self.settings.humanize_delay_min,
            self.settings.humanize_delay_max,
        )

    def find_all(self, locator: Locator) -> list["WebElement"]:
        """Retorna todos os elementos que casam com o locator (lista vazia se nada)."""
        try:
            return self.driver.find_elements(*locator)
        except NoSuchElementException:
            return []

    def find_first(self, locators: list[Locator]) -> list["WebElement"]:
        """Tenta cada locator em ordem e devolve o primeiro com matches."""
        for loc in locators:
            elements = self.find_all(loc)
            if elements:
                self.logger.debug("Locator usado: %s (%d itens)", loc, len(elements))
                return elements
        return []

    def find_first_in(
        self,
        container: "WebElement",
        locators: list[Locator],
    ) -> list["WebElement"]:
        """Busca dentro de um container com fallback entre múltiplos locators."""
        for by, value in locators:
            try:
                items = container.find_elements(by, value)
                if items:
                    return items
            except Exception:
                continue
        return []

    def click_if_present(self, locators: list[Locator]) -> bool:
        """Clica no primeiro elemento encontrado entre os locators (best effort)."""
        for by, value in locators:
            try:
                els = self.driver.find_elements(by, value)
                if els:
                    els[0].click()
                    return True
            except Exception:
                continue
        return False

    def safe_text(self, element: "WebElement", attribute: str | None = None) -> str:
        """Lê texto/atributo de um elemento sem propagar erros."""
        try:
            if attribute:
                return (element.get_attribute(attribute) or "").strip()
            return (element.text or "").strip()
        except Exception:
            return ""

    def humanized_scroll(self, total_pixels: int = 2400) -> None:
        """Faz scroll suave humanizado e pequena pausa final."""
        smooth_scroll(self.driver, total_pixels=total_pixels)
        random_delay(
            self.settings.humanize_delay_min,
            self.settings.humanize_delay_max,
        )

    def back_to_top(self) -> None:
        """Volta ao topo da página (atalho)."""
        scroll_to_top(self.driver)
