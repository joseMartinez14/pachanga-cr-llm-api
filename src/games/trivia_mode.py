from typing import Any
from src.utils.llm import make_llm
from src.schemas.trivia import TriviaResponse
from src.schemas.base import ItemFeedback
from src.redis_store import get_session_items, append_session_items
from src.utils.retry import retry_parse, ParseError
import uuid, orjson


def _make_task(locale: str, topics: list[str], difficulty: str, count: int, avoid: list[str], seed: str | None, past: list = None):
    past_feedback = f"Please don't repeat the same questions and consider the feedback of these past questions: {past}. " if past else ""
    return (
        f"Generate {count} multiple-choice trivia items in {locale}. "
        f"Topics: {topics}. Difficulty: {difficulty}. Avoid: {avoid}. "
        f"One correct answer per item, with answer_index. "
        f"{past_feedback}"
        f"Include meta with source='llm', locale='{locale}', seed='{seed or ''}'. "
        "Explanations d 30 words."
    )


@retry_parse
def generate_trivia_freeforall(
    user_id: str,
    session_id: str,
    game_name: str,
    locale: str,
    specific_params: dict,
):
    past = get_session_items(user_id, session_id, game_name)
    topics = specific_params.get("topics", [])
    difficulty = specific_params.get("difficulty", "medium")
    count = int(specific_params.get("count", 10))
    avoid = specific_params.get("avoid", [])
    seed = specific_params.get("seed")

    # Build LC chain with structured output
    llm = make_llm(temp=0.4).with_structured_output(TriviaResponse)

    # Build task
    task = _make_task(locale, topics, difficulty, count, avoid, seed, past)

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
def generate_trivia_teamvsteam(
    user_id: str,
    session_id: str,
    game_name: str,
    locale: str,
    specific_params: dict,
):
    past = get_session_items(user_id, session_id, game_name)
    topics = specific_params.get("topics", [])
    difficulty = specific_params.get("difficulty", "medium")
    count = int(specific_params.get("count", 10))
    avoid = specific_params.get("avoid", [])
    seed = specific_params.get("seed")
    team_count = specific_params.get("team_count", 2)

    # Build LC chain with structured output
    llm = make_llm(temp=0.4).with_structured_output(TriviaResponse)

    # Build task
    past_feedback = f"Please don't repeat the same questions and consider the feedback of these past questions: {past}. " if past else ""
    task = (
        f"Generate {count} multiple-choice trivia items in {locale} for team vs team format with {team_count} teams. "
        f"Topics: {topics}. Difficulty: {difficulty}. Avoid: {avoid}. "
        f"One correct answer per item, with answer_index. Questions should be fair for team competition. "
        f"{past_feedback}"
        f"Include meta with source='llm', locale='{locale}', seed='{seed or ''}'. "
        "Explanations d 30 words."
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
def generate_trivia_rapidfire(
    user_id: str,
    session_id: str,
    game_name: str,
    locale: str,
    specific_params: dict,
):
    past = get_session_items(user_id, session_id, game_name)
    topics = specific_params.get("topics", [])
    difficulty = specific_params.get("difficulty", "easy")
    count = int(specific_params.get("count", 20))
    avoid = specific_params.get("avoid", [])
    seed = specific_params.get("seed")

    # Build LC chain with structured output
    llm = make_llm(temp=0.4).with_structured_output(TriviaResponse)

    # Build task
    past_feedback = f"Please don't repeat the same questions and consider the feedback of these past questions: {past}. " if past else ""
    task = (
        f"Generate {count} multiple-choice trivia items in {locale} for rapid-fire format. "
        f"Topics: {topics}. Difficulty: {difficulty}. Avoid: {avoid}. "
        f"Questions should be quick to answer (10-15 seconds max). Keep prompts concise. "
        f"One correct answer per item, with answer_index. "
        f"{past_feedback}"
        f"Include meta with source='llm', locale='{locale}', seed='{seed or ''}'. "
        "Explanations d 20 words."
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