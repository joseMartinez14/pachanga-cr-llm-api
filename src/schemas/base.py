from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional, List, Any


class Meta(BaseModel):
    model_config = ConfigDict(extra='ignore')
    source: Literal["llm"] = "llm"
    locale: str
    seed: Optional[str] = None


class ItemFeedback(BaseModel):
    message: str
    feedback: Literal["Good", "Bad", "not feedback yet"] = "not feedback yet"


class GameResponse(BaseModel):
    model_config = ConfigDict(extra='ignore')
    items: List[Any]
    meta: Meta


class BaseParams(BaseModel):
    user_id: str
    session_id: str
    game_name: str
    locale: str = "es-CR"
    count: int = 10
    avoid: list[str] = []
    seed: str | None = None