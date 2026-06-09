from type_chart import get_type_multiplier, describe_effectiveness


def analyze_move_effectiveness(move, defender):
    attack_type = move["type"]
    defender_types = defender["types"]

    multiplier = get_type_multiplier(attack_type, defender_types)

    return {
        "move_name": move["name"],
        "move_type": attack_type,
        "move_power": move["power"],
        "defender": defender["name"],
        "defender_types": defender_types,
        "multiplier": multiplier,
        "effectiveness": describe_effectiveness(multiplier)
    }


def analyze_all_moves(attacker, defender):
    results = []

    for move in attacker["moves"]:
        result = analyze_move_effectiveness(move, defender)
        results.append(result)

    return results


def get_super_effective_moves(attacker, defender):
    results = analyze_all_moves(attacker, defender)

    super_effective_moves = []

    for result in results:
        if result["multiplier"] > 1:
            super_effective_moves.append(result)

    return super_effective_moves