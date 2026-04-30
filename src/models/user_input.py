"""Modelo Pydantic da entrada do usuário (tema selecionado + N dias)."""

from pydantic import BaseModel, ConfigDict, Field

from src.models.topics import Topic, label_for


class UserInput(BaseModel):
    """Entrada validada do usuário."""

    model_config = ConfigDict(frozen=True)

    topic: Topic = Field(description="Tema selecionado do menu (1-10).")
    days: int = Field(ge=1, le=10, description="Últimos N dias (1-10).")

    @property
    def topic_label(self) -> str:
        """Rótulo legível do tema escolhido."""
        return label_for(self.topic)
