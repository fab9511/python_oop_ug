from szachownica import *
global chessboard


def display_board():
    size = chessboard.size

    print("   " + " ".join(chr(ord('A') + i) for i in range(size)))  # Naglowek kolumn
    for i, row in enumerate(chessboard.board):
        print(f"{i + 1:2} ", end="")  # Numer wiersza
        for j, figure in enumerate(row):
            if (i + j) % 2 == 0:
                background = "░"
            else:
                background = "█"

            if figure == HETMAN:
                print("H", end=" ")
            elif figure == PION:
                print("P", end=" ")
            else:
                print(background, end=" ")
        print()

def display_pion_danger():
    if positions:=chessboard.pion_in_danger():
        print("Pion zbity")
        print("Hetmany atakujące: ", end=" ")
        for coordinates in positions:
            print(chr(coordinates[1]+ord("A")-1) + str(coordinates[0]), end=" ")
        print("")
    else:
        print("Pion bezpieczny")
        chessboard.pion_danger = False

if __name__ == "__main__":
    display_board() ##testing
    display_pion_danger()

