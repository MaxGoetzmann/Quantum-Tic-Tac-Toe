"""
"""

import sys
import time
import jsonpickle
from game import Game
from player_move import PlayerMove, MoveType

CYCLE = 1
# board_out = [
#             [None, None, None],
#             [None, None, None],
#             [None, None, None],
# ]
# game_out = {}
# player_won = ""
# player_turn = ""
# move_success = False


def get_player_moves(game: Game):
    """
    Prompt console loop for requesting player move types and positions.
    """
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

            assert 0 <= row <= 2 and 0 <= col <= 2

            real_move = PlayerMove(
                PlayerMove.match_abbr_to_move(move),
                (row, col), game.get_current_player(),
                game.get_current_player())

            assert game.is_valid_move(real_move)

            game.apply_move(real_move)

        except:
            print("Input is wrong.")

        time.sleep(CYCLE)


def make_move(game: Game, move: MoveType, row: int, col: int):
    """
    Debugging application of the fields of a move. 
    """
    test_move = PlayerMove(move, (row, col),
                           game.get_current_player(), game.get_current_turn())
    game.apply_move(test_move)
    print(game)


def test(game):
    """
    Debugging test scenarios for game.
    """
    make_move(game, MoveType.ZGATE, 0, 1)
    make_move(game, MoveType.NOTGATE, 0, 2)
    make_move(game, MoveType.ZGATE, 2, 2)
    make_move(game, MoveType.PLACE_SUPERPOS, 1, 0)


def handle_pyodide():
    """
    Read in set pyodide fields and output fields used by web. Fields originating from JavaScript 
    must be in the global scope and cannot be overwritten by placeholder Python variables.
    """
    # Is initial call to setup the gameboard with no player move?
    global pyodide_first_pass

    # Board returned to client. Simple one-char representation.
    global board_out

    # Full jsonpickle encoded representation of game. Repassed into script to save game state.
    global game_out

    # Was the move the player submitted legal?
    global move_success

    ### TODO: just parse the game state dict in JS of the fields below ###
    # If populated, there is a game winner.
    global player_won

    # X or O of the current player's turn.
    global player_turn

    game = None
    if pyodide_first_pass:
        print("first pass")
        game = Game()
    else:
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
        else:
            move_success = False
    player_turn = game.get_current_player().get_selection()
    board_out = game.nice_dump()
    game_out = jsonpickle.encode(game)


def play_game():
    """
    Driver function to boot game based on environment.
    """

    # Handle web pyodide deployment.
    if "pyodide" in sys.modules:
        handle_pyodide()
        return

    # Test locally via console.
    game = Game()
    test(game)
    dump = jsonpickle.encode(game)
    print(dump)
    new_g = jsonpickle.decode(dump)
    print(new_g)
    print(game.board.str_arr())
    get_player_moves(game)


play_game()
