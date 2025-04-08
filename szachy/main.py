from view_board import display_board as display
from szachownica import *

if __name__ == '__main__':
    global chessboard
    print("Inicjalizacja szachownicy")
    display()

    if positions:=chessboard.pion_in_danger():
        print("Pion zbity")
        print("Hetmany atakujące: ", end=" ")
        for coordinates in positions:
            print(chr(coordinates[1]+ord("A")-1) + str(coordinates[0]), end=", ")
    else:
        print("Pion bezpieczny")
