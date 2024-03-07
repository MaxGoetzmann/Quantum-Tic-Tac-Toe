"""Game"""

from typing import Union
from board import Board
from player import Player, PlayerPiece
from player_move import PlayerMove, MoveType
from piece import Piece
from gate import Gate, GateType


class Game():

    board: Board
    players: tuple[Player]
    turn: int
    current_player: Player
    game_ended: bool

    def __init__(self, first: Union[PlayerPiece, None] = None) -> None:
        # Decide first player, with X being the default.
        if first == PlayerPiece.O:
            self.players = (Player(PlayerPiece.O, True),
                            Player(PlayerPiece.X, False))
        else:
            self.players = (Player(PlayerPiece.X, True),
                            Player(PlayerPiece.O, False))

        self.current_player = self.players[0]
        self.board = Board()
        self.turn = 1
        self.game_ended = False

    def is_valid_move(self, move: PlayerMove) -> bool:
        """
        Reject move if trying to place piece on already existing one.
        """
        piece_on_piece = move.is_place() and self.board.is_piece(move.get_target())
        gate_on_gate = move.is_gate() and self.board.is_gate(move.get_target())
        return not (piece_on_piece or gate_on_gate)

    def get_player_from_piece(self, piece: PlayerPiece) -> Player:
        if piece == self.players[0].get_selection():
            return self.players[0]
        return self.players[1]

    def check_win(self) -> Union[Player, None]:
        """
        """

        win_conditions = [
            [self.board.get_owner((0, 0)), self.board.get_owner(
                (0, 1)), self.board.get_owner((0, 2))],
            [self.board.get_owner((1, 0)), self.board.get_owner(
                (1, 1)), self.board.get_owner((1, 2))],
            [self.board.get_owner((2, 0)), self.board.get_owner(
                (2, 1)), self.board.get_owner((2, 2))],
            [self.board.get_owner((0, 0)), self.board.get_owner(
                (1, 0)), self.board.get_owner((2, 0))],
            [self.board.get_owner((0, 1)), self.board.get_owner(
                (1, 1)), self.board.get_owner((2, 1))],
            [self.board.get_owner((0, 2)), self.board.get_owner(
                (1, 2)), self.board.get_owner((2, 2))],
            [self.board.get_owner((0, 0)), self.board.get_owner(
                (1, 1)), self.board.get_owner((2, 2))],
            [self.board.get_owner((2, 0)), self.board.get_owner(
                (1, 1)), self.board.get_owner((0, 2))],
        ]

        for cond in win_conditions:
            if (cond[0] == cond[1] == cond[2]) and (cond[0] is not None):
                return self.get_player_from_piece(cond[0])

        return None

    def get_current_player(self) -> Player:
        return self.current_player

    def get_current_turn(self) -> int:
        return self.turn

    def apply_move(self, move: PlayerMove) -> None:
        assert self.is_valid_move(move)

        print(move)

        # Do move for gate on piece
        if self.board.is_piece(move.get_target()):
            sq: Piece = self.board.get_square(move.get_target())
            if move.get_type() == MoveType.HGATE:
                sq.h_gate()
            elif move.get_type() == MoveType.ZGATE:
                sq.z_gate()
            elif move.get_type() == MoveType.NOTGATE:
                sq.not_gate()
        # Do move for piece on gate
        elif self.board.is_gate(move.get_target()):
            piece = Piece(self.current_player.get_selection(),
                          move.get_type() == MoveType.PLACE_SUPERPOS)
            gate: Gate = self.board.get_square(move.get_target())
            piece.any_gate(gate.mat())
            self.board.place(piece, move.get_target())
        # Do move for empty square
        else:
            sq = None
            if move.is_gate():
                if move.get_type() == MoveType.HGATE:
                    sq = Gate(GateType.H)
                elif move.get_type() == MoveType.NOTGATE:
                    sq = Gate(GateType.NOT)
                elif move.get_type() == MoveType.ZGATE:
                    sq = Gate(GateType.Z)
            else:
                sq = Piece(self.current_player.get_selection(),
                           move.get_type() == MoveType.PLACE_SUPERPOS)
            self.board.place(sq, move.get_target())

        # Check win
        winner = self.check_win()
        if winner:
            self.end_game(winner)
            return

        # Pass turn
        self.turn += 1
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def end_game(self, winner: Player) -> None:
        print(f"Player {winner} wins!!!")
        self.game_ended = True

    def is_game_over(self) -> bool:
        return self.game_ended

    def __str__(self) -> str:
        return str(self.board)
