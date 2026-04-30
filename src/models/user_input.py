"""Modelo Pydantic da entrada do usuário (apenas o tema selecionado)."""

from pydantic import BaseModel, ConfigDict, Field

from src.models.topics import Topic, label_for


class UserInput(BaseModel):
    """Entrada validada do usuário."""

    model_config = ConfigDict(frozen=True)

    topic: Topic = Field(description="Tema selecionado do menu (1-10).")

    @property
    def topic_label(self) -> str:
        """Rótulo legível do tema escolhido."""
        return label_for(self.topic)
