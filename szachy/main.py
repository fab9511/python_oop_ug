from view_board import *
from logic import *
import re


if __name__ == '__main__':
    global chessboard, IS_PION_SAFE
    print("Inicjalizacja szachownicy")
    while chessboard.pion_danger:
        display_board()
        display_pion_danger()

        if not chessboard.pion_danger:
            print("Koniec gry")
            break

        print("\nDostępne opcje: "
              "\n\t1.Ponowne losowanie pozycji pionka "
              "\n\t2.Usunięcie danego hetmana")

        opt = (input("Wybierz jedną opcję: ")).replace(".", "")
        while not re.match(r'[1-2]', opt):
            opt = (input("Podaj poprawną opcję: ")).replace(".","")

        if opt == "1":
            chessboard.new_position_pion()

        elif opt == "2":
            position =  input("Podaj koordynaty hetmana, którego chcesz usunąć: ")

            while not re.match(r'[A-Ha-h][1-8]', position):
                position = input("Podaj poprawny koordynat!!! \nNowy koordynat: ")

            col, row = position

            while not is_hetman(row, col.upper()):
                print("Brak hetmana na danej pozycji!!!")
                position = input("Podaj poprawny koordynat!!! \nNowy koordynat: ")
                while not re.match(r'[A-Ha-h][1-8]', position):
                    position = input("Podaj poprawny koordynat!!! \nNowy koordynat: ")
                col, row = position
            delete_hetman(row, col.upper())