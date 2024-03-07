import time
from game import Game
from player_move import PlayerMove, MoveType

CYCLE = 0.4
pyodide_move = {}


def initialize_board():
    return [[" " for _ in range(3)] for _ in range(3)]


def validate_move(row, col):
    return type(row) == int and type(col) == int \
        and row >= 0 and col >= 0 \
        and row <= 2 and col <= 2


def get_player_moves(game: Game):
    move_validator = {i.value: i.name for i in MoveType}
    while True:
        if game.is_game_over():
            break

        try:
            print(game)
            move = int(input(
                f"Player {game.get_current_player()}, enter your move's type (0-4): "))
            row = int(
                input(f"Player {game.get_current_player()}, enter your move's row (0-2): "))
            col = int(
                input(f"Player {game.get_current_player()}, enter your move's column (0-2): "))

            assert row >= 0 and row <= 2 and col >= 0 and col <= 2 and move in move_validator

            real_move = PlayerMove(
                move_validator[move], (row, col), game.get_current_player(), game.get_current_player())

            assert game.is_valid_move(real_move)

            game.apply_move(real_move)

        except:
            print("Input is wrong.")

        time.sleep(1)


def make_move(game, type, row, col):
    test_move = PlayerMove(type, (row, col),
                           game.get_current_player(), game.get_current_turn())
    game.apply_move(test_move)
    print(game)


def test(game):
    make_move(game, MoveType.ZGATE, 0, 1)
    make_move(game, MoveType.NOTGATE, 0, 2)
    make_move(game, MoveType.ZGATE, 2, 2)
    make_move(game, MoveType.PLACE_SUPERPOS, 1, 0)


def play_game():
    game = Game()
    test(game)
    get_player_moves(game)


if __name__ == "__main__":
    print("IN THE MAIN FUNCTION")
    play_game()
