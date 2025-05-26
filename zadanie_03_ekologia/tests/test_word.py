import unittest
from unittest.mock import MagicMock
from World import World


class TestWorldPlagueAndLogs(unittest.TestCase):
    def setUp(self):
        self.world = World(10, 10)

        self.org1 = MagicMock()
        self.org1.liveLength = 10
        self.org1.skipLifeLossThisTurn = False

        self.org2 = MagicMock()
        self.org2.liveLength = 3
        self.org2.skipLifeLossThisTurn = False

        self.world.organisms = [self.org1, self.org2]

        self.world._World__plagueTurnsLeft = 0
        self.world._World__plagueActive = False
        self.world._World__plagueAlreadyApplied = False
        self.world._World__logs = []


    def test_log_and_clearLogs(self):
        self.world.log("Test log")
        self.assertIn("Test log", self.world.logs)

        self.world.clearLogs()
        self.assertEqual(len(self.world.logs), 0)

    def test_isPositionFree_returns_true_when_none(self):
        self.world.getOrganismFromPosition = MagicMock(return_value=None)
        pos = MagicMock()
        self.assertTrue(self.world.isPositionFree(pos))

    def test_isPositionFree_returns_false_when_occupied(self):
        self.world.getOrganismFromPosition = MagicMock(return_value=MagicMock())
        pos = MagicMock()
        self.assertFalse(self.world.isPositionFree(pos))

    def test_plagueTurnsLeft_property(self):
        self.world.plagueTurnsLeft = 5
        self.assertEqual(self.world.plagueTurnsLeft, 5)

    def test_plagueActive_property_sets_turns_if_activated_with_zero_turns(self):
        self.world._World__plagueTurnsLeft = 0
        self.world.plagueActive = True
        self.assertTrue(self.world.plagueActive)
        self.assertEqual(self.world.plagueTurnsLeft, 2)

    def test_plagueAlreadyApplied_property(self):
        self.world.plagueAlreadyApplied = True
        self.assertTrue(self.world.plagueAlreadyApplied)
        self.world.plagueAlreadyApplied = False
        self.assertFalse(self.world.plagueAlreadyApplied)


if __name__ == "__main__":
    unittest.main()
