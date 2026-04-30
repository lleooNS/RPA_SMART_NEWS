"""Serviço de menu CLI: exibe os 10 temas e coleta o input do usuário."""

from __future__ import annotations

from pydantic import ValidationError
from rich.console import Console
from rich.table import Table

from src.models.topics import TOPIC_LABELS, Topic
from src.models.user_input import UserInput
from src.utils.logger import get_logger

console = Console()
logger = get_logger()


class MenuAbortedError(Exception):
    """Levantada quando o usuário esgota as tentativas de input."""


def display_topics() -> None:
    """Exibe a tabela com os 10 temas suportados."""
    table = Table(
        title="Temas disponíveis",
        title_style="bold cyan",
        header_style="bold magenta",
        show_lines=False,
    )
    table.add_column("#", justify="right", style="dim", width=4)
    table.add_column("Tema", style="bold")
    for topic in Topic:
        table.add_row(str(topic.value), TOPIC_LABELS[topic])
    console.print(table)


def collect_user_input(max_retries: int = 3) -> UserInput:
    """Coleta e valida a entrada do usuário (apenas o tema).

    Re-solicita em caso de input inválido, até `max_retries` tentativas.
    Levanta `MenuAbortedError` se o limite for atingido.
    """
    for attempt in range(1, max_retries + 1):
        topic_raw = console.input("[bold]Escolha um tema (1-10):[/] ").strip()

        try:
            user_input = UserInput(topic=_parse_int(topic_raw, field="tema"))
        except ValueError as exc:
            _warn(str(exc), attempt, max_retries)
            continue
        except ValidationError as exc:
            _warn(_format_validation_error(exc), attempt, max_retries)
            continue

        return user_input

    raise MenuAbortedError(
        f"Número máximo de tentativas ({max_retries}) esgotado."
    )


def _parse_int(value: str, *, field: str) -> int:
    """Converte string em inteiro com mensagem amigável em caso de erro."""
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(
            f"Campo '{field}' precisa ser um número inteiro (recebido: {value!r})."
        ) from exc


def _format_validation_error(exc: ValidationError) -> str:
    """Converte um `ValidationError` em mensagem amigável em pt-BR."""
    parts: list[str] = []
    for err in exc.errors():
        field = ".".join(str(x) for x in err["loc"]) or "input"
        parts.append(f"{field}: {err['msg']}")
    return " | ".join(parts)


def _warn(message: str, attempt: int, max_retries: int) -> None:
    """Imprime aviso de input inválido e contagem de tentativas restantes."""
    remaining = max_retries - attempt
    console.print(f"[red]Entrada inválida.[/] {message}")
    if remaining > 0:
        console.print(f"[yellow]Tentativas restantes: {remaining}[/]\n")
    logger.warning("Input invalido na tentativa %d/%d: %s", attempt, max_retries, message)
