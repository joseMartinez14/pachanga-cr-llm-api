from pydantic import BaseModel, ConfigDict
from typing import List, Literal
from .base import Meta, GameResponse


class TruthDareItem(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: str
    type: Literal["truth","dare"]
    prompt: str
    safety: Literal["G","PG","PG-13","R"] = "PG-13"


class CoupleTDResponse(GameResponse):
    items: List[TruthDareItem]


class CoupleQuizItem(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: str
    type: Literal["quiz"] = "quiz"
    prompt: str
    choices: List[str] | None = None
    category: str | None = None


class CoupleQuizResponse(GameResponse):
    items: List[CoupleQuizItem]


class CoupleWYRItem(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: str
    type: Literal["would_you_rather"] = "would_you_rather"
    option_a: str
    option_b: str
    spice: Literal["low","medium","high"] | None = None


class CoupleWYRResponse(GameResponse):
    items: List[CoupleWYRItem]


class CoupleStoryItem(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: str
    type: Literal["story_starter"] = "story_starter"
    prompt: str
    theme: str | None = None


class CoupleStoryResponse(GameResponse):
    items: List[CoupleStoryItem]