"""Implementação `OpenAILLMClient` (lazy import — opcional)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openai import OpenAI


class OpenAILLMClient:
    """Cliente LLM apoiado em `openai>=1.0`. Requer `pip install openai`."""

    name: str = "openai"

    def __init__(self, *, api_key: str, model: str) -> None:
        """Inicializa o cliente; valida chave e tenta importar `openai`."""
        if not api_key:
            raise ValueError("LLM_API_KEY ausente para o provedor 'openai'.")
        try:
            from openai import OpenAI as _OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "Pacote 'openai' não instalado. Rode `pip install openai` "
                "ou troque LLM_PROVIDER para 'stub'."
            ) from exc
        self._client: "OpenAI" = _OpenAI(api_key=api_key)
        self._model = model

    def complete(
        self,
        *,
        system: str,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 800,
    ) -> str:
        """Chama Chat Completions e devolve o texto da primeira resposta."""
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        choice = response.choices[0].message.content or ""
        return choice.strip()
