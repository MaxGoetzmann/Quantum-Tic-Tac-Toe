def initialize_board():
    return [[" " for _ in range(3)] for _ in range(3)]


def print_board(board):
    for row in board:
        print("|" + "|".join(row) + "|")


def check_win(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    return [player, player, player] in win_conditions


def check_tie(board):
    return all(all(cell != " " for cell in row) for row in board)


def validate_move(row, col):
    return type(row) == int and type(col) == int \
        and row >= 0 and col >= 0 \
        and row <= 2 and col <= 2


def get_player_move(board, player):
    while True:
        move = int(
            input(f"Player {player}, enter your move's type or number alias (1-3): ")) - 1
        )
        row = int(
            input(f"Player {player}, enter your move's row (1-3): ")) - 1
        col = int(
            input(f"Player {player}, enter your move's column (1-3): ")) - 1

        if not validate_move(row, col):
            print("Invalid move. Please try again.")
            continue

        if board[row][col] == " ":
            return row, col
        else:
            print("This position is already taken. Please try another one.")


def play_game():
    board = initialize_board()
    current_player = "X"
    while True:
        print_board(board)
        row, col = get_player_move(board, current_player)
        board[row][col] = current_player
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        if check_tie(board):
            print_board(board)
            print("It's a tie!")
            break
        current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
    play_game()