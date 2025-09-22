from typing import Any
from src.utils.llm import make_llm
from src.schemas.couple import CoupleTDResponse, CoupleQuizResponse, CoupleWYRResponse, CoupleStoryResponse
from src.schemas.base import ItemFeedback
from src.redis_store import get_session_items, append_session_items
from src.utils.retry import retry_parse, ParseError
import uuid, orjson


@retry_parse
def generate_couple_truthordare(
    user_id: str,
    session_id: str,
    game_name: str,
    locale: str,
    specific_params: dict,
):
    past = get_session_items(user_id, session_id, game_name)
    safety = specific_params.get("safety", "PG-13")
    count = int(specific_params.get("count", 10))
    avoid = specific_params.get("avoid", [])
    seed = specific_params.get("seed")
    truth_ratio = specific_params.get("truth_ratio", 0.5)

    # Build LC chain with structured output
    llm = make_llm(temp=0.4).with_structured_output(CoupleTDResponse)

    # Build task
    past_feedback = f"Please don't repeat the same questions and consider the feedback of these past questions: {past}. " if past else ""

    # Build task
    task = (
        f"Generate {count} truth or dare items in {locale} for couples. "
        f"Safety rating: {safety}. Avoid: {avoid}. "
        f"Mix of truth and dare questions with {truth_ratio} ratio for truth questions. "
        f"Questions should be intimate and fun for couples. "
        f"{past_feedback}"
        f"Include meta with source='llm', locale='{locale}', seed='{seed or ''}'. "
        "Keep items romantic and playful."
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
def generate_couple_quiz(
    user_id: str,
    session_id: str,
    game_name: str,
    locale: str,
    specific_params: dict,
):
    past = get_session_items(user_id, session_id, game_name)
    count = int(specific_params.get("count", 10))
    avoid = specific_params.get("avoid", [])
    seed = specific_params.get("seed")
    relationship_stage = specific_params.get("relationship_stage", "dating")

    # Build LC chain with structured output
    llm = make_llm(temp=0.4).with_structured_output(CoupleQuizResponse)

    # Build task
    past_feedback = f"Please don't repeat the same questions and consider the feedback of these past questions: {past}. " if past else ""
    task = (
        f"Generate {count} couple quiz questions in {locale} for couples in {relationship_stage} stage. "
        f"Avoid: {avoid}. "
        f"Questions should help couples learn about each other and spark conversations. "
        f"Include multiple choice answers or open-ended questions. "
        f"{past_feedback}"
        f"Include meta with source='llm', locale='{locale}', seed='{seed or ''}'. "
        "Focus on compatibility, preferences, and getting to know each other better."
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
def generate_couple_wouldyourather(
    user_id: str,
    session_id: str,
    game_name: str,
    locale: str,
    specific_params: dict,
):
    past = get_session_items(user_id, session_id, game_name)
    spice_level = specific_params.get("spice_level", "medium")
    count = int(specific_params.get("count", 10))
    avoid = specific_params.get("avoid", [])
    seed = specific_params.get("seed")

    # Build LC chain with structured output
    llm = make_llm(temp=0.4).with_structured_output(CoupleWYRResponse)

    # Build task
    past_feedback = f"Please don't repeat the same questions and consider the feedback of these past questions: {past}. " if past else ""
    task = (
        f"Generate {count} 'would you rather' questions in {locale} for couples. "
        f"Spice level: {spice_level}. Avoid: {avoid}. "
        f"Questions should be fun, thought-provoking, and couple-oriented. "
        f"Each question should have two interesting options to choose from. "
        f"{past_feedback}"
        f"Include meta with source='llm', locale='{locale}', seed='{seed or ''}'. "
        "Focus on relationship scenarios, preferences, and fun hypotheticals."
    )

    # Invoke with structured output
    try:
        data = llm.invoke(task)
    except Exception as e:
        raise ParseError(str(e))

    # Save to session with default feedback
    new_items = [{"message": f"{it.option_a} OR {it.option_b}", "feedback": "not feedback yet"} for it in data.items]
    append_session_items(user_id, session_id, game_name, new_items)

    return data.model_dump()


@retry_parse
def generate_couple_storybuilder(
    user_id: str,
    session_id: str,
    game_name: str,
    locale: str,
    specific_params: dict,
):
    past = get_session_items(user_id, session_id, game_name)
    theme = specific_params.get("theme", "romantic")
    count = int(specific_params.get("count", 10))
    avoid = specific_params.get("avoid", [])
    seed = specific_params.get("seed")

    # Build LC chain with structured output
    llm = make_llm(temp=0.4).with_structured_output(CoupleStoryResponse)

    # Build task
    past_feedback = f"Please don't repeat the same questions and consider the feedback of these past questions: {past}. " if past else ""
    task = (
        f"Generate {count} story building prompts in {locale} for couples with theme: {theme}. "
        f"Avoid: {avoid}. "
        f"Each prompt should be a story starter that couples can build together. "
        f"Prompts should encourage creativity, imagination, and collaboration. "
        f"{past_feedback}"
        f"Include meta with source='llm', locale='{locale}', seed='{seed or ''}'. "
        "Focus on scenarios that couples can develop together turn by turn."
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