"""Interface abstrata do cliente de LLM e tipos auxiliares."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMClient(Protocol):
    """Contrato mínimo de um cliente de LLM usado pelo projeto."""

    name: str

    def complete(
        self,
        *,
        system: str,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 800,
    ) -> str:
        """Envia o par (system, prompt) e devolve a resposta como texto."""
        ...
