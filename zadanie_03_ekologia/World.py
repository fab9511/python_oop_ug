from Position import Position
from Organisms.Plant import Plant
from Organisms.Lynx import Lynx
from Action import Action
from ActionEnum import ActionEnum


class World(object):

	def __init__(self, worldX, worldY):
		self.__worldX = worldX
		self.__worldY = worldY
		self.__turn = 0
		self.__organisms = []
		self.__newOrganisms = []
		self.__separator = '.'
		self.__plagueTurnsLeft = 0
		self.__plagueActive = False
		self.__plagueAlreadyApplied = False
		self.numberTurns = 1
		self.__logs = []

	@property
	def worldX(self):
		return self.__worldX

	@property
	def worldY(self):
		return self.__worldY

	@property
	def turn(self):
		return self.__turn

	@turn.setter
	def turn(self, value):
		self.__turn = value

	@property
	def organisms(self):
		return self.__organisms

	@organisms.setter
	def organisms(self, value):
		self.__organisms = value

	@property
	def newOrganisms(self):
		return self.__newOrganisms

	@newOrganisms.setter
	def newOrganisms(self, value):
		self.__newOrganisms = value

	@property
	def separator(self):
		return self.__separator

	@property
	def plagueTurnsLeft(self):
		return self.__plagueTurnsLeft

	@plagueTurnsLeft.setter
	def plagueTurnsLeft(self, value):
		self.__plagueTurnsLeft = value
		if self.__plagueTurnsLeft == 0:
			for organism in self.organisms:
				organism.skipLifeLossThisTurn = False


	@property
	def plagueActive(self):
		return self.__plagueActive

	@plagueActive.setter
	def plagueActive(self, value):
		self.__plagueActive = value
		if value and self.plagueTurnsLeft == 0:
			self.plagueTurnsLeft = 2

	@property
	def plagueAlreadyApplied(self):
		return self.__plagueAlreadyApplied

	@plagueAlreadyApplied.setter
	def plagueAlreadyApplied(self, value):
		self.__plagueAlreadyApplied = value

	@property
	def logs(self):
		return self.__logs

	def makeTurn(self):
		actions = []
		self.numberTurns += 1

		if self.plagueActive:
			if not self.plagueAlreadyApplied:
				self.enablePlague()
				self.plagueAlreadyApplied = True
			self.updatePlague()

		for org in self.organisms:
			if self.positionOnBoard(org.position):
				actions = org.move()
				for a in actions:
					self.makeMove(a)
				actions = []
				if self.positionOnBoard(org.position):
					actions = org.action()
					for a in actions:
						self.makeMove(a)
					actions = []

		self.organisms = [o for o in self.organisms if self.positionOnBoard(o.position)]

		for o in self.organisms:
			o.decreaseLife()
			o.power += 1
			if o.liveLength < 1:
				self.log(str(o.__class__.__name__) + ': died of old age at: ' + str(o.position))
		self.organisms = [o for o in self.organisms if o.liveLength > 0]

		self.newOrganisms = [o for o in self.newOrganisms if self.positionOnBoard(o.position)]
		self.organisms.extend(self.newOrganisms)
		self.organisms.sort(key=lambda o: o.initiative, reverse=True)
		self.newOrganisms = []

		self.turn += 1

	def makeMove(self, action):
		self.log(action)
		if action.action == ActionEnum.A_ADD:
			self.newOrganisms.append(action.organism)
		elif action.action == ActionEnum.A_INCREASEPOWER:
			action.organism.power += action.value
		elif action.action == ActionEnum.A_MOVE:
			action.organism.position = action.position
		elif action.action == ActionEnum.A_REMOVE:
			action.organism.position = Position(xPosition=-1, yPosition=-1)


	def addOrganism(self, newOrganism):
		newOrgPosition = Position(xPosition=newOrganism.position.x, yPosition=newOrganism.position.y)

		if self.positionOnBoard(newOrgPosition):
			self.organisms.append(newOrganism)
			self.organisms.sort(key=lambda org: org.initiative, reverse=True)
			return True
		return False

	def isPositionFree(self, pos):
		if self.getOrganismFromPosition(pos) is None:
			return True
		else:
			return False

	def positionOnBoard(self, position):
		return position.x >= 0 and position.y >= 0 and position.x < self.worldX and position.y < self.worldY

	def getOrganismFromPosition(self, position):
		pomOrganism = None

		for org in self.organisms:
			if org.position == position:
				pomOrganism = org
				break
		if pomOrganism is None:
			for org in self.newOrganisms:
				if org.position == position:
					pomOrganism = org
					break
		return pomOrganism

	def getNeighboringPositions(self, position):
		result = []
		pomPosition = None

		for y in range(-1, 2):
			for x in range(-1, 2):
				pomPosition = Position(xPosition=position.x + x, yPosition=position.y + y)
				if self.positionOnBoard(pomPosition) and not (y == 0 and x == 0):
					result.append(pomPosition)
		return result

	def filterFreePositions(self, fields):
		result = []

		for field in fields:
			if self.getOrganismFromPosition(field) is None:
				result.append(field)
		return result

	def filterPositionsWithoutAnimals(self, fields):
		result = []
		pomOrg = None

		for filed in fields:
			pomOrg = self.getOrganismFromPosition(filed)
			if pomOrg is None or isinstance(pomOrg, Plant):
				result.append(filed)
		return result

	def filterPositionsWithLynx(self, fields):
		result = []
		for pos in fields:
			org = self.getOrganismFromPosition(pos)
			if isinstance(org, Lynx):
				result.append(pos)
		return result

	def enablePlague(self):
		for organism in self.organisms:
			organism.liveLength = max(1, organism.liveLength // 2)
			organism.skipLifeLossThisTurn = True

	def updatePlague(self):
		if self.plagueTurnsLeft > 0:
			self.plagueTurnsLeft -= 1
		if self.plagueTurnsLeft == 0:
			self.plagueActive = False
			self.plagueAlreadyApplied = False

	def activatePlague(self, turns=2):
		if not self.plagueActive:
			self.plagueActive = True
			self.plagueTurnsLeft = turns

	def log(self, message):
		self.__logs.append(message)

	def clearLogs(self):
		self.__logs = []

	def __str__(self):
		result = '\nturn: ' + str(self.__turn) + '\n'
		for wY in range(0, self.worldY):
			for wX in range(0, self.worldX):
				org = self.getOrganismFromPosition(Position(xPosition=wX, yPosition=wY))
				if org:
					result += str(org.sign)
				else:
					result += self.separator
			result += '\n'
		return result
