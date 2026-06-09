TYPE_CHART = {
    "Normal": {
        "super_effective": [],
        "not_very_effective": ["Rock", "Steel"],
        "no_effect": ["Ghost"]
    },
    "Fire": {
        "super_effective": ["Grass", "Ice", "Bug", "Steel"],
        "not_very_effective": ["Fire", "Water", "Rock", "Dragon"],
        "no_effect": []
    },
    "Water": {
        "super_effective": ["Fire", "Ground", "Rock"],
        "not_very_effective": ["Water", "Grass", "Dragon"],
        "no_effect": []
    },
    "Electric": {
        "super_effective": ["Water", "Flying"],
        "not_very_effective": ["Electric", "Grass", "Dragon"],
        "no_effect": ["Ground"]
    },
    "Grass": {
        "super_effective": ["Water", "Ground", "Rock"],
        "not_very_effective": ["Fire", "Grass", "Poison", "Flying", "Bug", "Dragon", "Steel"],
        "no_effect": []
    },
    "Ice": {
        "super_effective": ["Grass", "Ground", "Flying", "Dragon"],
        "not_very_effective": ["Fire", "Water", "Ice", "Steel"],
        "no_effect": []
    },
    "Fighting": {
        "super_effective": ["Normal", "Ice", "Rock", "Dark", "Steel"],
        "not_very_effective": ["Poison", "Flying", "Psychic", "Bug", "Fairy"],
        "no_effect": ["Ghost"]
    },
    "Poison": {
        "super_effective": ["Grass", "Fairy"],
        "not_very_effective": ["Poison", "Ground", "Rock", "Ghost"],
        "no_effect": ["Steel"]
    },
    "Ground": {
        "super_effective": ["Fire", "Electric", "Poison", "Rock", "Steel"],
        "not_very_effective": ["Grass", "Bug"],
        "no_effect": ["Flying"]
    },
    "Flying": {
        "super_effective": ["Grass", "Fighting", "Bug"],
        "not_very_effective": ["Electric", "Rock", "Steel"],
        "no_effect": []
    },
    "Psychic": {
        "super_effective": ["Fighting", "Poison"],
        "not_very_effective": ["Psychic", "Steel"],
        "no_effect": ["Dark"]
    },
    "Bug": {
        "super_effective": ["Grass", "Psychic", "Dark"],
        "not_very_effective": ["Fire", "Fighting", "Poison", "Flying", "Ghost", "Steel", "Fairy"],
        "no_effect": []
    },
    "Rock": {
        "super_effective": ["Fire", "Ice", "Flying", "Bug"],
        "not_very_effective": ["Fighting", "Ground", "Steel"],
        "no_effect": []
    },
    "Ghost": {
        "super_effective": ["Psychic", "Ghost"],
        "not_very_effective": ["Dark"],
        "no_effect": ["Normal"]
    },
    "Dragon": {
        "super_effective": ["Dragon"],
        "not_very_effective": ["Steel"],
        "no_effect": ["Fairy"]
    },
    "Dark": {
        "super_effective": ["Psychic", "Ghost"],
        "not_very_effective": ["Fighting", "Dark", "Fairy"],
        "no_effect": []
    },
    "Steel": {
        "super_effective": ["Ice", "Rock", "Fairy"],
        "not_very_effective": ["Fire", "Water", "Electric", "Steel"],
        "no_effect": []
    },
    "Fairy": {
        "super_effective": ["Fighting", "Dragon", "Dark"],
        "not_very_effective": ["Fire", "Poison", "Steel"],
        "no_effect": []
    }
}


def get_single_type_multiplier(attack_type, defender_type):
    attack_type = attack_type.title()
    defender_type = defender_type.title()

    if attack_type not in TYPE_CHART:
        return 1

    chart = TYPE_CHART[attack_type]

    if defender_type in chart["no_effect"]:
        return 0

    if defender_type in chart["super_effective"]:
        return 2

    if defender_type in chart["not_very_effective"]:
        return 0.5

    return 1


def get_type_multiplier(attack_type, defender_types):
    total_multiplier = 1

    for defender_type in defender_types:
        single_multiplier = get_single_type_multiplier(attack_type, defender_type)
        total_multiplier = total_multiplier * single_multiplier

    return total_multiplier


def describe_effectiveness(multiplier):
    if multiplier == 0:
        return "no effect"
    elif multiplier > 1:
        return "super effective"
    elif multiplier < 1:
        return "not very effective"
    else:
        return "normal effectiveness"


def calculate_move_options(attacker, defender):
    """
    Calculates the type effectiveness of every move the attacker has
    against the defender.

    attacker format:
    {
        "name": "Pikachu",
        "types": ["Electric"],
        "moves": [
            {"name": "Thunderbolt", "type": "Electric", "power": 90}
        ]
    }

    defender format:
    {
        "name": "Charizard",
        "types": ["Fire", "Flying"]
    }
    """

    options = []

    defender_types = defender["types"]

    for move in attacker["moves"]:
        move_name = move["name"]
        move_type = move["type"]
        move_power = move["power"]

        multiplier = get_type_multiplier(move_type, defender_types)
        effectiveness = describe_effectiveness(multiplier)

        options.append({
            "name": move_name,
            "type": move_type,
            "power": move_power,
            "type_multiplier": multiplier,
            "effectiveness": effectiveness
        })

    return options
def calculate_damage(move, defender):
    move_type = move["type"]
    move_power = move["power"]
    defender_types = defender["types"]

    multiplier = get_type_multiplier(move_type, defender_types)
    damage = int(move_power * multiplier)

    return {
        "move_name": move["name"],
        "move_type": move_type,
        "move_power": move_power,
        "type_multiplier": multiplier,
        "damage": damage,
        "effectiveness": describe_effectiveness(multiplier)
    }