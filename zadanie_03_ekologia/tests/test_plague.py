import unittest
from io import StringIO
import sys
from Position import Position
from World import World
from Organisms.Animal import Animal


class TestOrganism(Animal):
    def __init__(self, position, world, life):
        super().__init__(None, position, world)
        self.liveLength = life
        self.initParams()

    def clone(self):
        return TestOrganism(self.position, self.world, self.liveLength)

    def initParams(self):
        self.power = 1
        self.initiative = 1
        self.powerToReproduce = 1
        self.sign = 'T'

    def move(self):
        return []

    def action(self):
        return []


class TestPlagueMode(unittest.TestCase):

    def setUp(self):
        self._original_stdout = sys.stdout
        sys.stdout = StringIO()

        self.world = World(5, 5)

        self.org1 = TestOrganism(Position(xPosition=1, yPosition=1), self.world, 10)
        self.org2 = TestOrganism(Position(xPosition=2, yPosition=2), self.world, 6)
        self.org3 = TestOrganism(Position(xPosition=3, yPosition=3), self.world, 3)

        self.world._World__organisms = [self.org1, self.org2, self.org3]

    def tearDown(self):
        sys.stdout = self._original_stdout

    def test_plague_halves_lives(self):
        self.world.plagueActive = True
        self.world.makeTurn()

        self.assertEqual(self.org1.liveLength, 5)
        self.assertEqual(self.org2.liveLength, 3)
        self.assertEqual(self.org3.liveLength, 1)

    def test_plague_last_only_two_turns(self):
        self.world.plagueActive = True
        self.world.makeTurn()
        self.assertEqual(self.world.plagueTurnsLeft, 1)

        self.world.makeTurn()
        self.assertEqual(self.world.plagueTurnsLeft, 0)
        self.assertFalse(self.world.plagueActive)

    def test_newborns_not_affected(self):
        self.world.plagueActive = True
        self.world.makeTurn()

        new_org = TestOrganism(Position(xPosition=3, yPosition=3), self.world, 8)
        self.world.addOrganism(new_org)

        self.world.makeTurn()  # plaga 2 tura
        self.assertEqual(new_org.liveLength, 7)


if __name__ == "__main__":
    unittest.main()
