"""Entrypoint do RPA_SMART_NEWS.

Mini-projeto do módulo "Laboratório Introdutório: Construindo um
Mini-projeto com Inteligência Artificial Generativa" — UFG.

Delega toda a orquestração para `src.services.orchestrator.run`.
"""

from __future__ import annotations

import sys

from src.services.orchestrator import run


def main() -> int:
    """Inicia o RPA tratando interrupções do usuário."""
    try:
        return run()
    except KeyboardInterrupt:
        print("\nEncerrado pelo usuário.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
