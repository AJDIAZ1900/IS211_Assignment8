import random
import time
import argparse

# -------------------- Player Classes --------------------

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def take_turn(self, game):
        pass


class HumanPlayer(Player):
    def take_turn(self, game):
        turn_total = 0
        while True:
            choice = input(f"{self.name}, roll or hold? (r/h): ").lower()
            if choice == 'r':
                roll = game.roll_dice()
                print(f"{self.name} rolled {roll}")
                if roll == 1:
                    print("Turn over. No points.")
                    return 0
                else:
                    turn_total += roll
                    print(f"Turn total: {turn_total}")
            else:
                return turn_total


class ComputerPlayer(Player):
    def take_turn(self, game):
        turn_total = 0
        hold_value = min(25, 100 - self.score)

        while turn_total < hold_value:
            roll = game.roll_dice()
            print(f"{self.name} rolled {roll}")

            if roll == 1:
                print(f"{self.name} loses turn.")
                return 0
            else:
                turn_total += roll

        print(f"{self.name} holds with {turn_total}")
        return turn_total


# -------------------- Factory Pattern --------------------

class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type")


# -------------------- Game Class --------------------

class Game:
    def __init__(self, player1_type, player2_type):
        self.player1 = PlayerFactory.create_player(player1_type, "Player 1")
        self.player2 = PlayerFactory.create_player(player2_type, "Player 2")
        self.current_player = self.player1

    def roll_dice(self):
        return random.randint(1, 6)

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def play(self):
        while self.player1.score < 100 and self.player2.score < 100:
            print(f"\n{self.current_player.name}'s turn")
            turn_score = self.current_player.take_turn(self)
            self.current_player.score += turn_score

            print(f"{self.current_player.name} total score: {self.current_player.score}")

            if self.current_player.score >= 100:
                print(f"{self.current_player.name} wins!")
                return

            self.switch_player()


# -------------------- Proxy Pattern --------------------

class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.start_time = time.time()

    def play(self):
        while self.game.player1.score < 100 and self.game.player2.score < 100:
            if time.time() - self.start_time >= 60:
                print("\nTime is up!")
                if self.game.player1.score > self.game.player2.score:
                    print("Player 1 wins by score!")
                elif self.game.player2.score > self.game.player1.score:
                    print("Player 2 wins by score!")
                else:
                    print("It's a tie!")
                return

            player = self.game.current_player
            print(f"\n{player.name}'s turn")

            turn_score = player.take_turn(self.game)
            player.score += turn_score

            print(f"{player.name} total score: {player.score}")

            if player.score >= 100:
                print(f"{player.name} wins!")
                return

            self.game.switch_player()


# -------------------- Main --------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--player1", required=True)
    parser.add_argument("--player2", required=True)
    parser.add_argument("--timed", action="store_true")

    args = parser.parse_args()

    game = Game(args.player1, args.player2)

    if args.timed:
        game = TimedGameProxy(game)

    game.play()


if __name__ == "__main__":
    main()
