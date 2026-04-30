"""Factory que devolve a implementação concreta de `LLMClient` por settings."""

from __future__ import annotations

from src.genai.llm_client import LLMClient
from src.utils.config import Settings, get_settings
from src.utils.logger import get_logger

logger = get_logger()


def get_llm_client(settings: Settings | None = None) -> LLMClient:
    """Resolve o provedor configurado (`LLM_PROVIDER`) em uma instância concreta."""
    cfg = settings or get_settings()
    provider = cfg.llm_provider.lower()

    if provider == "stub":
        from src.genai.llm_clients.stub import StubLLMClient

        logger.info("LLM provider: stub (offline)")
        return StubLLMClient()

    if provider == "openai":
        from src.genai.llm_clients.openai_client import OpenAILLMClient

        logger.info("LLM provider: openai (model=%s)", cfg.llm_model)
        return OpenAILLMClient(api_key=cfg.llm_api_key, model=cfg.llm_model)

    raise ValueError(f"LLM provider não suportado: {provider!r}")
