from typing import Any
from src.utils.llm import make_llm
from src.schemas.party import DrinkingChallengeResponse, CharadesResponse, SpinBottleResponse, KingsCupResponse
from src.schemas.base import ItemFeedback
from src.redis_store import get_session_items, append_session_items
from src.utils.retry import retry_parse, ParseError
import uuid, orjson


@retry_parse
def generate_party_drinkingchallenges(
    user_id: str,
    session_id: str,
    game_name: str,
    locale: str,
    specific_params: dict,
):
    past = get_session_items(user_id, session_id, game_name)
    intensity = specific_params.get("intensity", "medium")
    count = int(specific_params.get("count", 10))
    avoid = specific_params.get("avoid", [])
    seed = specific_params.get("seed")
    group_size = specific_params.get("group_size", 6)

    # Build LC chain with structured output
    llm = make_llm(temp=0.4).with_structured_output(DrinkingChallengeResponse)

    # Build task
    past_feedback = f"Please don't repeat the same challenges and consider the feedback of these past challenges: {past}. " if past else ""
    task = (
        f"Generate {count} drinking challenge prompts in {locale} for a party of {group_size} people. "
        f"Intensity level: {intensity}. Avoid: {avoid}. "
        f"Challenges should be fun, social, and appropriate for adult party games. "
        f"Include duration when relevant. Focus on group participation and entertainment. "
        f"{past_feedback}"
        f"Include meta with source='llm', locale='{locale}', seed='{seed or ''}'. "
    )

    # Invoke with structured output
    try:
        data = llm.invoke(task)
    except Exception as e:
        raise ParseError(str(e))

    # Save to session with default feedback
    new_items = [{"message": it.prompt, "feedback": "not feedback yet"} for it in data.items]
    append_session_items(user_id, session_id, game_name, new_items)

    return data.model_dump()


@retry_parse
def generate_party_charades(
    user_id: str,
    session_id: str,
    game_name: str,
    locale: str,
    specific_params: dict,
):
    past = get_session_items(user_id, session_id, game_name)
    categories = specific_params.get("categories", ["movies", "books", "celebrities"])
    difficulty = specific_params.get("difficulty", "medium")
    count = int(specific_params.get("count", 20))
    avoid = specific_params.get("avoid", [])
    seed = specific_params.get("seed")

    # Build LC chain with structured output
    llm = make_llm(temp=0.4).with_structured_output(CharadesResponse)

    # Build task
    past_feedback = f"Please don't repeat the same phrases and consider the feedback of these past phrases: {past}. " if past else ""
    task = (
        f"Generate {count} charades phrases in {locale} across categories: {categories}. "
        f"Difficulty: {difficulty}. Avoid: {avoid}. "
        f"Phrases should be recognizable and appropriate for acting out. "
        f"Include variety in categories and difficulty levels. "
        f"{past_feedback}"
        f"Include meta with source='llm', locale='{locale}', seed='{seed or ''}'. "
        "Focus on popular culture and universally known concepts."
    )

    # Invoke with structured output
    try:
        data = llm.invoke(task)
    except Exception as e:
        raise ParseError(str(e))

    # Save to session with default feedback
    new_items = [{"message": it.phrase, "feedback": "not feedback yet"} for it in data.items]
    append_session_items(user_id, session_id, game_name, new_items)

    return data.model_dump()


@retry_parse
def generate_party_spinbottle(
    user_id: str,
    session_id: str,
    game_name: str,
    locale: str,
    specific_params: dict,
):
    past = get_session_items(user_id, session_id, game_name)
    spice_level = specific_params.get("spice_level", "medium")
    count = int(specific_params.get("count", 15))
    avoid = specific_params.get("avoid", [])
    seed = specific_params.get("seed")
    group_composition = specific_params.get("group_composition", "mixed")

    # Build LC chain with structured output
    llm = make_llm(temp=0.4).with_structured_output(SpinBottleResponse)

    # Build task
    past_feedback = f"Please don't repeat the same actions and consider the feedback of these past actions: {past}. " if past else ""
    task = (
        f"Generate {count} spin the bottle action prompts in {locale} for {group_composition} group. "
        f"Spice level: {spice_level}. Avoid: {avoid}. "
        f"Actions should be fun, party-appropriate, and progressive in intensity. "
        f"Include variety in target types and interaction styles. "
        f"{past_feedback}"
        f"Include meta with source='llm', locale='{locale}', seed='{seed or ''}'. "
        "Focus on building group energy and social fun."
    )

    # Invoke with structured output
    try:
        data = llm.invoke(task)
    except Exception as e:
        raise ParseError(str(e))

    # Save to session with default feedback
    new_items = [{"message": it.action, "feedback": "not feedback yet"} for it in data.items]
    append_session_items(user_id, session_id, game_name, new_items)

    return data.model_dump()


@retry_parse
def generate_party_kingscup(
    user_id: str,
    session_id: str,
    game_name: str,
    locale: str,
    specific_params: dict,
):
    past = get_session_items(user_id, session_id, game_name)
    rule_style = specific_params.get("rule_style", "classic")
    count = int(specific_params.get("count", 13))  # 13 cards in a deck
    avoid = specific_params.get("avoid", [])
    seed = specific_params.get("seed")

    # Build LC chain with structured output
    llm = make_llm(temp=0.4).with_structured_output(KingsCupResponse)

    # Build task
    past_feedback = f"Please don't repeat the same rules and consider the feedback of these past rules: {past}. " if past else ""
    task = (
        f"Generate {count} Kings Cup card rules in {locale} with {rule_style} style. "
        f"Avoid: {avoid}. "
        f"Each card (Ace through King) should have a clear rule and description. "
        f"Rules should be easy to understand and execute during a drinking game. "
        f"{past_feedback}"
        f"Include meta with source='llm', locale='{locale}', seed='{seed or ''}'. "
        "Focus on traditional Kings Cup rules with clear explanations."
    )

    # Invoke with structured output
    try:
        data = llm.invoke(task)
    except Exception as e:
        raise ParseError(str(e))

    # Save to session with default feedback
    new_items = [{"message": f"{it.card}: {it.rule}", "feedback": "not feedback yet"} for it in data.items]
    append_session_items(user_id, session_id, game_name, new_items)

    return data.model_dump()