from szachownica import *

def display_board():
    global chessboard
    for num in chessboard.board:
        for figure in num:
            if HETMAN == figure:
                print("H", end=" ")
            elif PION == figure:
                print("P", end=" ")
            else:
                print(".", end=" ")
        print()

if __name__ == "__main__":
    display_board() ##testing


