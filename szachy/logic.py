from szachownica import *
import re


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


def select_option():
    print("\nDostępne opcje: "
          "\n\t1.Ponowne losowanie pozycji pionka "
          "\n\t2.Usunięcie danego hetmana")

    opt = (input("Wybierz jedną opcję: ")).replace(".", "")
    while not re.match(r'[1-2]', opt):
        opt = (input("Podaj poprawną opcję: ")).replace(".", "")

    return opt


def execute_option(opt):
    if opt == "1":
        execute_random_pion_move()
    elif opt == "2":
        execute_delete_hetman()


def execute_random_pion_move():
    chessboard.new_position_pion()


def execute_delete_hetman():
    row, col = get_position()

    while not is_hetman(row, col.upper()):
        print("Brak hetmana na danej pozycji!!!")
        row, col = get_position()

    delete_hetman(row, col.upper())


def get_position():
    position = input("Podaj koordynaty hetmana, którego chcesz usunąć: ")

    while not re.match(r'[A-Ha-h][1-8]', position):
        position = input("Podaj poprawny koordynat!!! \nNowy koordynat: ")

    col, row = position
    return row, col

def pion_danger():
    return chessboard.pion_danger