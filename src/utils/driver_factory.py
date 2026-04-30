"""Factory do WebDriver Selenium (Chrome) com `chromedriver-autoinstaller`."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.utils.config import Settings, get_settings
from src.utils.logger import get_logger

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver

logger = get_logger()


def create_driver(settings: Settings | None = None) -> "WebDriver":
    """Cria e devolve uma instância configurada do Chrome WebDriver.

    O ChromeDriver é instalado/atualizado automaticamente via
    `chromedriver-autoinstaller`, dispensando setup manual.
    """
    import chromedriver_autoinstaller
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    cfg = settings or get_settings()
    chromedriver_autoinstaller.install()

    options = Options()
    if cfg.headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1366,900")
    options.add_argument(f"--user-agent={cfg.user_agent}")
    options.add_argument("--lang=pt-BR")
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"]
    )
    options.add_experimental_option("useAutomationExtension", False)
    options.page_load_strategy = "eager"

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(cfg.selenium_timeout * 2)
    driver.implicitly_wait(0)
    logger.info(
        "WebDriver Chrome inicializado | headless=%s | timeout=%.1fs",
        cfg.headless,
        cfg.selenium_timeout,
    )
    return driver


def quit_driver(driver: "WebDriver | None") -> None:
    """Encerra o driver de forma resiliente, sem propagar exceções."""
    if driver is None:
        return
    try:
        driver.quit()
        logger.info("WebDriver encerrado.")
    except Exception as exc:
        logger.warning("Falha ao encerrar WebDriver: %s", exc)
