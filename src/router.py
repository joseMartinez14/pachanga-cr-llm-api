from typing import Callable, Dict
from src.games.trivia_mode import generate_trivia_freeforall, generate_trivia_teamvsteam, generate_trivia_rapidfire
from src.games.couple_mode import generate_couple_truthordare, generate_couple_quiz, generate_couple_wouldyourather, generate_couple_storybuilder
from src.games.party_mode import generate_party_drinkingchallenges, generate_party_charades, generate_party_spinbottle, generate_party_kingscup


Handler = Callable[..., dict]

ROUTES: Dict[str, Handler] = {
    # Trivia Mode
    "TriviaMode_FreeForAll": generate_trivia_freeforall,
    "TriviaMode_TeamVsTeam": generate_trivia_teamvsteam,
    "TriviaMode_RapidFire": generate_trivia_rapidfire,

    # Couple Mode
    "CoupleMode_TruthOrDare": generate_couple_truthordare,
    "CoupleMode_CoupleQuiz": generate_couple_quiz,
    "CoupleMode_WouldYouRather": generate_couple_wouldyourather,
    "CoupleMode_StoryBuilder": generate_couple_storybuilder,

    # Party Mode
    "PartyMode_DrinkingChallenges": generate_party_drinkingchallenges,
    "PartyMode_Charades": generate_party_charades,
    "PartyMode_SpinTheBottle": generate_party_spinbottle,
    "PartyMode_KingsCup": generate_party_kingscup,
}


def get_handler(game_name: str) -> Handler | None:
    return ROUTES.get(game_name)