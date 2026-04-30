"""Base do Page Object Model (placeholder até a etapa de Selenium).

A implementação completa virá no item B-007 do backlog (R1), incluindo:
    - Esperas explícitas (`WebDriverWait`).
    - Helpers de busca de elementos a partir de locators.
    - Scroll humanizado e ações via `ActionChains`.
"""

from __future__ import annotations


class BasePage:
    """Classe base para todos os Page Objects do projeto.

    Esta classe é um **placeholder** nesta iteração e será expandida
    quando a camada Selenium for construída (B-007).
    """

    def __init__(self, driver: object | None = None) -> None:
        """Inicializa a página com a instância do WebDriver."""
        self.driver = driver
