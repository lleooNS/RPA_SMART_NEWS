"""Testes do contrato `LLMClient`, do `StubLLMClient` e do factory."""

from __future__ import annotations

import pytest

from src.genai.factory import get_llm_client
from src.genai.llm_client import LLMClient
from src.genai.llm_clients.stub import StubLLMClient
from src.utils.config import Settings


def _settings(**overrides: object) -> Settings:
    return Settings(_env_file=None, **overrides)  # type: ignore[arg-type]


class TestStubClient:
    def test_implementa_protocolo(self) -> None:
        client = StubLLMClient()
        assert isinstance(client, LLMClient)
        assert client.name == "stub"

    def test_resposta_inclui_bullets_do_prompt(self) -> None:
        client = StubLLMClient()
        prompt = (
            "Tema: Economia\nJanela: 5 dia(s)\n\n"
            "NOTÍCIAS:\n"
            "1. [G1 | 30/04] Selic permanece em 10,75% ao ano\n"
            "2. [BBC | 29/04] Dólar fecha em alta\n"
        )
        out = client.complete(system="x", prompt=prompt)
        assert "Selic" in out
        assert "Dólar" in out
        assert out.startswith("Foram analisadas")

    def test_sem_bullets_devolve_mensagem_default(self) -> None:
        client = StubLLMClient()
        out = client.complete(system="x", prompt="texto solto sem bullets")
        assert "Não foram identificados" in out


class TestFactory:
    def test_provider_stub(self) -> None:
        client = get_llm_client(_settings(llm_provider="stub"))
        assert client.name == "stub"

    def test_provider_invalido(self) -> None:
        with pytest.raises(ValueError):
            get_llm_client(_settings(llm_provider="stub").model_copy(
                update={"llm_provider": "outro"}
            ))

    def test_openai_sem_key_falha(self) -> None:
        with pytest.raises(ValueError):
            get_llm_client(
                _settings(llm_provider="openai", llm_api_key="")
            )
