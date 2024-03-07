import sys
import time
import json
import jsonpickle
from game import Game
from player_move import PlayerMove, MoveType

CYCLE = 1
board_out = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
]
game_out = {}
player_won = ""
move_success = False


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

        time.sleep(CYCLE)


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
    global pyodide_first_pass, board_out, game_out, player_won, move_success
    game = None
    if pyodide_first_pass:
        print("first pass")
        game = Game()
        test(game)
        board_out = game.nice_dump()
        game_out = jsonpickle.encode(game)
        return

    print("second pass attempting to load", game_in)
    game: Game = jsonpickle.decode(game_in)
    print(pyodide_move)
    clean_type = PlayerMove.match_abbr_to_move(pyodide_move["type"])
    clean_move = PlayerMove(
        clean_type,
        (pyodide_move["row"],
         pyodide_move["col"]),
        game.get_current_player(),
        game.get_current_turn())
    if game.is_valid_move(clean_move):
        move_success = True
        game.apply_move(clean_move)
        if game.is_game_over():
            player_won = game.check_win().get_selection()
        board_out = game.nice_dump()
        game_out = jsonpickle.encode(game)
    else:
        move_success = False


def play_game():
    if "pyodide" in sys.modules:
        handle_pyodide()
        return

    game = Game()
    test(game)
    dump = jsonpickle.encode(game)
    print(dump)
    new_g = jsonpickle.decode(dump)
    print(new_g)
    print(game.board.nice_dump())
    get_player_moves(game)


play_game()
