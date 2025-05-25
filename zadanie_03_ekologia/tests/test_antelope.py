import unittest
from unittest.mock import MagicMock
from Organisms.Antelope import Antelope
from Organisms.Lynx import Lynx
from Position import Position
from ActionEnum import ActionEnum
from World import World

class TestAntelope(unittest.TestCase):

    def setUp(self):
        self.world = MagicMock(spec=World)
        self.position = Position(xPosition=2, yPosition=2)
        self.antelope = Antelope(position=self.position, world=self.world)

    def test_move_without_lynx(self):
        self.antelope.getLynxPosition = MagicMock(return_value=[])
        self.antelope.getNeighboringPosition = MagicMock(return_value=[
            Position(xPosition=2, yPosition=3)
        ])
        self.world.getOrganismFromPosition.return_value = None

        result = self.antelope.move()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].action, ActionEnum.A_MOVE)

    def test_escape_successful(self):
        lynx_pos = Position(xPosition=1, yPosition=2)
        self.antelope.getLynxPosition = MagicMock(return_value=[lynx_pos])
        self.world.positionOnBoard.return_value = True
        self.world.getOrganismFromPosition.return_value = None

        result = self.antelope.move()

        expected_escape_pos = Position(xPosition=4, yPosition=2)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].action, ActionEnum.A_MOVE)
        self.assertEqual(result[0].position.x, expected_escape_pos.x)
        self.assertEqual(result[0].position.y, expected_escape_pos.y)

    def test_escape_impossible_attacks(self):
        lynx_pos = Position(xPosition=1, yPosition=2)
        lynx = MagicMock(spec=Lynx)
        lynx.consequences.return_value = ['fight_result']

        self.antelope.getLynxPosition = MagicMock(return_value=[lynx_pos])
        self.world.positionOnBoard.return_value = True
        self.world.getOrganismFromPosition.side_effect = lambda pos: lynx if pos == lynx_pos else 'BLOCKED'

        result = self.antelope.move()

        self.assertIn('fight_result', result)
        lynx.consequences.assert_called_once_with(self.antelope)

if __name__ == '__main__':
    unittest.main()
