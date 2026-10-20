"""Casos de integração gerados pelo few-shot ajustado.

O limite do teste é o navegador e a internet. As fontes são páginas
falsas e o resumo usa o cliente stub, que não chama a API da OpenAI.
"""

from datetime import datetime, timezone

from src.genai.llm_clients.stub import StubLLMClient
from src.genai.summarizer import summarize
from src.models.news import NewsArticle
from src.models.topics import Topic
from src.models.user_input import UserInput
from src.services.orchestrator import _run_pipeline
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


def _fabrica(nome: str, artigos: list[NewsArticle] | None = None, falha: str | None = None):
    class Pagina:
        name = nome

        def __init__(self, driver, settings) -> None:
            del driver, settings

        def collect(self, topic, max_items: int = 15):
            del topic
            if falha:
                raise RuntimeError(falha)
            return list(artigos or [])[:max_items]

    return Pagina


def test_fonte_indisponivel_nao_impede_as_outras_e_url_repetida_sai() -> None:
    chip = _artigo(
        "Chip ficticio e anunciado",
        "https://exemplo.teste/g1/chip",
        "G1",
    )
    chip_repetido = chip.model_copy(update={"url": "https://exemplo.teste/g1/chip?utm=1"})
    estudo = _artigo(
        "Laboratorio ficticio publica estudo",
        "https://exemplo.teste/agencia/estudo",
        "Agencia Brasil",
    )
    aplicativo = _artigo(
        "Aplicativo ficticio chega ao publico",
        "https://exemplo.teste/r7/app",
        "R7",
    )
    coletadas = coletar_noticias(
        None,
        Topic.TECNOLOGIA,
        settings=Settings(),
        page_factories=[
            _fabrica("G1", [chip, chip_repetido]),
            _fabrica("BBC", falha="timeout ficticio"),
            _fabrica("Agencia Brasil", [estudo]),
            _fabrica("R7", [aplicativo]),
        ],
    )

    assert {artigo.source for artigo in coletadas} == {"G1", "Agencia Brasil", "R7"}
    unicas = dedupe(coletadas)
    resumo = summarize(
        unicas,
        Topic.TECNOLOGIA,
        settings=Settings(),
        client=StubLLMClient(),
    )

    assert len(unicas) == 3
    assert resumo.metadata["llm_provider"] == "stub"
    assert resumo.metadata["articles_total"] == 3
    assert {fonte.source for fonte in resumo.sources} == {"G1", "Agencia Brasil", "R7"}
    assert resumo.bullets


def test_mesmo_titulo_em_fontes_diferentes_conta_uma_vez() -> None:
    g1 = _artigo(
        "Satelite ficticio entra em orbita",
        "https://exemplo.teste/g1/satelite",
        "G1",
    )
    r7 = _artigo(
        "Satelite ficticio entra em orbita",
        "https://exemplo.teste/r7/satelite",
        "R7",
    )
    unicas = dedupe([g1, r7])
    resumo = summarize(
        unicas,
        Topic.TECNOLOGIA,
        settings=Settings(),
        client=StubLLMClient(),
    )

    assert len(unicas) == 1
    assert resumo.metadata["articles_total"] == 1
    assert len(resumo.sources) == 1


def test_coleta_vazia_nao_chama_a_sumarizacao(monkeypatch) -> None:
    chamadas = {"total": 0}

    monkeypatch.setattr(
        "src.services.orchestrator.coletar_noticias",
        lambda driver, topic, settings=None: [],
    )

    def _proibir_sumarizacao(*args, **kwargs):
        del args, kwargs
        chamadas["total"] += 1
        raise AssertionError("a sumarizacao nao deveria ser chamada")

    monkeypatch.setattr("src.services.orchestrator.summarize", _proibir_sumarizacao)

    resultado = _run_pipeline(
        None,
        UserInput(topic=Topic.TECNOLOGIA),
        Settings(),
    )

    assert resultado is None
    assert chamadas["total"] == 0
