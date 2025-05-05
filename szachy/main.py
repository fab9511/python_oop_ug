from view_board import *
from logic import *


if __name__ == '__main__':
    print("Początek gry!!!!\n" + "="*30)
    while pion_danger():
        display_board()
        display_pion_danger()
        print("\n" + "="*30)
        if not pion_danger():
            print("Koniec gry")
            break

        opt = select_option()
        print("\n"+ "="*30)
        execute_option(opt)

