"""Testes dos helpers de humanização (delays + scroll)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.utils import humanize


class TestRandomDelay:
    def test_dentro_da_faixa(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(humanize.time, "sleep", lambda _s: None)
        valor = humanize.random_delay(0.0, 0.0)
        assert valor == 0.0

    def test_faixa_invalida(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(humanize.time, "sleep", lambda _s: None)
        with pytest.raises(ValueError):
            humanize.random_delay(2.0, 1.0)

    def test_faixa_negativa_invalida(self) -> None:
        with pytest.raises(ValueError):
            humanize.random_delay(-1.0, 1.0)


class TestSmoothScroll:
    def test_executa_passos_via_execute_script(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(humanize.time, "sleep", lambda _s: None)
        driver = MagicMock()
        steps = humanize.smooth_scroll(
            driver, total_pixels=900, step_pixels=300,
            pause_min=0.0, pause_max=0.0,
        )
        assert steps == 3
        assert driver.execute_script.call_count == 3

    def test_step_zero_devolve_zero(self) -> None:
        driver = MagicMock()
        assert humanize.smooth_scroll(driver, total_pixels=0) == 0


class TestScrollToTop:
    def test_chama_window_scroll_to(self) -> None:
        driver = MagicMock()
        humanize.scroll_to_top(driver)
        driver.execute_script.assert_called_once()
