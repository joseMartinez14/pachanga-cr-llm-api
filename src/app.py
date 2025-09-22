import json
import os
from src.router import get_handler
from src.config import settings

def _auth_ok(headers: dict) -> bool:
    token = headers.get("authorization") or headers.get("Authorization")
    if not settings.api_bearer:
        return True
    return token == f"Bearer {settings.api_bearer}"

def _resp(status: int, body: dict):
    return {"statusCode": status, "headers": {"Content-Type": "application/json"}, "body": json.dumps(body)}

def handler(event, context):
    # Handle case where event is a string (local invocation)
    if isinstance(event, str):
        try:
            event = json.loads(event)
        except json.JSONDecodeError:
            return _resp(400, {"error": "invalid event JSON"})

    if not _auth_ok(event.get("headers", {})):
        return _resp(401, {"error": "unauthorized"})

    try:
        body_str = event.get("body") or "{}"
        # Handle case where body is already a dict (local testing)
        if isinstance(body_str, dict):
            body = body_str
        else:
            body = json.loads(body_str)

        user_id = body.get("user_id", "test_user")
        session_id = body.get("session_id", "test_session")
        game_name = body["game_name"]
        specific_params = body.get("specific_params", {})
        locale = body.get("locale", settings.default_locale)
    except Exception as e:
        return _resp(400, {"error": "invalid request body", "details": str(e)})

    fn = get_handler(game_name)
    if not fn:
        return _resp(400, {"error": f"unknown game_name '{game_name}'"})

    try:
        result = fn(
            user_id=user_id,
            session_id=session_id,
            game_name=game_name,
            locale=locale,
            specific_params=specific_params,
        )
        return _resp(200, result)
    except Exception as e:
        return _resp(500, {"error": "generation_failed", "details": str(e)})