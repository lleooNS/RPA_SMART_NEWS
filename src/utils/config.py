"""Configuração centralizada da aplicação (lida do `.env`)."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

LLMProvider = Literal["stub", "openai"]


class Settings(BaseSettings):
    """Configurações da aplicação carregadas do ambiente / `.env`."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    log_level: str = Field(
        default="INFO",
        description="Nível de log: DEBUG, INFO, WARNING, ERROR.",
    )
    max_retries: int = Field(
        default=3,
        ge=1,
        description="Tentativas de input antes de abortar a execução.",
    )
    output_dir: Path = Field(
        default=PROJECT_ROOT / "output",
        description="Diretório de saída para os PDFs gerados.",
    )

    headless: bool = Field(
        default=False,
        description="Se True, abre o Chrome sem interface (debug/CI).",
    )
    selenium_timeout: float = Field(
        default=15.0,
        gt=0,
        description="Timeout (s) padrão das esperas explícitas do Selenium.",
    )
    humanize_delay_min: float = Field(
        default=0.8,
        ge=0,
        description="Delay mínimo (s) entre ações humanizadas.",
    )
    humanize_delay_max: float = Field(
        default=2.5,
        ge=0,
        description="Delay máximo (s) entre ações humanizadas.",
    )
    max_news_per_site: int = Field(
        default=15,
        ge=1,
        le=100,
        description="Máximo de notícias coletadas por site por execução.",
    )
    user_agent: str = Field(
        default=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        description="User-Agent enviado pelo Chrome controlado.",
    )

    llm_provider: LLMProvider = Field(
        default="stub",
        description="Provedor de LLM: 'stub' (offline) ou 'openai'.",
    )
    llm_model: str = Field(
        default="gpt-4o-mini",
        description="Identificador do modelo LLM (quando aplicável).",
    )
    llm_api_key: str = Field(
        default="",
        description="API key do provedor de LLM (não use o stub).",
    )
    llm_temperature: float = Field(
        default=0.2,
        ge=0,
        le=2,
        description="Temperatura usada nas chamadas ao LLM.",
    )
    llm_max_tokens: int = Field(
        default=800,
        ge=64,
        description="Tokens máximos por resposta do LLM.",
    )

    @field_validator("humanize_delay_max")
    @classmethod
    def _max_geq_min(cls, v: float, info: object) -> float:
        """Garante que o delay máximo é >= mínimo."""
        data = getattr(info, "data", {}) or {}
        minimum = data.get("humanize_delay_min", 0.0)
        if v < minimum:
            raise ValueError("humanize_delay_max deve ser >= humanize_delay_min")
        return v


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Retorna as configurações da aplicação (singleton em memória)."""
    return Settings()
