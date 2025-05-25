from .Animal import Animal
from Position import Position
from Action import Action
from ActionEnum import ActionEnum

class Antelope(Animal):

	def __init__(self, antelope=None, position=None, world=None):
		super(Antelope, self).__init__(antelope, position, world)

	def clone(self):
		return Antelope(self, None, None)

	def initParams(self):
		self.power = 4
		self.initiative = 3
		self.liveLength = 11
		self.powerToReproduce = 5
		self.sign = 'A'

	def move(self):
		result = []
		lynxPositions = self.getLynxPosition()

		if lynxPositions:
			result.extend(self.tryEscape(lynxPositions))
		else:
			result = super().move()

		return result

	def tryEscape(self, lynxPositions):
		result = []
		lynxPos = lynxPositions[0]
		dx = self.position.x - lynxPos.x
		dy = self.position.y - lynxPos.y

		escapePos = Position(xPosition=self.position.x + 2 * dx, yPosition=self.position.y + 2 * dy)

		if self.world.positionOnBoard(escapePos) and self.world.getOrganismFromPosition(escapePos) is None:
			result.append(Action(ActionEnum.A_MOVE, escapePos, 0, self))
			self.lastPosition = self.position
		else:
			lynx = self.world.getOrganismFromPosition(lynxPos)
			if lynx:
				result.extend(lynx.consequences(self))

		return result

	def getNeighboringPosition(self):
		return self.world.filterPositionsWithoutAnimals(self.world.getNeighboringPositions(self.position))

	def getLynxPosition(self):
		return self.world.filterPositionsWithLynx(self.world.getNeighboringPositions(self.position))