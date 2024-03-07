import sys
import time
import json
import jsonpickle
from game import Game
from player_move import PlayerMove, MoveType

CYCLE = 0.4
pyodide_move = {}
board_out = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
]
game_out = {}
game_in = {}


def get_json(obj):
    return json.loads(
        json.dumps(obj, default=lambda o: getattr(o, '__dict__', str(o)))
    )


def get_player_moves(game: Game):
    while True:
        if game.is_game_over():
            break

        try:
            print(game)
            move = input(
                f"Player {game.get_current_player()}, enter your move's type: ")
            row = int(
                input(f"Player {game.get_current_player()}, enter your move's row (0-2): "))
            col = int(
                input(f"Player {game.get_current_player()}, enter your move's column (0-2): "))

            assert row >= 0 and row <= 2 and col >= 0 and col <= 2

            real_move = PlayerMove(
                PlayerMove.match_abbr_to_move(move), (row, col), game.get_current_player(), game.get_current_player())

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


def handle_pyodide():
    # restored_game = jsons.load(game_in, Game)
    clean_type = PlayerMove.match_abbr_to_move(pyodide_move["type"])
    clean_move = PlayerMove(
        clean_type, (pyodide_move["row"], pyodide_move["col"]), restored_game.get_current_player(), restored_game.get_current_turn())
    restored_game.is_valid_move(clean_move)


def play_game():
    game = Game()
    test(game)
    if "pyodide" in sys.modules:
        handle_pyodide()
    else:
        # dump = get_json(game)
        # print(dump)
        # new_g = Game(dump)
        # print(new_g)
        dump = jsonpickle.encode(game)
        print(dump)
        new_g = jsonpickle.decode(dump)
        print(new_g)
        print(game.board.nice_dump())
        get_player_moves(game)


if __name__ == "__main__":
    print("IN THE MAIN FUNCTION")
    play_game()
