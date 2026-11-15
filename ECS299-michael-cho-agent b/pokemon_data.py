import json
import os
import requests

CACHE_FILE = "pokemon_cache.json"
POKEAPI_BASE = "https://pokeapi.co/api/v2"


def pokemon_can_learn_move(pokemon_name, move_name):
    move_data = fetch_move_data(move_name)
    pokemon_key = normalize_name(pokemon_name)

    for pokemon in move_data["learned_by_pokemon"]:
        if pokemon["name"] == pokemon_key:
            return True

    return False


def validate_player_team_basic(player_team):
    errors = []

    for pokemon in player_team:
        name = pokemon["name"]

        try:
            official_types = get_pokemon_types(name)
        except ValueError:
            errors.append(name + " is not a valid Pokémon.")
            continue

        if pokemon["types"] != official_types:
            errors.append(
                name
                + " has incorrect typing. Expected "
                + str(official_types)
                + " but got "
                + str(pokemon["types"])
            )

        for move in pokemon["moves"]:
            move_name = move["name"]

            try:
                can_learn = pokemon_can_learn_move(name, move_name)

                if not can_learn:
                    errors.append(name + " cannot legally learn " + move_name + ".")

            except ValueError:
                errors.append(move_name + " is not a valid move.")

    return errors
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    return {
        "pokemon": {},
        "moves": {}
    }


def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(cache, file, indent=2)


def normalize_name(name):
    return name.lower().replace(" ", "-")


def fetch_pokemon_data(pokemon_name):
    cache = load_cache()
    key = normalize_name(pokemon_name)

    if key in cache["pokemon"]:
        return cache["pokemon"][key]

    response = requests.get(f"{POKEAPI_BASE}/pokemon/{key}")

    if response.status_code != 200:
        raise ValueError("Could not find Pokémon data for: " + pokemon_name)

    data = response.json()
    cache["pokemon"][key] = data
    save_cache(cache)

    return data


def fetch_move_data(move_name):
    cache = load_cache()
    key = normalize_name(move_name)

    if key in cache["moves"]:
        return cache["moves"][key]

    response = requests.get(f"{POKEAPI_BASE}/move/{key}")

    if response.status_code != 200:
        raise ValueError("Could not find move data for: " + move_name)

    data = response.json()
    cache["moves"][key] = data
    save_cache(cache)

    return data


def get_pokemon_types(pokemon_name):
    data = fetch_pokemon_data(pokemon_name)

    types = []

    for type_slot in data["types"]:
        type_name = type_slot["type"]["name"].title()
        types.append(type_name)

    return types


def get_base_stats(pokemon_name):
    data = fetch_pokemon_data(pokemon_name)

    stats = {}

    for stat_entry in data["stats"]:
        stat_name = stat_entry["stat"]["name"]
        base_stat = stat_entry["base_stat"]
        stats[stat_name] = base_stat

    return stats


def calculate_level_50_hp(base_hp, iv=31, ev=0):
    return int(((2 * base_hp + iv + (ev // 4)) * 50) / 100) + 50 + 10


def calculate_level_50_other_stat(base_stat, nature_multiplier=1.0, iv=31, ev=0):
    raw_stat = int(((2 * base_stat + iv + (ev // 4)) * 50) / 100) + 5
    return int(raw_stat * nature_multiplier)


def get_level_50_stats(pokemon_name):
    base_stats = get_base_stats(pokemon_name)

    hp = calculate_level_50_hp(base_stats["hp"])

    return {
        "hp": hp,
        "attack": calculate_level_50_other_stat(base_stats["attack"]),
        "defense": calculate_level_50_other_stat(base_stats["defense"]),
        "special_attack": calculate_level_50_other_stat(base_stats["special-attack"]),
        "special_defense": calculate_level_50_other_stat(base_stats["special-defense"]),
        "speed": calculate_level_50_other_stat(base_stats["speed"])
    }


def get_move_info(move_name):
    data = fetch_move_data(move_name)

    effect_text = ""

    for entry in data["effect_entries"]:
        if entry["language"]["name"] == "en":
            effect_text = entry["short_effect"]
            break

    move_info = {
        "name": data["name"].replace("-", " ").title(),
        "type": data["type"]["name"].title(),
        "power": data["power"] if data["power"] is not None else 0,
        "accuracy": data["accuracy"],
        "effect_chance": data["effect_chance"],
        "damage_class": data["damage_class"]["name"],
        "effect": effect_text
    }

    return move_info