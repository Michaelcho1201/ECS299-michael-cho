player_team = [
    {
        "name": "Pikachu",
        "item": "Light Ball",
        "ability": "Static",
        "nature": "Timid",
        "moves": ["Thunderbolt", "Quick Attack", "Iron Tail", "Electro Ball"]
    },
    {
        "name": "Charizard",
        "item": "Charcoal",
        "ability": "Blaze",
        "nature": "Modest",
        "moves": ["Flamethrower", "Air Slash", "Dragon Claw", "Slash"]
    },
    {
        "name": "Blastoise",
        "item": "Mystic Water",
        "ability": "Torrent",
        "nature": "Bold",
        "moves": ["Water Pulse", "Bite", "Protect", "Rapid Spin"]
    },
    {
        "name": "Venusaur",
        "item": "Miracle Seed",
        "ability": "Overgrow",
        "nature": "Calm",
        "moves": ["Razor Leaf", "Sleep Powder", "Leech Seed", "Vine Whip"]
    },
    {
        "name": "Lucario",
        "item": "Black Belt",
        "ability": "Inner Focus",
        "nature": "Adamant",
        "moves": ["Aura Sphere", "Metal Claw", "Quick Attack", "Detect"]
    },
    {
        "name": "Snorlax",
        "item": "Leftovers",
        "ability": "Immunity",
        "nature": "Careful",
        "moves": ["Body Slam", "Rest", "Crunch", "Heavy Slam"]
    }
]

def show_player_team():
    print("Player Team:")
    for i in range(len(player_team)):
        pokemon = player_team[i]
        print(str(i + 1) + ". " + pokemon["name"])
        print("   Item: " + pokemon["item"])
        print("   Ability: " + pokemon["ability"])
        print("   Nature: " + pokemon["nature"])
        print("   Moves: " + str(pokemon["moves"]))
