"""Parsing de datas em pt-BR / ISO usado pelos Page Objects.

Tenta interpretar a `published_at` exposta pelos sites em diversos
formatos (ISO 8601, "30 de abril de 2026", "30/04/2026 09:30",
"há 3 horas", etc.). Retorna `None` quando nada casa — o chamador
decide se mantém o artigo sem data ou descarta.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

PT_MONTHS: dict[str, int] = {
    "jan": 1, "janeiro": 1,
    "fev": 2, "fevereiro": 2,
    "mar": 3, "marco": 3, "março": 3,
    "abr": 4, "abril": 4,
    "mai": 5, "maio": 5,
    "jun": 6, "junho": 6,
    "jul": 7, "julho": 7,
    "ago": 8, "agosto": 8,
    "set": 9, "setembro": 9,
    "out": 10, "outubro": 10,
    "nov": 11, "novembro": 11,
    "dez": 12, "dezembro": 12,
}

_RELATIVE_RE = re.compile(
    r"h[áa]\s+(\d+)\s*(min|minuto|minutos|h|hora|horas|d|dia|dias)",
    flags=re.IGNORECASE,
)
_DDMMYYYY_RE = re.compile(
    r"(\d{1,2})/(\d{1,2})/(\d{2,4})(?:[\sT](\d{1,2}):(\d{2}))?"
)
_PT_LONG_RE = re.compile(
    r"(\d{1,2})\s*de\s*([a-zA-Z\u00C0-\u017F]+)\s*(?:de\s*)?(\d{4})",
    flags=re.IGNORECASE,
)


def parse_date(text: str, *, now: datetime | None = None) -> datetime | None:
    """Tenta parsear uma string de data em vários formatos comuns.

    Retorna `None` quando nenhum formato for reconhecido.
    """
    if not text:
        return None
    cleaned = text.strip()
    reference = now or datetime.now(timezone.utc)

    try:
        return datetime.fromisoformat(cleaned.replace("Z", "+00:00"))
    except ValueError:
        pass

    rel = _RELATIVE_RE.search(cleaned)
    if rel:
        n = int(rel.group(1))
        unit = rel.group(2).lower()
        if unit.startswith("min"):
            return reference - timedelta(minutes=n)
        if unit.startswith("h"):
            return reference - timedelta(hours=n)
        if unit.startswith("d"):
            return reference - timedelta(days=n)

    pt_long = _PT_LONG_RE.search(cleaned)
    if pt_long:
        day = int(pt_long.group(1))
        month_name = pt_long.group(2).lower().strip()
        year = int(pt_long.group(3))
        month = PT_MONTHS.get(month_name) or PT_MONTHS.get(month_name[:3])
        if month:
            try:
                return datetime(year, month, day, tzinfo=timezone.utc)
            except ValueError:
                return None

    short = _DDMMYYYY_RE.search(cleaned)
    if short:
        day = int(short.group(1))
        month = int(short.group(2))
        year_raw = int(short.group(3))
        year = year_raw + 2000 if year_raw < 100 else year_raw
        hour = int(short.group(4) or 0)
        minute = int(short.group(5) or 0)
        try:
            return datetime(year, month, day, hour, minute, tzinfo=timezone.utc)
        except ValueError:
            return None

    return None
