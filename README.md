# Party Game API - AI-Powered Game Content Generator

A serverless Python API that generates dynamic party game content using OpenAI and LangChain. Features Redis session management, Pydantic validation, and supports 11 different game types across 3 categories.

## 🚀 Live API Endpoint

**Lambda Function:** `https://skujfs07yh.execute-api.us-east-1.amazonaws.com/game-content`

## 🎮 Supported Game Types

### Trivia Mode

- **TriviaMode_FreeForAll** - General trivia questions
- **TriviaMode_TeamVsTeam** - Team competition format
- **TriviaMode_RapidFire** - Quick-answer format

### Couple Mode

- **CoupleMode_TruthOrDare** - Truth or dare questions
- **CoupleMode_CoupleQuiz** - Compatibility questions
- **CoupleMode_WouldYouRather** - Choice-based questions
- **CoupleMode_StoryBuilder** - Story starter prompts

### Party Mode

- **PartyMode_DrinkingChallenges** - Adult party challenges
- **PartyMode_Charades** - Acting/guessing game items
- **PartyMode_SpinTheBottle** - Bottle spin actions
- **PartyMode_KingsCup** - Card-based party rules

## 📡 API Usage

### Generate Game Content

**Endpoint:** `POST /game-content`

```bash
curl -X POST https://your-api-gateway-url/game-content \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "user_id": "user123",
    "session_id": "session456",
    "game_name": "TriviaMode_FreeForAll",
    "locale": "es-CR",
    "specific_params": {
      "topics": ["fútbol", "Italia 90"],
      "difficulty": "medium",
      "count": 5,
      "avoid": ["violencia"]
    }
  }'
```

### Submit Feedback

**Endpoint:** `POST /feedback`

```bash
curl -X POST https://your-api-gateway-url/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "session_id": "session456",
    "game_name": "TriviaMode_FreeForAll",
    "message": "¿En qué año Costa Rica jugó su primer Mundial?",
    "feedback": "Good"
  }'
```

## 🎯 Game Parameters

### Common Parameters

- `user_id` (string) - User identifier
- `session_id` (string) - Session identifier
- `game_name` (string) - One of the supported game types
- `locale` (string) - Language/locale (default: "es-CR")
- `specific_params` (object) - Game-specific parameters

### Trivia Mode Parameters

- `topics` (array) - List of trivia topics
- `difficulty` (string) - "easy", "medium", "hard" (default: "medium")
- `count` (number) - Number of questions (default: 10)
- `avoid` (array) - Topics to avoid
- `seed` (string) - Random seed for reproducibility

**Example for TeamVsTeam:**

```json
{
  "topics": ["history", "science"],
  "difficulty": "hard",
  "count": 15,
  "team_count": 3
}
```

### Couple Mode Parameters

- `safety` (string) - "G", "PG", "PG-13", "R" (default: "PG-13")
- `spice_level` (string) - "low", "medium", "high" (default: "medium")
- `relationship_stage` (string) - "dating", "serious", "married" (default: "dating")
- `truth_ratio` (number) - Ratio of truth vs dare (0.0-1.0, default: 0.5)
- `theme` (string) - Story theme for StoryBuilder (default: "romantic")

**Example for TruthOrDare:**

```json
{
  "safety": "PG-13",
  "count": 8,
  "truth_ratio": 0.6
}
```

### Party Mode Parameters

- `intensity` (string) - "light", "medium", "heavy" (default: "medium")
- `group_size` (number) - Number of players (default: 6)
- `spice_level` (string) - "mild", "medium", "spicy" (default: "medium")
- `categories` (array) - For charades: ["movies", "books", "celebrities"]
- `rule_style` (string) - For Kings Cup: "classic", "modern" (default: "classic")

**Example for Charades:**

```json
{
  "categories": ["movies", "TV shows", "celebrities"],
  "difficulty": "easy",
  "count": 25
}
```

## 📋 Response Format

All endpoints return structured JSON responses:

```json
{
  "items": [
    {
      "id": "uuid-1",
      "type": "multiple_choice",
      "prompt": "¿En qué año Costa Rica jugó su primer Mundial?",
      "choices": ["1986", "1990", "1994", "1998"],
      "answer_index": 1,
      "explanation": "Costa Rica debutó en Italia 1990",
      "topic": "fútbol",
      "difficulty": "medium"
    }
  ],
  "meta": {
    "source": "llm",
    "locale": "es-CR",
    "seed": null
  }
}
```

### Item Types by Game Mode

**Trivia Items:**

- `type`: "multiple_choice"
- `prompt`, `choices`, `answer_index`, `explanation`, `topic`, `difficulty`

**Truth or Dare Items:**

- `type`: "truth" or "dare"
- `prompt`, `safety`

**Couple Quiz Items:**

- `type`: "quiz"
- `prompt`, `choices`, `category`

**Would You Rather Items:**

- `type`: "would_you_rather"
- `option_a`, `option_b`, `spice`

**Story Builder Items:**

- `type`: "story_starter"
- `prompt`, `theme`

**Drinking Challenge Items:**

- `type`: "drinking_challenge"
- `prompt`, `intensity`, `duration`

**Charades Items:**

- `type`: "charades"
- `phrase`, `category`, `difficulty`

**Spin Bottle Items:**

- `type`: "spin_bottle"
- `action`, `target_type`, `spice_level`

**Kings Cup Items:**

- `type`: "kings_cup"
- `card`, `rule`, `description`

## 🧠 Smart Features

### Session Memory

The API remembers past items and user feedback to:

- Avoid repeating questions/challenges
- Consider user preferences from feedback
- Improve content quality over time

### Feedback System

Rate content as "Good", "Bad", or "not feedback yet" to help the AI learn your preferences.

## 🔧 Local Development

### Prerequisites

- Python 3.12+
- Node.js (for Serverless Framework)
- OpenAI API key
- Redis instance (Upstash recommended)

### Setup

1. **Clone and install:**

```bash
git clone <repository>
cd party-game-api
pip install -r requirements.txt
npm install -g serverless
```

2. **Configure environment:**

```bash
cp .env.example .env
# Edit .env with your credentials:
# OPENAI_API_KEY=sk-***
# UPSTASH_REDIS_URL=rediss://***
# UPSTASH_REDIS_TOKEN=***
```

3. **Test locally:**

```bash
# Test a specific game function
serverless invoke local --function game --data '{"body": "{\"game_name\": \"TriviaMode_FreeForAll\"}"}'

# Start offline server
serverless offline
```

4. **Deploy:**

```bash
serverless deploy
```

## 📁 Project Structure

```
src/
├── app.py              # Main Lambda handler
├── router.py           # Game type routing
├── feedback.py         # Feedback endpoint
├── config.py           # Environment settings
├── redis_store.py      # Session storage
├── games/              # Game implementations
│   ├── trivia_mode.py
│   ├── couple_mode.py
│   └── party_mode.py
├── schemas/            # Pydantic models
│   ├── base.py
│   ├── trivia.py
│   ├── couple.py
│   └── party.py
└── utils/              # Utilities
    ├── llm.py
    └── retry.py
```

## 🔐 Authentication

Optional Bearer token authentication. Set `API_BEARER_TOKEN` environment variable to enable.

```bash
curl -H "Authorization: Bearer your-token-here" ...
```

## 🌍 Localization

Supports multiple locales. Default is `es-CR` (Costa Rica Spanish). Pass `locale` parameter to generate content in different languages.

## 📝 License

MIT License
