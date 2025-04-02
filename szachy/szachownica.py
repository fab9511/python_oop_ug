import random

HETMAN = 4
PION = 1

class Chessboard:
    def __init__(self, size = 8, num_hetman = 5, num_pion = 1):
        if not isinstance(size, int) or not isinstance(num_hetman, int):
            raise TypeError('size and number of hetman must be an integer')

        self.size = size
        # self.max_figures = size**2  ## dodać max, aby nie tworzyć nieskończonej petli w __generate_figure()
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.__generate_figure(HETMAN, num_hetman)
        self.__generate_figure(PION, num_pion)

    def __generate_figure(self, figures, num_figure):
        while num_figure > 0:
            set_x = random.randint(0, self.size-1)
            set_y = random.randint(0, self.size-1)
            if self.__set_figure(figures, set_x, set_y):
                num_figure -= 1


    def __set_figure(self, figures, set_x, set_y):
        if self.board[set_y][set_x] == 0:
            self.board[set_y][set_x] = figures
            return True
        else:
            return False
#

    def pion_in_danger(self):
        res = []
        for num_row, row  in enumerate(self.board):
            for num_col, value in enumerate(row):
                if value == PION:
                    continue
                elif value == HETMAN:
                    if self.__moves_hetman(num_row, num_col):
                        res.append((num_row+1, num_col+1))
                else:
                    continue
        return res


    def __moves_hetman(self, row, col):
        moves = [True] * 6
        for z in range(self.size):  ## dodać warunek żeby nie isć tą scieżką jeśli była jakaś figura inna niż pion
            if self.board[row][z] in [PION, HETMAN] and moves[0]:
                return True  # Kolumna
            if self.board[z][col] == PION and moves[1]:
                return True  # Wiersz
            if row + z < self.size and col + z < self.size and self.board[row + z][col + z] == PION:
                return True  # Skośna na prawo w dół
            if row - z >= 0 and col - z >= 0 and self.board[row - z][col - z] == PION:
                return True  # Skośna na lewo w górę
            if row + z < self.size and col - z >= 0 and self.board[row + z][col - z] == PION:
                return True  # Skośna na lewo w dół
            if row - z >= 0 and col + z < self.size and self.board[row - z][col + z] == PION:
                return True  # Skośna na prawo w górę
        return False


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

