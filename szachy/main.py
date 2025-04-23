from view_board import *
from logic import *


if __name__ == '__main__':
    print("Początek gry!!!!\n============================")
    while pion_danger():
        display_board()
        display_pion_danger()
        print("\n============================")
        if not pion_danger():
            print("Koniec gry")
            break

        opt = select_option()
        print("\n============================")
        execute_option(opt)

