from player_team import player_team
from llm_battle_controller import resolve_turn_with_llm
from type_chart import calculate_move_options, calculate_damage

def show_active_hp(player_team, opponent_team, active_player_index, active_opponent_index):
    active_player = player_team[active_player_index]
    active_opponent = opponent_team[active_opponent_index]

    print()
    print("========== ACTIVE POKÉMON HP ==========")
    print(
        "Player: "
        + active_player["name"]
        + " - "
        + str(active_player["current_hp"])
        + "/"
        + str(active_player["max_hp"])
        + " HP"
    )

    print(
        "Opponent: "
        + active_opponent["name"]
        + " - "
        + str(active_opponent["current_hp"])
        + "/"
        + str(active_opponent["max_hp"])
        + " HP"
    )
    print()


def choose_player_move(active_player):
    print("Your active Pokémon: " + active_player["name"])
    print("Choose a move:")

    for i, move in enumerate(active_player["moves"]):
        print(
            str(i + 1)
            + ". "
            + move["name"]
            + " | Type: "
            + move["type"]
            + " | Power: "
            + str(move["power"])
        )

    choice = input("Move number: ")
    move_index = int(choice) - 1

    return active_player["moves"][move_index]


def has_available_pokemon(team):
    for pokemon in team:
        if pokemon["current_hp"] > 0:
            return True

    return False


def choose_player_switch(player_team):
    print()
    print("Your Pokémon fainted. Choose a new Pokémon:")

    available_indices = []

    for i, pokemon in enumerate(player_team):
        if pokemon["current_hp"] > 0:
            available_indices.append(i)
            print(
                str(i + 1)
                + ". "
                + pokemon["name"]
                + " - "
                + str(pokemon["current_hp"])
                + "/"
                + str(pokemon["max_hp"])
                + " HP"
            )

    while True:
        choice = input("Choose Pokémon number: ")

        try:
            new_index = int(choice) - 1

            if new_index in available_indices:
                return new_index
            else:
                print("That Pokémon is fainted or invalid. Choose another Pokémon.")

        except ValueError:
            print("Please enter a valid number.")


def choose_ai_switch(opponent_team):
    print()
    print("Opponent Pokémon fainted. AI is choosing a new Pokémon.")

    for i, pokemon in enumerate(opponent_team):
        if pokemon["current_hp"] > 0:
            print("AI switched to " + pokemon["name"] + ".")
            return i

    return None


def run_battle(opponent_team, difficulty_level):
    battle_history = []

    active_player_index = 0
    active_opponent_index = 0

    protect_detect_tracker = {
        "player": {
            "consecutive_uses": 0,
            "last_move_was_protect_or_detect": False
        },
        "opponent": {
            "consecutive_uses": 0,
            "last_move_was_protect_or_detect": False
        }
    }

    battle_over = False
    player_won = False
    turn_count = 0

    print("Battle started.")

    while battle_over == False:
        turn_count = turn_count + 1

        print()
        print("===================================")
        print("Turn " + str(turn_count))
        print("===================================")

        show_active_hp(
            player_team,
            opponent_team,
            active_player_index,
            active_opponent_index
        )

        active_player = player_team[active_player_index]
        active_opponent = opponent_team[active_opponent_index]

        print("Active Player Pokémon: " + active_player["name"])
        print("Active Opponent Pokémon: " + active_opponent["name"])
        print()

        player_move = choose_player_move(active_player)

        player_move_damage_info = calculate_damage(
            player_move,
            active_opponent
        )

        ai_move_options = calculate_move_options(
            active_opponent,
            active_player
        )

        turn_result = resolve_turn_with_llm(
            player_team,
            opponent_team,
            active_player_index,
            active_opponent_index,
            player_move,
            player_move_damage_info,
            ai_move_options,
            battle_history,
            protect_detect_tracker
        )

        active_player_index = turn_result["active_player_index"]
        active_opponent_index = turn_result["active_opponent_index"]

        player_team[:] = turn_result["player_team"]
        opponent_team[:] = turn_result["opponent_team"]

        protect_detect_tracker = turn_result["protect_detect_tracker"]

        battle_over = turn_result["battle_over"]
        player_won = turn_result["player_won"]

        print()
        print("========== TURN RESULT ==========")
        print(turn_result["visible_turn_summary"])

        print()
        print("Player used: " + turn_result["player_move"]["name"])
        print("AI used: " + turn_result["ai_move"]["name"])

        
        print()
        print("Player move damage: " + str(turn_result["player_move_result"]["damage"]))
        print("Player move multiplier: x" + str(turn_result["player_move_result"]["type_multiplier"]))
        print("Player move effectiveness: " + turn_result["player_move_result"]["effectiveness"])
        print(turn_result["player_move_result"]["message"])

        print()
        print("AI move damage: " + str(turn_result["ai_move_result"]["damage"]))
        print("AI move multiplier: x" + str(turn_result["ai_move_result"]["type_multiplier"]))
        print("AI move effectiveness: " + turn_result["ai_move_result"]["effectiveness"])
        print(turn_result["ai_move_result"]["message"])

        show_active_hp(
            player_team,
            opponent_team,
            active_player_index,
            active_opponent_index
        )

        battle_history.append(turn_result)

        active_player = player_team[active_player_index]
        active_opponent = opponent_team[active_opponent_index]

        if active_player["current_hp"] <= 0:
            active_player["current_hp"] = 0

            if has_available_pokemon(player_team):
                active_player_index = choose_player_switch(player_team)
            else:
                print("All player Pokémon have fainted.")
                battle_over = True
                player_won = False

        if active_opponent["current_hp"] <= 0:
            active_opponent["current_hp"] = 0

            if has_available_pokemon(opponent_team):
                active_opponent_index = choose_ai_switch(opponent_team)
            else:
                print("All opponent Pokémon have fainted.")
                battle_over = True
                player_won = True

    return {
        "player_won": player_won,
        "moves": turn_count
    }
