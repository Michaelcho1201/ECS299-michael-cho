from diffculty import adjust_difficulty
from diffculty import generate_pokemon_team
from battle_loop import run_battle
from player_team import player_team


def reset_player_team_hp():
    for pokemon in player_team:
        pokemon["current_hp"] = pokemon["max_hp"]


def start_game():
    difficulty_level = 0
    keep_playing = True

    while keep_playing:
        reset_player_team_hp()

        opponent_team = generate_pokemon_team(difficulty_level)

        battle_result = run_battle(opponent_team, difficulty_level)

        difficulty_level = adjust_difficulty(
            difficulty_level,
            battle_result["player_won"],
            battle_result["moves"]
        )

        print("New difficulty level: " + str(difficulty_level))

        answer = input("Play another battle? yes/no: ")

        if answer != "yes":
            keep_playing = False


start_game()
