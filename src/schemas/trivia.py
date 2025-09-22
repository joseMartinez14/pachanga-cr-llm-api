from pydantic import BaseModel, Field, ConfigDict
from typing import List, Literal
from .base import Meta, GameResponse


class TriviaItem(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: str
    type: Literal["multiple_choice"] = "multiple_choice"
    prompt: str
    choices: List[str]
    answer_index: int
    explanation: str | None = None
    topic: str | None = None
    difficulty: Literal["easy","medium","hard"] = "medium"


class TriviaResponse(GameResponse):
    items: List[TriviaItem]