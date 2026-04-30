"""Geração do relatório final em PDF (B-013, versão básica).

Layout simples:
    1. Título / subtítulo
    2. Tema + metadados (gerado em, provider LLM, total de notícias)
    3. Resumo executivo
    4. Pontos-chave (bullets), quando houver
    5. Lista de fontes (título + nome da fonte + URL)

A versão apresentável (capa, sumário, clusters, paginação) fica para o R3 (B-201).
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos

from src.models.summary import Summary
from src.models.topics import label_for
from src.utils.config import Settings, get_settings
from src.utils.logger import get_logger

logger = get_logger()

_PAGE_MARGIN: float = 15.0
_LINE_HEIGHT: float = 6.0
_COLOR_LINK: tuple[int, int, int] = (50, 90, 200)
_COLOR_MUTED: tuple[int, int, int] = (90, 90, 90)
_COLOR_TEXT: tuple[int, int, int] = (0, 0, 0)


def generate_pdf(
    summary: Summary,
    *,
    settings: Settings | None = None,
    output_dir: Path | None = None,
    overwrite: bool = True,
) -> Path:
    """Gera o relatório PDF e devolve o **caminho absoluto** do arquivo.

    Args:
        summary: Resultado consolidado da sumarização.
        settings: Configurações da aplicação (opcional, usa singleton).
        output_dir: Diretório de saída (sobrepõe `settings.output_dir`).
        overwrite: Se ``False`` e o arquivo já existir, adiciona sufixo `_2`,
            `_3`, ... evitando duplicar dentro de uma mesma execução.
    """
    cfg = settings or get_settings()
    out_dir = (output_dir or cfg.output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    path = (out_dir / _build_filename(summary)).resolve()
    if path.exists() and not overwrite:
        path = _disambiguate(path)

    pdf = _build_pdf(summary)
    pdf.output(str(path))
    logger.info("PDF gerado | path=%s | sources=%d", path, len(summary.sources))
    return path


def _build_pdf(summary: Summary) -> FPDF:
    """Monta o documento PDF a partir do `Summary`."""
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(_PAGE_MARGIN, _PAGE_MARGIN, _PAGE_MARGIN)
    pdf.set_auto_page_break(auto=True, margin=_PAGE_MARGIN)
    pdf.add_page()

    _render_header(pdf, summary)
    _render_metadata(pdf, summary)
    _render_executive_summary(pdf, summary)
    _render_bullets(pdf, summary)
    _render_sources(pdf, summary)

    return pdf


def _render_header(pdf: FPDF, summary: Summary) -> None:
    """Cabeçalho com título e subtítulo do produto."""
    pdf.set_text_color(*_COLOR_TEXT)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(
        0, 10, _safe("RPA_SMART_NEWS"),
        new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C",
    )
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(
        0, 6, _safe("Resumo Inteligente de Noticias"),
        new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C",
    )
    pdf.ln(4)


def _render_metadata(pdf: FPDF, summary: Summary) -> None:
    """Bloco com tema escolhido + metadados da execução."""
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(
        0, 8, _safe(f"Tema: {label_for(summary.topic)}"),
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )

    pdf.set_text_color(*_COLOR_MUTED)
    pdf.set_font("Helvetica", "", 10)
    generated = summary.generated_at.strftime("%d/%m/%Y %H:%M UTC")
    provider = summary.metadata.get("llm_provider", "?")
    total = summary.metadata.get("articles_total", len(summary.sources))
    pdf.cell(
        0, 5, _safe(f"Gerado em: {generated}"),
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.cell(
        0, 5,
        _safe(f"Provider LLM: {provider}  |  Noticias coletadas: {total}"),
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.set_text_color(*_COLOR_TEXT)
    pdf.ln(3)


def _render_executive_summary(pdf: FPDF, summary: Summary) -> None:
    """Bloco com o resumo executivo."""
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(
        0, 8, _safe("Resumo executivo"),
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(
        0, _LINE_HEIGHT, _safe(summary.executive_summary),
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.ln(2)


def _render_bullets(pdf: FPDF, summary: Summary) -> None:
    """Bloco com os pontos-chave extraídos do resumo."""
    if not summary.bullets:
        return
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(
        0, 8, _safe("Pontos-chave"),
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.set_font("Helvetica", "", 11)
    for bullet in summary.bullets:
        pdf.multi_cell(
            0, _LINE_HEIGHT, _safe(f"- {bullet}"),
            new_x=XPos.LMARGIN, new_y=YPos.NEXT,
        )
    pdf.ln(2)


def _render_sources(pdf: FPDF, summary: Summary) -> None:
    """Lista numerada de fontes (título + site + URL clicável)."""
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(
        0, 8, _safe(f"Fontes ({len(summary.sources)})"),
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.set_font("Helvetica", "", 10)
    for idx, ref in enumerate(summary.sources, start=1):
        pdf.set_text_color(*_COLOR_TEXT)
        pdf.multi_cell(
            0, 5,
            _safe(f"{idx}. {ref.title}  ({ref.source})"),
            new_x=XPos.LMARGIN, new_y=YPos.NEXT,
        )
        url_text = str(ref.url)
        pdf.set_text_color(*_COLOR_LINK)
        pdf.multi_cell(
            0, 5, _safe(url_text),
            link=url_text,
            new_x=XPos.LMARGIN, new_y=YPos.NEXT,
            wrapmode="CHAR",
        )
        pdf.ln(1)
    pdf.set_text_color(*_COLOR_TEXT)


def _safe(text: str) -> str:
    """Garante texto compatível com a fonte core Helvetica (latin-1).

    Caracteres fora do latin-1 (ex.: emojis) viram ``?`` para não quebrar a
    geração — todos os caracteres comuns do português brasileiro estão
    cobertos.
    """
    if not text:
        return ""
    return text.encode("latin-1", errors="replace").decode("latin-1")


def _build_filename(summary: Summary) -> str:
    """Monta o nome `<YYYYMMDD_HHMMSS>_<slug-do-tema>.pdf`."""
    ts = summary.generated_at.strftime("%Y%m%d_%H%M%S")
    slug = _slugify(label_for(summary.topic))
    return f"{ts}_{slug}.pdf"


def _disambiguate(path: Path) -> Path:
    """Adiciona sufixo `_2`, `_3`, ... quando o arquivo já existe."""
    stem, suffix, parent = path.stem, path.suffix, path.parent
    counter = 2
    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slugify(text: str) -> str:
    """Slug ASCII minúsculo com `_` como separador (`Crimes/Segurança` → `crimes_seguranca`)."""
    norm = unicodedata.normalize("NFKD", text)
    ascii_only = norm.encode("ascii", "ignore").decode("ascii").lower()
    cleaned = _SLUG_RE.sub("_", ascii_only).strip("_")
    return cleaned or "tema"
