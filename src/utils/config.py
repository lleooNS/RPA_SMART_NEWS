"""Configuração centralizada da aplicação (lida do `.env`)."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]


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
    max_days: int = Field(
        default=10,
        ge=1,
        le=10,
        description="Limite máximo de dias aceitos no input do usuário.",
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


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Retorna as configurações da aplicação (singleton em memória)."""
    return Settings()
