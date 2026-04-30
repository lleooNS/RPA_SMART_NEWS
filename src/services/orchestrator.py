"""Orquestrador principal do RPA_SMART_NEWS."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel

from src.models.user_input import UserInput
from src.services.menu import (
    MenuAbortedError,
    collect_user_input,
    display_topics,
)
from src.utils.config import get_settings
from src.utils.logger import setup_logger

console = Console()


def run() -> int:
    """Inicia o fluxo principal do RPA. Retorna o exit code."""
    settings = get_settings()
    logger = setup_logger(settings.log_level)
    logger.info("Inicializando RPA_SMART_NEWS")

    _print_banner()
    display_topics()

    try:
        user_input = collect_user_input(
            max_retries=settings.max_retries,
            max_days=settings.max_days,
        )
    except MenuAbortedError as exc:
        logger.error("Operacao cancelada: %s", exc)
        console.print(f"\n[bold red]Operação cancelada:[/] {exc}")
        return 1
    except Exception as exc:
        logger.exception("Erro inesperado ao coletar input do usuario")
        console.print(f"\n[bold red]Erro inesperado:[/] {exc}")
        return 2

    _print_confirmation(user_input)
    logger.info(
        "Entrada validada | tema=%s | dias=%d",
        user_input.topic_label,
        user_input.days,
    )

    console.print(
        "\n[dim]Próxima etapa: abertura do navegador "
        "(será implementada nas próximas iterações).[/]"
    )
    return 0


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
            f"[bold]Tema:[/]    {user_input.topic_label}\n"
            f"[bold]Período:[/] últimos {user_input.days} dia(s)",
            title="Confirmação",
            border_style="green",
        )
    )
