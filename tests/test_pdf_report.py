"""Testes da geração do relatório PDF (B-013)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from src.models.summary import SourceRef, Summary
from src.models.topics import Topic
from src.pdf.report import (
    _build_filename,
    _build_pdf,
    _disambiguate,
    _safe,
    _slugify,
    generate_pdf,
)


def _summary(
    *,
    topic: Topic = Topic.ECONOMIA,
    bullets: list[str] | None = None,
    sources: list[SourceRef] | None = None,
    executive_summary: str = "Resumo executivo de teste com acentos: ção, é, ã.",
) -> Summary:
    """Helper para montar um `Summary` válido com defaults amigáveis."""
    return Summary(
        topic=topic,
        generated_at=datetime(2026, 4, 30, 18, 30, 45, tzinfo=timezone.utc),
        executive_summary=executive_summary,
        bullets=bullets if bullets is not None else ["Ponto A", "Ponto B"],
        sources=sources
        if sources is not None
        else [
            SourceRef(title="Materia 1", url="https://g1.globo.com/a", source="G1"),
            SourceRef(
                title="Materia 2",
                url="https://www.bbc.com/portuguese/b",
                source="BBC News Brasil",
            ),
        ],
        metadata={"llm_provider": "stub", "articles_total": 5},
    )


class TestSlugify:
    def test_remove_acentos_e_normaliza(self) -> None:
        assert _slugify("Crimes/Segurança") == "crimes_seguranca"
        assert _slugify("Saúde") == "saude"
        assert _slugify("Eventos globais") == "eventos_globais"

    def test_string_vazia_devolve_default(self) -> None:
        assert _slugify("") == "tema"
        assert _slugify("???") == "tema"


class TestSafe:
    def test_preserva_pt_br(self) -> None:
        assert _safe("Política, ção e açúcar") == "Política, ção e açúcar"

    def test_substitui_caracteres_fora_de_latin1(self) -> None:
        assert "?" in _safe("emoji 😀 fora")

    def test_string_vazia(self) -> None:
        assert _safe("") == ""


class TestBuildFilename:
    def test_padrao_timestamp_tema(self) -> None:
        summary = _summary(topic=Topic.ECONOMIA)
        assert _build_filename(summary) == "20260430_183045_economia.pdf"

    def test_tema_com_acentos(self) -> None:
        summary = _summary(topic=Topic.SAUDE)
        assert _build_filename(summary).endswith("_saude.pdf")


class TestDisambiguate:
    def test_adiciona_sufixo_quando_arquivo_existe(self, tmp_path: Path) -> None:
        existing = tmp_path / "20260430_183045_economia.pdf"
        existing.write_bytes(b"%PDF-")
        candidate = _disambiguate(existing)
        assert candidate.name == "20260430_183045_economia_2.pdf"
        assert not candidate.exists()

    def test_incrementa_ate_encontrar_disponivel(self, tmp_path: Path) -> None:
        base = tmp_path / "x.pdf"
        base.write_bytes(b"%PDF-")
        (tmp_path / "x_2.pdf").write_bytes(b"%PDF-")
        (tmp_path / "x_3.pdf").write_bytes(b"%PDF-")
        candidate = _disambiguate(base)
        assert candidate.name == "x_4.pdf"


class TestBuildPdf:
    def test_constroi_com_pelo_menos_uma_pagina(self) -> None:
        summary = _summary()
        pdf = _build_pdf(summary)
        assert pdf.page_no() >= 1

    def test_funciona_sem_bullets(self) -> None:
        summary = _summary(bullets=[])
        pdf = _build_pdf(summary)
        assert pdf.page_no() >= 1

    def test_funciona_sem_fontes(self) -> None:
        summary = _summary(sources=[])
        pdf = _build_pdf(summary)
        assert pdf.page_no() >= 1


class TestGeneratePdf:
    def test_gera_arquivo_pdf_valido(self, tmp_path: Path) -> None:
        summary = _summary()
        path = generate_pdf(summary, output_dir=tmp_path)

        assert path.exists()
        assert path.is_absolute()
        assert path.suffix == ".pdf"
        assert path.name.startswith("20260430_183045_economia")
        with path.open("rb") as fh:
            assert fh.read(5) == b"%PDF-"

    def test_overwrite_true_sobrescreve_arquivo_existente(
        self, tmp_path: Path
    ) -> None:
        summary = _summary()
        path1 = generate_pdf(summary, output_dir=tmp_path, overwrite=True)
        size1 = path1.stat().st_size
        path2 = generate_pdf(summary, output_dir=tmp_path, overwrite=True)

        assert path1 == path2
        assert path2.stat().st_size == size1

    def test_overwrite_false_evita_duplicar(self, tmp_path: Path) -> None:
        summary = _summary()
        path1 = generate_pdf(summary, output_dir=tmp_path, overwrite=False)
        path2 = generate_pdf(summary, output_dir=tmp_path, overwrite=False)

        assert path1.exists()
        assert path2.exists()
        assert path1 != path2
        assert path2.name.endswith("_2.pdf")

    def test_cria_output_dir_se_nao_existir(self, tmp_path: Path) -> None:
        target = tmp_path / "novo" / "subdir"
        assert not target.exists()
        path = generate_pdf(_summary(), output_dir=target)
        assert target.is_dir()
        assert path.parent == target.resolve()

    def test_aceita_emoji_no_resumo_sem_quebrar(self, tmp_path: Path) -> None:
        summary = _summary(executive_summary="Boletim 😀 com emoji.")
        path = generate_pdf(summary, output_dir=tmp_path)
        assert path.exists()

    def test_funciona_com_lista_minima(self, tmp_path: Path) -> None:
        summary = _summary(bullets=[], sources=[])
        path = generate_pdf(summary, output_dir=tmp_path)
        assert path.exists()
        assert path.stat().st_size > 0
