import unittest
from Organisms.Lynx import Lynx
from Position import Position
from World import World

class TestLynx(unittest.TestCase):

    def setUp(self):
        self.world = World(10, 10)
        self.position = Position(xPosition=5, yPosition=5)
        self.lynx = Lynx(position=self.position, world=self.world)

    def test_initial_parameters(self):
        self.assertEqual(self.lynx.power, 6)
        self.assertEqual(self.lynx.initiative, 5)
        self.assertEqual(self.lynx.liveLength, 18)
        self.assertEqual(self.lynx.powerToReproduce, 14)
        self.assertEqual(self.lynx.sign, 'R')

    def test_clone(self):
        clone = self.lynx.clone()
        self.assertIsInstance(clone, Lynx)
        self.assertEqual(clone.power, 6)
        self.assertEqual(clone.sign, 'R')
        self.assertEqual(clone.initiative, 5)
        self.assertEqual(clone.liveLength, 18)
        self.assertEqual(clone.powerToReproduce, 14)
        self.assertIsNotNone(clone.position)
        self.assertIsNotNone(clone.world)

    def test_get_neighboring_positions(self):
        neighbors = self.lynx.getNeighboringPosition()
        for pos in neighbors:
            self.assertTrue(abs(pos.x - self.position.x) <= 1)
            self.assertTrue(abs(pos.y - self.position.y) <= 1)
            self.assertFalse(pos == self.position)


if __name__ == '__main__':
    unittest.main()
