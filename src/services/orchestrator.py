"""Orquestrador principal do RPA_SMART_NEWS.

Pipeline R1 (end-to-end):
    input (tema) → driver → coleta nas 4 fontes fixas →
    dedupe (URL + título) → sumarização (LLM) → geração do PDF →
    exibição do caminho absoluto do arquivo.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from rich.console import Console
from rich.panel import Panel

from src.genai.summarizer import summarize
from src.models.news import NewsArticle
from src.models.summary import Summary
from src.models.user_input import UserInput
from src.pdf.report import generate_pdf
from src.services.menu import (
    MenuAbortedError,
    collect_user_input,
    display_topics,
)
from src.steps.coleta_step import coletar_noticias
from src.utils.config import Settings, get_settings
from src.utils.dedupe import dedupe
from src.utils.driver_factory import create_driver, quit_driver
from src.utils.logger import setup_logger

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver

console = Console()


def run() -> int:
    """Inicia o fluxo principal do RPA. Retorna o exit code."""
    settings = get_settings()
    logger = setup_logger(settings.log_level)
    logger.info("Inicializando RPA_SMART_NEWS")

    _print_banner()
    display_topics()

    try:
        user_input = collect_user_input(max_retries=settings.max_retries)
    except MenuAbortedError as exc:
        logger.error("Operacao cancelada: %s", exc)
        console.print(f"\n[bold red]Operação cancelada:[/] {exc}")
        return 1
    except Exception as exc:
        logger.exception("Erro inesperado ao coletar input do usuario")
        console.print(f"\n[bold red]Erro inesperado:[/] {exc}")
        return 2

    _print_confirmation(user_input)
    logger.info("Entrada validada | tema=%s", user_input.topic_label)

    driver = None
    try:
        driver = create_driver(settings)
        summary = _run_pipeline(driver, user_input, settings)
    except KeyboardInterrupt:
        logger.warning("Execução interrompida pelo usuário (Ctrl+C).")
        console.print("\n[yellow]Execução interrompida pelo usuário.[/]")
        return 130
    except Exception as exc:
        logger.exception("Erro inesperado durante o pipeline")
        console.print(f"\n[bold red]Erro inesperado no pipeline:[/] {exc}")
        return 3
    finally:
        quit_driver(driver)

    if summary is None:
        return 4
    _print_summary(summary)

    try:
        pdf_path = generate_pdf(summary, settings=settings)
    except Exception as exc:
        logger.exception("Falha ao gerar o PDF")
        console.print(f"\n[bold red]Falha ao gerar o PDF:[/] {exc}")
        return 5

    _print_pdf_path(pdf_path)
    logger.info("Pipeline concluído | pdf=%s", pdf_path)
    return 0


def _run_pipeline(
    driver: "WebDriver",
    user_input: UserInput,
    settings: Settings,
) -> Summary | None:
    """Executa coleta → dedupe → sumarização."""
    logger = setup_logger(settings.log_level)

    coletadas = coletar_noticias(driver, user_input.topic, settings=settings)
    _log_step(logger, "Coleta", coletadas)

    if not coletadas:
        console.print(
            "\n[bold red]Coleta vazia:[/] nenhum dos sites configurados "
            "retornou notícias para esse tema. Possíveis causas:\n"
            "  • Layout das páginas mudou (locators desatualizados)\n"
            "  • Bloqueio temporário por anti-bot em todos os sites\n"
            "  • Sem conexão com a internet\n"
        )
        return None

    unicas = dedupe(coletadas)
    _log_step(logger, "Deduplicação", unicas)

    return summarize(unicas, user_input.topic, settings=settings)


def _log_step(logger, label: str, items: list[NewsArticle]) -> None:
    """Loga o tamanho do conjunto após uma etapa do pipeline."""
    logger.info("%s: %d notícias", label, len(items))


def _print_banner() -> None:
    """Exibe o banner inicial da aplicação."""
    console.print(
        Panel.fit(
            "[bold cyan]RPA_SMART_NEWS[/]\n"
            "[dim]Resumo Inteligente de Notícias[/]",
            border_style="cyan",
        )
    )


def _print_confirmation(user_input: UserInput) -> None:
    """Exibe a confirmação da entrada validada."""
    console.print(
        Panel(
            f"[bold]Tema:[/] {user_input.topic_label}",
            title="Confirmação",
            border_style="green",
        )
    )


def _print_summary(summary: Summary) -> None:
    """Imprime o resumo executivo + total de fontes."""
    body = (
        f"{summary.executive_summary}\n\n"
        f"[dim]Fontes: {len(summary.sources)} | "
        f"Provider LLM: {summary.metadata.get('llm_provider', '?')}[/]"
    )
    console.print(
        Panel(
            body,
            title=f"Resumo — {summary.topic.name.title()}",
            border_style="cyan",
        )
    )


def _print_pdf_path(pdf_path: Path) -> None:
    """Exibe ao usuário o caminho absoluto do PDF gerado (B-014, RF15)."""
    console.print(
        Panel(
            f"[bold green]PDF gerado com sucesso![/]\n\n"
            f"[bold]Caminho:[/] {pdf_path}",
            title="Relatório final",
            border_style="green",
        )
    )
