from szachownica import *

# def display_board():
#     global chessboard
#     for num in chessboard.board:
#         for figure in num:
#             if HETMAN == figure:
#                 print("H", end=" ")
#             elif PION == figure:
#                 print("P", end=" ")
#             else:
#                 print(".", end=" ")
#         print()

def display_board():
    global chessboard
    SIZE = len(chessboard.board)

    print("   " + " ".join(chr(ord('A') + i) for i in range(SIZE)))  # Nagłówek kolumn
    for i, row in enumerate(chessboard.board):
        print(f"{i + 1:2} ", end="")  # Numer wiersza
        for j, figure in enumerate(row):
            # Naprzemienne kolory pola
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

if __name__ == "__main__":
    display_board() ##testing


