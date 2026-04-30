"""Testes de parsing de datas (`parse_date`)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from src.utils.date_filter import parse_date


class TestParseDate:
    def test_iso_simples(self) -> None:
        result = parse_date("2026-04-30T14:00:00+00:00")
        assert result is not None
        assert result.year == 2026
        assert result.tzinfo is not None

    def test_iso_com_z(self) -> None:
        result = parse_date("2026-04-30T14:00:00Z")
        assert result is not None
        assert result.month == 4

    def test_pt_longo(self) -> None:
        result = parse_date("30 de abril de 2026")
        assert result is not None
        assert result == datetime(2026, 4, 30, tzinfo=timezone.utc)

    def test_pt_longo_abreviado(self) -> None:
        result = parse_date("01 de jan de 2026")
        assert result is not None
        assert result.month == 1

    def test_dd_mm_yyyy_com_hora(self) -> None:
        result = parse_date("30/04/2026 09:30")
        assert result is not None
        assert result.day == 30
        assert result.hour == 9

    def test_relativo_horas(self) -> None:
        agora = datetime(2026, 4, 30, 15, 0, tzinfo=timezone.utc)
        result = parse_date("há 3 horas", now=agora)
        assert result is not None
        assert result == agora - timedelta(hours=3)

    def test_relativo_dias(self) -> None:
        agora = datetime(2026, 4, 30, tzinfo=timezone.utc)
        result = parse_date("há 2 dias", now=agora)
        assert result == agora - timedelta(days=2)

    def test_string_vazia(self) -> None:
        assert parse_date("") is None

    def test_formato_desconhecido(self) -> None:
        assert parse_date("texto sem data") is None
