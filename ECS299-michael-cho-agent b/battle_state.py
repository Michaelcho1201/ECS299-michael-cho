class BattleState:
    def __init__(self, player_team, opponent_team_text, difficulty_level):
        self.player_team = player_team
        self.opponent_team_text = opponent_team_text
        self.difficulty_level = difficulty_level
        self.turn_count = 0
        self.player_won = False
        self.battle_over = False

    def increase_turn(self):
        self.turn_count = self.turn_count + 1

    def end_battle(self, player_won):
        self.player_won = player_won
        self.battle_over = True

    def get_state_text(self):
        return (
        "Current Difficulty: " + str(self.difficulty_level) + "\n" +
        "Turns Taken: " + str(self.turn_count) + "\n" +
        "Battle Over: " + str(self.battle_over) + "\n" +
        "Player Won: " + str(self.player_won)
    )