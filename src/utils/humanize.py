"""Helpers de humanização da navegação (scroll suave + delays)."""

from __future__ import annotations

import random
import time
from typing import Protocol


class _SupportsExecuteScript(Protocol):
    def execute_script(self, script: str, *args: object) -> object: ...


def random_delay(min_seconds: float, max_seconds: float) -> float:
    """Aguarda um tempo aleatório dentro da faixa e retorna o valor usado."""
    if min_seconds < 0 or max_seconds < min_seconds:
        raise ValueError("Faixa de delay inválida.")
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)
    return delay


def smooth_scroll(
    driver: _SupportsExecuteScript,
    *,
    total_pixels: int = 2400,
    step_pixels: int = 300,
    pause_min: float = 0.15,
    pause_max: float = 0.45,
) -> int:
    """Faz scroll incremental simulando rolagem humana.

    Retorna o número de passos efetivamente executados.
    """
    if step_pixels <= 0 or total_pixels <= 0:
        return 0
    steps = max(1, total_pixels // step_pixels)
    for _ in range(steps):
        driver.execute_script(f"window.scrollBy(0, {step_pixels});")
        time.sleep(random.uniform(pause_min, pause_max))
    return steps


def scroll_to_top(driver: _SupportsExecuteScript) -> None:
    """Volta ao topo da página (sem animação)."""
    driver.execute_script("window.scrollTo(0, 0);")
