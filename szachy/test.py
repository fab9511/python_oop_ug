import unittest
from unittest.mock import patch
from io import StringIO
from szachownica import Chessboard, HETMAN, PION
import view_board


class TestInitBoard(unittest.TestCase):
    def test_initial_figure_counts(self):
        board = Chessboard()
        hetman_count = sum(row.count(HETMAN) for row in board.board)
        pion_count = sum(row.count(PION) for row in board.board)
        self.assertEqual(hetman_count, 5)
        self.assertEqual(pion_count, 1)

    def test_board_size(self):
        board = Chessboard(size=8)
        self.assertEqual(len(board.board), 8)
        self.assertEqual(len(board.board[0]), 8)


class TestControlledPlacement(unittest.TestCase):
    @patch("random.randint")
    def test_fixed_placement(self, mock_randint):
        mock_randint.side_effect = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]

        board = Chessboard(num_hetman=5, num_pion=1)
        self.assertEqual(board.board[0][0], HETMAN)
        self.assertEqual(board.board[1][1], HETMAN)
        self.assertEqual(board.board[2][2], HETMAN)
        self.assertEqual(board.board[3][3], HETMAN)
        self.assertEqual(board.board[4][4], HETMAN)
        self.assertEqual(board.board[5][5], PION)

class TestPionLogic(unittest.TestCase):
    def setUp(self):
        self.board = Chessboard()

    def test_find_pion(self):
        pos = self.board._Chessboard__find_pion()
        self.assertIsNotNone(pos)
        row, col = pos
        self.assertEqual(self.board.board[row][col], PION)

    def test_move_pion(self):
        old_pos = self.board._Chessboard__find_pion()
        self.board.new_position_pion()
        new_pos = self.board._Chessboard__find_pion()
        self.assertNotEqual(old_pos, new_pos)

class TestHetmanLogic(unittest.TestCase):
    def setUp(self):
        self.board = Chessboard(num_hetman=0, num_pion=0)
        self.board.board[4][4] = PION
        self.board.board[4][0] = HETMAN
        self.board.board[0][4] = HETMAN
        self.board.board[0][0] = HETMAN

    def test_pion_in_danger(self):
        attackers = self.board.pion_in_danger()
        self.assertEqual(len(attackers), 3)

    def test_remove_hetman(self):
        pos = (0,0)
        self.board.remove_hetman(*pos)
        self.assertEqual(self.board.board[pos[0]][pos[1]], 0)




"============================================================"


class TestViewBoard(unittest.TestCase):
    @patch("sys.stdout", new_callable=StringIO)
    def test_display_column_headers(self, mock_stdout):
        view_board.display_column_headers(8)
        output = mock_stdout.getvalue().strip()
        expected_output = "A B C D E F G H"
        self.assertEqual(output, expected_output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_row(self, mock_stdout):
        row = [HETMAN, PION, 0, 0, 0, 0, 0, 0]
        view_board.display_row(row, 1)
        output = mock_stdout.getvalue().strip()
        expected_output = "1 H P █ ░ █ ░ █ ░"
        self.assertEqual(output, expected_output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_board(self, mock_stdout):
        chessboard = Chessboard(num_hetman=0, num_pion=0)
        chessboard.board[4][4] = PION
        chessboard.board[0][0] = HETMAN
        view_board.display_board(chessboard)
        output = mock_stdout.getvalue().strip().split("\n")

        self.assertIn("A B C D E F G H", output[0])
        self.assertIn(" 4 ░ █ ░ █ ░ █ ░ █ ", output[4])

    @patch("sys.stdout", new_callable=StringIO)
    @patch("szachownica.Chessboard.pion_in_danger")
    def test_display_pion_danger(self, mock_pion_in_danger, mock_stdout):
        # Testujemy funkcję display_pion_danger
        mock_pion_in_danger.return_value = [(1, 1), (1, 4)]  # Symulujemy, że pionek jest zagrożony przez dwa hetmany

        chessboard = Chessboard(num_hetman=3, num_pion=1)
        view_board.display_pion_danger(chessboard)

        output = mock_stdout.getvalue().strip()
        expected_output = "Pion zbity\nHetmany atakujące:  A1 D1"
        self.assertEqual(output, expected_output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("szachownica.Chessboard.pion_in_danger")
    def test_display_pion_safe(self, mock_pion_in_danger, mock_stdout):
        # Testujemy, czy pionek jest bezpieczny
        mock_pion_in_danger.return_value = []

        chessboard = Chessboard(num_hetman=3, num_pion=1)
        view_board.display_pion_danger(chessboard)

        output = mock_stdout.getvalue().strip()
        expected_output = "Pion bezpieczny"
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
