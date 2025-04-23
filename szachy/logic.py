"""
logic.py

Moduł zawiera logikę gry w szachy z pionkiem i hetmanami.
Implementuje funkcje do generowania szachownicy, sprawdzania, czy pionek
jest w niebezpieczeństwie oraz manipulacji figurami (losowanie pozycji, usuwanie hetmana).
"""
from szachownica import *
import re


def is_hetman(row, col):
    """
    Sprawdza, czy na danej pozycji znajduje się hetman.

    :param row: int - numer wiersza (od 1 do 8).
    :param col: str litera kolumny (od A do H).
    :return: bool - True jeśli figura stojąca na pozycji col,row to chetman
    """
    row = int(row) - 1
    col = ord(col) - ord('A')
    if chessboard.board[row][col] == HETMAN:
        return True
    else:
        return False

def delete_hetman(row, col):
    """
    Usuwa hetmana z danej pozycji na szachownicy.

    :param row: int - numer wiersza (od 1 do 8).
    :param col: str - litera kolumny (od A do H).
    :return: None
    """
    global chessboard
    row = int(row) - 1
    col = ord(col) - ord('A')
    chessboard.remove_hetman(row, col)


def select_option():
    """
    Wyświetla dostępne opcje użytkownikowi i pobiera poprawny wybór.

    :return: str - numer opcji wybranej przez użytkownika ("1" lub "2").
    """
    print("\nDostępne opcje: "
          "\n\t1.Ponowne losowanie pozycji pionka "
          "\n\t2.Usunięcie danego hetmana")

    opt = (input("Wybierz jedną opcję: ")).replace(".", "")
    while not re.match(r'[1-2]', opt):
        opt = (input("Podaj poprawną opcję: ")).replace(".", "")

    return opt


def execute_option(opt):
    """
    Wykonuje akcję w zależności od wybranej opcji:
    - 1: losuje nową pozycję pionka.
    - 2: usuwa hetmana z podanej pozycji.

    :param opt: str - numer opcji ("1" lub "2").
    :return: None
    """
    if opt == "1":
        execute_random_pion_move()
    elif opt == "2":
        execute_delete_hetman()


def execute_random_pion_move():
    """
    Wykonuje losowy ruch pionka, zmieniając jego pozycję na nową,
    niekolidującą z istniejącymi figurami.

    :return: None
    """
    chessboard.new_position_pion()


def execute_delete_hetman():
    """
    Usuwa hetmana z planszy na podstawie pozycji podanej przez użytkownika.
    Sprawdza poprawność pozycji oraz obecność hetmana przed usunięciem.

    :return: None
    """
    row, col = get_position()

    while not is_hetman(row, col.upper()):
        print("Brak hetmana na danej pozycji!!!")
        row, col = get_position()

    delete_hetman(row, col.upper())


def get_position():
    """
    Pobiera od użytkownika współrzędne hetmana do usunięcia.

    :return: tuple - (row, col), gdzie row to numer wiersza (str), a col to litera kolumny (str).
    """

    position = input("Podaj koordynaty hetmana, którego chcesz usunąć: ")

    while not re.match(r'[A-Ha-h][1-8]', position):
        position = input("Podaj poprawny koordynat!!! \nNowy koordynat: ")

    col, row = position
    return row, col

def pion_danger():
    """
    Sprawdza, czy pionek znajduje się w niebezpieczeństwie (jest atakowany przez hetmana).

    :return: bool - True jeśli pionek jest zagrożony, False w przeciwnym przypadku.
    """
    return chessboard.pion_danger