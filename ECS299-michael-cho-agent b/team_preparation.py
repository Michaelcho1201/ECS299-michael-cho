from pokemon_data import get_pokemon_types
from pokemon_data import get_level_50_stats
from pokemon_data import get_move_info


def prepare_generated_opponent_team(opponent_team):
    for pokemon in opponent_team:
        stats = get_level_50_stats(pokemon["name"])
        types = get_pokemon_types(pokemon["name"])

        pokemon["types"] = types

        pokemon["stats"] = {
            "attack": stats["attack"],
            "defense": stats["defense"],
            "special_attack": stats["special_attack"],
            "special_defense": stats["special_defense"],
            "speed": stats["speed"]
        }

        pokemon["max_hp"] = stats["hp"]
        pokemon["current_hp"] = stats["hp"]

        updated_moves = []

        for move in pokemon["moves"]:
            move_name = move["name"]

            try:
                move_info = get_move_info(move_name)
                updated_moves.append(move_info)
            except ValueError:
                updated_moves.append(move)

        pokemon["moves"] = updated_moves

    return opponent_team