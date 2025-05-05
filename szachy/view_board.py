"""
view_board.py

Moduł odpowiedzialny za prezentację szachownicy oraz wizualne informowanie o stanie pionka.
Zawiera funkcje do wyświetlania planszy z figurami oraz komunikatów o zagrożeniu pionka.

Używa globalnej instancji `chessboard` z modułu `szachownica`.
"""


from szachownica import *


def display_column_headers(size):
    """
    Wyświetla nagłówki kolumn (A-H) nad planszą.

    :param size: int - rozmiar planszy (np. 8 dla planszy 8x8).
    :return: None
    """
    print("   " + " ".join(chr(ord('A') + i) for i in range(size)))


def display_row(row, row_num):
    """
    Wyświetla jeden wiersz planszy z figurami i odpowiednim tłem.

    :param row: list - lista zawierająca figury w danym wierszu.
    :param row_num: int - numer wiersza (1-8).
    :return: None
    """
    print(f"{row_num:2} ", end="")  # Num row
    for j, figure in enumerate(row):
        if figure == HETMAN:
            print("H", end=" ")
        elif figure == PION:
            print("P", end=" ")
        else:
            background = "░" if (row_num + j) % 2 == 0 else "█"
            print(background, end=" ")
    print()


def display_board(plansza = chessboard):
    """
    Wyświetla całą szachownicę z oznaczeniami wierszy i kolumn oraz figurami.

    :return: None
    """
    size = plansza.size 
    display_column_headers(size)
    for i, row in enumerate(plansza.board):
        display_row(row, i+1)


def display_pion_danger(plansza = chessboard):
    """
    Sprawdza, czy pionek jest atakowany i wypisuje odpowiednią informację.
    Jeśli tak, wyświetla również pozycje wszystkich hetmanów zagrażających pionkowi.

    :return: None
    """
    if positions:=plansza.pion_in_danger():
        print("Pion zbity")
        print("Hetmany atakujące: ", end=" ")
        for coordinates in positions:
            print(chr(coordinates[1]+ord("A")-1) + str(coordinates[0]), end=" ")
        print("")
    else:
        print("Pion bezpieczny")
        plansza.pion_danger = False
