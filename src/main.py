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
    while True:
        try:
            move = int(
                input(f"Player {game.get_current_player()}, enter your move's type (0-4): "))
            row = int(
                input(f"Player {game.get_current_player()}, enter your move's row (1-3): ")) - 1
            col = int(
                input(f"Player {game.get_current_player()}, enter your move's column (1-3): ")) - 1

            assert row >= 0 and row <= 2 and col >= 0 and col <= 2 and move in MoveType

            real_move = PlayerMove(
                move, (row, col), game.get_current_player(), game.get_current_player())

            if board[row][col] == " ":
                return row, col
            else:
                print("This position is already taken. Please try another one.")
        except:
            print("Input is wrong.")


def play_game():
    game = Game()
    game.print_board()
    get_player_moves(game)

    # while True:
    #     print(pyodide_move)

    #     # Don't infinite loop which upsets computer.
    #     if "unload" in pyodide_move:
    #         break

    #     time.sleep(CYCLE)


if __name__ == "__main__":
    print("IN THE MAIN FUNCTION")
    play_game()
