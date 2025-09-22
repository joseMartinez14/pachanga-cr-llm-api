import orjson
import time
from upstash_redis import Redis
from src.config import settings
from src.schemas.base import ItemFeedback

redis = Redis(url=settings.upstash_redis_url, token=settings.upstash_redis_token)

def _k_session(u, s, g):
    return f"session:{u}:{s}:{g}"

def _k_feedback(u, s, g):
    return f"feedback:{u}:{s}:{g}"

def get_session_items(user_id: str, session_id: str, game_name: str) -> list[dict]:
    raw = redis.get(_k_session(user_id, session_id, game_name))
    if raw is None:
        return []
    # Upstash Redis returns bytes, convert to string if needed
    if isinstance(raw, bytes):
        raw = raw.decode('utf-8')
    return orjson.loads(raw)

def set_session_items(user_id: str, session_id: str, game_name: str, items: list[dict], ttl=60*60*72):
    redis.set(_k_session(user_id, session_id, game_name), orjson.dumps(items).decode('utf-8'), ex=ttl)

def append_session_items(user_id: str, session_id: str, game_name: str, new_items: list[dict], ttl=60*60*72):
    items = get_session_items(user_id, session_id, game_name)
    items.extend(new_items)
    set_session_items(user_id, session_id, game_name, items, ttl)

def append_feedback(user_id: str, session_id: str, game_name: str, entry: ItemFeedback, ttl=60*60*720):
    key = _k_feedback(user_id, session_id, game_name)
    raw = redis.get(key)
    if raw is None:
        arr = []
    else:
        # Upstash Redis returns bytes, convert to string if needed
        if isinstance(raw, bytes):
            raw = raw.decode('utf-8')
        arr = orjson.loads(raw)
    arr.append(entry.model_dump())
    redis.set(key, orjson.dumps(arr).decode('utf-8'), ex=ttl)