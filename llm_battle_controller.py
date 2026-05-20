from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY").strip())

def choose_ai_move(opponent_pokemon, player_pokemon, battle_history):
    prompt = """
You are controlling the opponent Pokémon in a battle.

Opponent Pokémon:
""" + str(opponent_pokemon) + """

Player Pokémon:
""" + str(player_pokemon) + """

Battle history:
""" + str(battle_history) + """

Choose the best move for the opponent.
Return only the move name.
""".strip()

    response = client.responses.create(
        model="gpt-5.3-codex",
        input=prompt
    )

    return response.output_text