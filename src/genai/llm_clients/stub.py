"""Implementação `StubLLMClient` — determinística e offline.

Útil para R1 (sem provedor decidido), CI e testes. Reaproveita o
conteúdo do prompt para gerar uma resposta plausível, sem chamar
qualquer API externa.
"""

from __future__ import annotations

import re

_SECTION_RE = re.compile(
    r"NOTÍCIAS:\s*(.+?)(?:\n[A-ZÀ-ÚÇ ]{4,}:|\Z)",
    flags=re.DOTALL | re.IGNORECASE,
)
_BULLET_RE = re.compile(r"^\s*[-*\d.]\s*(.+)$", flags=re.MULTILINE)


class StubLLMClient:
    """Gera um resumo sintético baseado nos próprios títulos do prompt."""

    name: str = "stub"

    def complete(
        self,
        *,
        system: str,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 800,
    ) -> str:
        """Devolve um texto curto sintetizando os bullets identificados no prompt."""
        del system, temperature, max_tokens

        section = _SECTION_RE.search(prompt)
        body = section.group(1) if section else prompt
        bullets = [b.strip() for b in _BULLET_RE.findall(body) if b.strip()]
        bullets = bullets[:8]

        if not bullets:
            return (
                "Não foram identificados pontos de destaque suficientes para "
                "produzir um resumo nesta execução."
            )

        intro = (
            f"Foram analisadas {len(bullets)} manchetes recentes. "
            "Principais destaques:"
        )
        bullet_lines = "\n".join(f"- {b}" for b in bullets)
        outro = (
            "Resumo gerado de forma offline (provedor 'stub'). "
            "Para um resumo gerado por LLM, configure LLM_PROVIDER e LLM_API_KEY."
        )
        return f"{intro}\n{bullet_lines}\n\n{outro}"
