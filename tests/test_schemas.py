import pytest
from src.schemas.base import Meta, ItemFeedback, GameResponse, BaseParams
from src.schemas.trivia import TriviaItem, TriviaResponse
from src.schemas.couple import TruthDareItem, CoupleTDResponse
from src.schemas.party import DrinkingChallengeItem, DrinkingChallengeResponse

def test_meta_schema():
    meta = Meta(locale="es-CR", seed="test123")
    assert meta.source == "llm"
    assert meta.locale == "es-CR"
    assert meta.seed == "test123"

def test_item_feedback_schema():
    feedback = ItemFeedback(message="Test question", feedback="Good")
    assert feedback.message == "Test question"
    assert feedback.feedback == "Good"

def test_base_params_schema():
    params = BaseParams(
        user_id="user1",
        session_id="session1",
        game_name="TriviaMode_FreeForAll"
    )
    assert params.user_id == "user1"
    assert params.session_id == "session1"
    assert params.game_name == "TriviaMode_FreeForAll"
    assert params.locale == "es-CR"
    assert params.count == 10

def test_trivia_item_schema():
    item = TriviaItem(
        id="1",
        prompt="What is 2+2?",
        choices=["3", "4", "5", "6"],
        answer_index=1,
        explanation="Basic math"
    )
    assert item.type == "multiple_choice"
    assert item.prompt == "What is 2+2?"
    assert item.answer_index == 1

def test_trivia_response_schema():
    meta = Meta(locale="en-US")
    items = [
        TriviaItem(
            id="1",
            prompt="Test question?",
            choices=["A", "B"],
            answer_index=0
        )
    ]
    response = TriviaResponse(items=items, meta=meta)
    assert len(response.items) == 1
    assert response.meta.locale == "en-US"

def test_truth_dare_item_schema():
    item = TruthDareItem(
        id="1",
        type="truth",
        prompt="What's your biggest fear?",
        safety="PG"
    )
    assert item.type == "truth"
    assert item.safety == "PG"

def test_drinking_challenge_item_schema():
    item = DrinkingChallengeItem(
        id="1",
        prompt="Take a sip if you've ever...",
        intensity="light",
        duration="30 seconds"
    )
    assert item.type == "drinking_challenge"
    assert item.intensity == "light"