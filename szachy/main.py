from view_board import display_board as display
from szachownica import *

if __name__ == '__main__':
    global chessboard
    print("Inicjalizacja szachownicy")
    display()
    if positions:=chessboard.pion_in_danger():
        print("Pion zbity")
        print(f'Hetmany atakujące {positions}')
    else:
        print("Pion bezpieczny")
