from szachownica import *


def is_hetman(row, col):
    row = int(row) - 1
    col = ord(col) - ord('A')
    if chessboard.board[row][col] == HETMAN:
        return True
    else:
        return False

def delete_hetman(row, col):
    global chessboard
    row = int(row) - 1
    col = ord(col) - ord('A')
    chessboard.remove_hetman(row, col)
