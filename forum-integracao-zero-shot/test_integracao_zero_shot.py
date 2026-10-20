"""Único caso de integração aproveitável do prompt zero-shot.

As quatro fontes respondem e o resumo reúne as quatro notícias.
Não há fonte indisponível, duplicata nem coleta vazia.
"""

from datetime import datetime, timezone

from src.genai.llm_clients.stub import StubLLMClient
from src.genai.summarizer import summarize
from src.models.news import NewsArticle
from src.models.topics import Topic
from src.steps.coleta_step import coletar_noticias
from src.utils.config import Settings
from src.utils.dedupe import dedupe


def _artigo(titulo: str, url: str, fonte: str) -> NewsArticle:
    return NewsArticle(
        title=titulo,
        url=url,
        source=fonte,
        topic=Topic.TECNOLOGIA,
        published_at=datetime(2026, 4, 30, 12, 0, tzinfo=timezone.utc),
        snippet="Trecho ficticio.",
    )


def _fabrica(nome: str, artigo: NewsArticle):
    class Pagina:
        name = nome

        def __init__(self, driver, settings) -> None:
            del driver, settings

        def collect(self, topic, max_items: int = 15):
            del topic
            return [artigo][:max_items]

    return Pagina


def test_quatro_fontes_geram_resumo_com_quatro_noticias() -> None:
    artigos = [
        _artigo("Chip ficticio e anunciado", "https://exemplo.teste/g1/chip", "G1"),
        _artigo("Estudo ficticio sobre redes", "https://exemplo.teste/bbc/redes", "BBC"),
        _artigo("Laboratorio ficticio publica nota", "https://exemplo.teste/agencia/nota", "Agencia Brasil"),
        _artigo("Aplicativo ficticio chega ao publico", "https://exemplo.teste/r7/app", "R7"),
    ]
    fabricas = [
        _fabrica(artigo.source, artigo)
        for artigo in artigos
    ]
    coletadas = coletar_noticias(
        None,
        Topic.TECNOLOGIA,
        settings=Settings(),
        page_factories=fabricas,
    )
    unicas = dedupe(coletadas)
    resumo = summarize(
        unicas,
        Topic.TECNOLOGIA,
        settings=Settings(),
        client=StubLLMClient(),
    )

    assert len(unicas) == 4
    assert resumo.metadata["articles_total"] == 4
    assert len(resumo.sources) == 4
