import json
from src.config import settings
from src.redis_store import append_feedback
from src.schemas.base import ItemFeedback

def _resp(status: int, body: dict):
    return {"statusCode": status, "headers": {"Content-Type": "application/json"}, "body": json.dumps(body)}

def handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
        user_id = body["user_id"]
        session_id = body["session_id"]
        game_name = body["game_name"]
        message = body["message"]
        feedback = body["feedback"]
    except Exception:
        return _resp(400, {"error": "invalid request body"})

    entry = ItemFeedback(message=message, feedback=feedback)
    append_feedback(user_id, session_id, game_name, entry)
    return _resp(200, {"ok": True})