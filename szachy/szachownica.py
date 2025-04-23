"""
szachownica.py

Moduł odpowiedzialny za logikę szachownicy i operacje na figurach.
Zawiera klasę Chessboard, która umożliwia losowe rozmieszczenie hetmanów i pionka,
sprawdzenie zagrożenia dla pionka oraz manipulację figurami (np. usuwanie, zmiana pozycji).

Stałe:
    HETMAN = 4
    PION = 1
"""

import random

HETMAN = 4
PION = 1


class Chessboard:
    """
    Reprezentuje planszę szachową i logikę operacji na figurach.

    :param size: int - rozmiar planszy (domyślnie 8x8).
    :param num_hetman: int - liczba hetmanów (maksymalnie 5).
    :param num_pion: int - liczba pionków (zawsze 1).
    """
    def __init__(self, size = 8, num_hetman = 5, num_pion = 1):
        if not isinstance(size, int) or not isinstance(num_hetman, int):
            raise TypeError('size and number of hetman must be an integer')

        self.size = size
        if num_hetman > 5:
            raise ValueError('num_hetman must be less than 6')
        self.num_hetman = num_hetman
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.__place_random_figures(HETMAN, num_hetman)
        self.__place_random_figures(PION, num_pion)
        self.pion_danger = True


    def __place_random_figures(self, figures, num_figure):
        """
        Umieszcza losowo określoną liczbę figur na planszy.

        :param figures: int - typ figury (HETMAN lub PION).
        :param num_figure: int - liczba figur do umieszczenia.
        :return: None
        """
        while num_figure > 0:
            set_x = random.randint(0, self.size-1)
            set_y = random.randint(0, self.size-1)
            if self.__set_figure(figures, set_x, set_y):
                num_figure -= 1


    def __set_figure(self, figures, set_x, set_y):
        """
        Ustawia figurę na wskazanej pozycji, jeśli jest pusta.

        :param figures: int - typ figury.
        :param set_x: int - kolumna.
        :param set_y: int - wiersz.
        :return: bool - True jeśli udało się ustawić figurę.
        """
        if self.board[set_y][set_x] == 0:
            self.board[set_y][set_x] = figures
            return True
        else:
            return False


    def pion_in_danger(self):
        """
        Sprawdza, czy pionek jest zagrożony przez któregoś z hetmanów.

        :return: list - lista współrzędnych hetmanów, którzy atakują pionka.
        """
        res = []
        for num_row, row  in enumerate(self.board):
            for num_col, value in enumerate(row):
                if value == PION:
                    continue
                elif value == HETMAN:
                    if self.__can_attack_pion(num_row, num_col):
                        res.append((num_row+1, num_col+1))
                else:
                    continue
        return res


    def __can_attack_pion(self, row, col):
        """
        Sprawdza, czy hetman na danej pozycji może zaatakować pionka.

        :param row: int - wiersz hetmana.
        :param col: int - kolumna hetmana.
        :return: bool - True jeśli może zaatakować pionka.
        """
        moves = [True] * 8

        for z in range(1, self.size):  #bo z = 0 => pozycja hetmana

            # Ruch poziomy (w prawo)
            if moves[0] and col + z < self.size:
                piece = self.board[row][col + z]
                if piece == PION:
                    return True
                elif piece == HETMAN or piece != 0:
                    moves[0] = False

            # Ruch poziomy (w lewo)
            if moves[1] and col - z >= 0:
                piece = self.board[row][col - z]
                if piece == PION:
                    return True
                elif piece == HETMAN or piece != 0:
                    moves[1] = False

            # Ruch pionowy (w góre)
            if moves[2] and row - z >= 0:
                piece = self.board[row - z][col]
                if piece == PION:
                    return True
                elif piece == HETMAN or piece != 0:
                    moves[2] = False


            # Ruch pionowy (w dół)
            if moves[3] and row + z < self.size:
                piece = self.board[row + z][col]
                if piece == PION:
                    return True
                elif piece == HETMAN or piece != 0:
                    moves[3] = False

            # Skośna na prawo w dół
            if moves[4] and row + z < self.size and col + z < self.size:
                piece = self.board[row + z][col + z]
                if piece == PION:
                    return True
                elif piece == HETMAN or piece != 0:
                    moves[4] = False

            # Skośna na lewo w górę
            if moves[5] and row - z >= 0 and col - z >= 0:
                piece = self.board[row - z][col - z]
                if piece == PION:
                    return True
                elif piece == HETMAN or piece != 0:
                    moves[5] = False

            # Skośna na lewo w dół
            if moves[6] and row + z < self.size and col - z >= 0:
                piece = self.board[row + z][col - z]
                if piece == PION:
                    return True
                elif piece == HETMAN or piece != 0:
                    moves[6] = False

            # Skośna na prawo w górę
            if moves[7] and row - z >= 0 and col + z < self.size:
                piece = self.board[row - z][col + z]
                if piece == PION:
                    return True
                elif piece == HETMAN or piece != 0:
                    moves[7] = False

        return False  # Jeśli nie znaleziono możliwego bicia piona


    def new_position_pion(self):
        """
        Przypisuje pionkowi nową losową pozycję na planszy.

        :return: None
        """
        row, col = self.__find_pion()
        self.board[row][col] = 0
        self.__place_random_figures(PION, 1)


    def __find_pion(self):
        """
        Znajduje aktualną pozycję pionka.

        :return: tuple - współrzędne (row, col) pionka.
        """
        for row_index, row in enumerate(self.board):
            for col_index, value in enumerate(row):
                if value == PION:
                    return row_index, col_index
        return None


    def remove_hetman(self, row, col):
        """
        Usuwa hetmana z danej pozycji.

        :param row: int - numer wiersza (0-indexed).
        :param col: int - numer kolumny (0-indexed).
        :return: None
        """
        self.board[row][col] = 0

chessboard = Chessboard()

if __name__ == '__main__':
    board = Chessboard()
    for num in board.board:
        for figure in num:
            if HETMAN == figure:
                print("H", end=" ")
            elif PION == figure:
                print("P", end=" ")
            else:
                print(".", end=" ")
        print()

