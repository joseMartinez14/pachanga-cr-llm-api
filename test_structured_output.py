#!/usr/bin/env python3
"""Test script to verify structured output works correctly."""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.games.trivia_mode import generate_trivia_freeforall

def test_structured_output():
    print("Testing structured output with trivia function...")

    try:
        result = generate_trivia_freeforall(
            user_id="test_user",
            session_id="test_session",
            game_name="TriviaMode_FreeForAll",
            locale="en",
            specific_params={"count": 2, "topics": ["science"], "difficulty": "easy"}
        )

        print("✓ Function executed successfully!")
        print(f"✓ Result type: {type(result)}")
        print(f"✓ Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")

        if isinstance(result, dict) and 'items' in result:
            print(f"✓ Generated {len(result['items'])} trivia items")
            print(f"✓ First item: {result['items'][0] if result['items'] else 'None'}")

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_structured_output()