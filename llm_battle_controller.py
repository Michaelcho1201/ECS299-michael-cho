from openai import OpenAI
import os
import json
from move_analysis import analyze_all_moves, get_super_effective_moves

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY").strip())

def resolve_turn_with_llm(
    player_team,
    opponent_team,
    active_player_index,
    active_opponent_index,
    player_move,
    player_move_damage_info,
    ai_move_options,
    battle_history,
    protect_detect_tracker
):    
    active_player = player_team[active_player_index]
    active_opponent = opponent_team[active_opponent_index]

    ai_move_effectiveness = analyze_all_moves(active_opponent, active_player)
    ai_super_effective_moves = get_super_effective_moves(active_opponent, active_player)

    prompt = f"""
You are the battle engine and opponent AI for a Pokémon-style battle.

The player controls their own 6-Pokémon team.
The AI controls its own 6-Pokémon team.

You must keep track of:
- HP for every Pokémon on both teams
- damage dealt by each attack
- accuracy checks
- move effects
- ability effects
- item effects when relevant
- fainted Pokémon
- battle history
- active Pokémon on both sides

Python has already calculated type effectiveness using a separate type chart.
You must use the provided type-effectiveness information.
Do not invent or override type effectiveness.

The player should NOT need to input:
- damage values
- move accuracy
- move effects
- ability effects
- item effects

The player must be able to see:
- the active player Pokémon and its current HP
- the active opponent Pokémon and its current HP
- the player move used
- the AI move used
- damage dealt by each move
- whether each move was super effective, not very effective, immune, or normal effectiveness
- whether a move missed
- whether a Pokémon fainted

Do not print the HP of benched Pokémon unless the player must choose a replacement after one of their Pokémon faints.

Protect / Detect rule:
- Protect and Detect have 100% success chance the first time they are used.
- Each consecutive usage in a row increases the chance of failure by a multiplier of 3.
- The failure chance should be handled internally.
- Do NOT reveal the hidden success/failure probability to the player.
- If a Pokémon uses a move that is NOT Protect or Detect, reset that Pokémon's consecutive Protect/Detect counter.
- The same applies separately to the AI Pokémon.

Fainting and switching rule:
- If the active player Pokémon reaches 0 HP, it faints.
- If the active opponent Pokémon reaches 0 HP, it faints.
- A fainted Pokémon cannot keep battling.
- The side with the fainted Pokémon must switch to another Pokémon with HP greater than 0.
- The player chooses their replacement manually.
- The AI may choose its own replacement.
- Do not choose a fainted Pokémon as the next active Pokémon.

Player move damage rule:
- Python has already calculated the player's move damage.
- You must use the provided Python-calculated player move damage.
- Do not invent a different damage number for the player's move.
- The player's damage is move_power multiplied by type_multiplier.
- The move_power must stay the same as the value listed in the player's team.
- Only return the provided damage value in player_move_result["damage"].

AI move-selection rule:
- If the active AI Pokémon has one or more super effective damaging moves against the active player Pokémon, strongly prefer one of those moves.
- A super effective move has a type multiplier greater than 1.
- If there are no super effective moves, choose the best available move based on damage, accuracy, role, status effects, strategy, and battle situation.
- Do not claim that a move is super effective unless Python marks it as super effective below.

Type-effectiveness and AI move selection rules:
- Python has already calculated the AI move options against the active player Pokémon.
- Use the provided AI move options exactly.
- Do not override the provided type_multiplier values.
- x2 or greater means super effective.
- x0.5 or less means not very effective.
- x0 means no effect.
- x1 means normal effectiveness.
- For dual-type Pokémon, Python has already multiplied the effectiveness against each defender type.
- If the AI has one or more moves with type_multiplier greater than 1, prefer a super-effective move.
- If multiple moves are super effective, prefer the move with the best combination of power, accuracy, and useful effects.
- If no move is super effective, choose the best strategic move.
- Avoid moves with type_multiplier 0 unless there is no useful alternative.
- Keep and use each move's power value.
- A move with power 0 is usually a status move and should not deal direct damage unless its effect says otherwise.
Current player team:
{json.dumps(player_team, indent=2)}

Current opponent team:
{json.dumps(opponent_team, indent=2)}

Active player Pokémon index:
{active_player_index}

Active opponent Pokémon index:
{active_opponent_index}

Player selected move:
{player_move}
Python-calculated player move damage:
{json.dumps(player_move_damage_info, indent=2)}

AI calculated move options against the active player Pokémon:
{json.dumps(ai_move_options, indent=2)}

AI move effectiveness against the active player Pokémon:
{json.dumps(ai_move_effectiveness, indent=2)}

AI super effective move options:
{json.dumps(ai_super_effective_moves, indent=2)}

Protect / Detect tracker:
{json.dumps(protect_detect_tracker, indent=2)}

Battle history:
{json.dumps(battle_history, indent=2)}

Your job:
1. Choose the AI's move.
2. Strongly prefer a super effective AI move if one is available.
3. Resolve the player's move.
4. Resolve the AI's move.
5. Apply damage, accuracy, move effects, ability effects, and item effects.
6. Use the Python-provided type-effectiveness result.
7. Update HP values.
8. Update Protect / Detect tracker.
9. Return the full result as valid JSON only.


Return JSON in this exact structure:

{{
  "active_player_index": 0,
  "active_opponent_index": 0,

  "player_move": {{}},
  "ai_move": {{}},

  "player_move_result": {{
    "hit": true,
    "damage": 0,
    "type_multiplier": 1,
    "effectiveness": "normal effectiveness",
    "message": ""
  }},

  "ai_move_result": {{
    "hit": true,
    "damage": 0,
    "type_multiplier": 1,
    "effectiveness": "normal effectiveness",
    "message": ""
  }},

  "player_team": [],
  "opponent_team": [],

  "protect_detect_tracker": {{}},

  "fainted": {{
    "player_pokemon_fainted": false,
    "opponent_pokemon_fainted": false
  }},

  "visible_turn_summary": "",
  "battle_over": false,
  "player_won": false
}}

Only return valid JSON.
Do not include markdown.
Do not include explanations outside the JSON.
""".strip()

    response = client.responses.create(
        model="gpt-5.3-codex",
        input=prompt
    )

    return json.loads(response.output_text)
