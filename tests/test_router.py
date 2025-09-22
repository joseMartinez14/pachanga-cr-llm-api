import pytest
from src.router import get_handler, ROUTES

def test_get_handler_known_game():
    handler = get_handler("TriviaMode_FreeForAll")
    assert handler is not None
    assert callable(handler)

def test_get_handler_unknown_game():
    handler = get_handler("UnknownGame")
    assert handler is None

def test_routes_contains_trivia_games():
    assert "TriviaMode_FreeForAll" in ROUTES
    assert "TriviaMode_TeamVsTeam" in ROUTES
    assert "TriviaMode_RapidFire" in ROUTES

def test_routes_contains_couple_games():
    assert "CoupleMode_TruthOrDare" in ROUTES
    assert "CoupleMode_CoupleQuiz" in ROUTES
    assert "CoupleMode_WouldYouRather" in ROUTES
    assert "CoupleMode_StoryBuilder" in ROUTES

def test_routes_contains_party_games():
    assert "PartyMode_DrinkingChallenges" in ROUTES
    assert "PartyMode_Charades" in ROUTES
    assert "PartyMode_SpinTheBottle" in ROUTES
    assert "PartyMode_KingsCup" in ROUTES