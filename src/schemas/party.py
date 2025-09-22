from pydantic import BaseModel, ConfigDict
from typing import List, Literal
from .base import GameResponse


class DrinkingChallengeItem(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: str
    type: Literal["drinking_challenge"] = "drinking_challenge"
    prompt: str
    intensity: Literal["light","medium","heavy"] = "medium"
    duration: str | None = None


class DrinkingChallengeResponse(GameResponse):
    items: List[DrinkingChallengeItem]


class CharadesItem(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: str
    type: Literal["charades"] = "charades"
    phrase: str
    category: str
    difficulty: Literal["easy","medium","hard"] = "medium"


class CharadesResponse(GameResponse):
    items: List[CharadesItem]


class SpinBottleItem(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: str
    type: Literal["spin_bottle"] = "spin_bottle"
    action: str
    target_type: Literal["specific","random","choice"] = "random"
    spice_level: Literal["mild","medium","spicy"] = "medium"


class SpinBottleResponse(GameResponse):
    items: List[SpinBottleItem]


class KingsCupItem(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: str
    type: Literal["kings_cup"] = "kings_cup"
    card: str
    rule: str
    description: str


class KingsCupResponse(GameResponse):
    items: List[KingsCupItem]