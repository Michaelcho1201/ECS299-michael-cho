from diffculty import adjust_difficulty
from diffculty import generate_pokemon_team
from battle_loop import run_battle

def start_game():
    difficulty_level = 0
    keep_playing = True

    while keep_playing:
        opponent_team = generate_pokemon_team(difficulty_level)

        battle_result = run_battle(opponent_team, difficulty_level)

        difficulty_level = adjust_difficulty(
            difficulty_level,
            battle_result.player_won,
            battle_result.turn_count
        )

        print("New difficulty level: " + str(difficulty_level))

        answer = input("Play another battle? yes/no: ")

        if answer != "yes":
            keep_playing = False

start_game()