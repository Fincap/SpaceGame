import pygame, sys, os, random, time

GAMEW = 1664
GAMEH = 936
UIX =  1248
FPS = 60

STARCOUNT = 300

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode((GAMEW, GAMEH))
pygame.display.set_caption("Space Game v0.1")
fpsClock = pygame.time.Clock()

class Cursor(object):

	def pos(self):
		return pygame.mouse.get_pos()

	def x(self):
		return self.pos()[0]

	def y(self):
		return self.pos()[1]

class Star(object):

	stars = []

	def __init__(self, name, x, y):
		self.name = name
		self.x = x
		self.y = y
		self.rect = pygame.Rect(self.x, self.y, 2, 2)
		self.owner = None

	def render(self):
		if self.owner != None:
			self.color = self.owner.color
		else:
			self.color = (255, 255, 255)
		pygame.draw.rect(screen, self.color, self.rect)

	def render_stars():
		for star in Star.stars:
			star.render()

class Empire(object):

	empires = []

	def __init__(self, name, color):
		self.name = name
		self.color = color
		self.capital = self.generate_capital()

	def generate_capital(self):
		isUnique = False
		while not isUnique:
			randstar = random.choice(Star.stars)
			if randstar.owner == None:
				randstar.owner = self
				isUnique = True

		return randstar

def build_universe():
	alreadyOccupied = []
	count = 0
	while count < STARCOUNT:
		randx = random.randint(5, UIX)
		randy = random.randint(5, GAMEH)
		if (randx, randy) not in alreadyOccupied:
			Star.stars.append(Star("Star", randx, randy))
			alreadyOccupied.append((randx, randy))
			count += 1

def handle_input():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				sys.exit()

#Initializiation
Cursor = Cursor()
build_universe()

#Define empires
Man = Empire("Empire of Man", (0, 0, 255))

#Game loop
while True:

	handle_input()

	screen.fill((0,0,0))
	Star.render_stars()

	pygame.display.update()
	fpsClock.tick(FPS)