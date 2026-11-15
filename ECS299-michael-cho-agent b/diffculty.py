import os
from openai import OpenAI
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY").strip())
def adjust_difficulty(difficulty_level: int, player_won: bool, moves: int) -> int:
    """
    Adjusts an integer difficulty level.

    Rules:
    - If the player wins:
        difficulty += 1 + ((80 - moves) / 2)
    - If the player loses:
        difficulty -= 1 + ((80 - moves) / 2)
    - If moves > 80:
        only apply the base result adjustment:
            +1 for win
            -1 for loss

    The final returned difficulty is an integer.
    """

    base_adjustment = 1 if player_won else -1

    if moves > 80:
        return difficulty_level + base_adjustment

    bonus = (80 - moves) / 2

    if player_won:
        new_difficulty = difficulty_level + 1 + bonus
    else:
        new_difficulty = difficulty_level - 1 - bonus

    return int(new_difficulty)
def difficulty_to_percent(difficulty_level: int) -> int:
    
    return difficulty_level 

def generate_pokemon_team(difficulty_level: int) -> str:
    difficulty_percent = difficulty_to_percent(difficulty_level)

    if difficulty_percent < 25:
        team_type = "random basic non-evolved Pokémon"
    elif difficulty_percent < 50:
        team_type = "random medium Pokémon, which can include up to one evolution stage "
    elif difficulty_percent < 75:
        team_type = "random medium pokemon, which can include up to two evolution stages "
    elif difficulty_percent < 95:
        team_type = "strong Pokémon at any evolution stage, but not battle-ready and without competitive strategies"
    else:
        team_type = "a competitive battle-ready team"

    prompt = f"""
    Build a 6-Pokémon opponent AI controlled team based on a difficulty of {difficulty_percent}%.
    This difficulty should generate {team_type}.

    Higher difficulty means stronger synergy, more advanced strategy, and more competitive picks.
    Lower difficulty means simpler, more forgiving, beginner-friendly picks.

    Return valid JSON only.

    Each Pokémon must use this exact format:

    [
    {{
        "name": "",
        "types": ["Type1"],
        "current_hp": 100,
        "max_hp": 100,
        "role": "",
        "item": "",
        "ability": "",
        "nature": "",
        "evs": "",
        "moves": [
        {{
            "name": "",
            "type": "",
            "power": 0
        }},
        {{
            "name": "",
            "type": "",
            "power": 0
        }},
        {{
            "name": "",
            "type": "",
            "power": 0
        }},
        {{
            "name": "",
            "type": "",
            "power": 0
        }}
        ]
    }}
    ]

    Rules:
    - Return exactly 6 Pokémon.
    - Include one or two Pokémon types in the "types" list.
    - Keep power information for every damaging move.
    - If a move does no direct damage, set "power" to 0.
    - Include the type of every move.
    - Do not include markdown.
    - Do not include explanation outside the JSON.
    """.strip()
    print(prompt)

    response = client.responses.create(
        model="gpt-5.3-codex",
        input=prompt
    )

    return json.loads(response.output_text)
