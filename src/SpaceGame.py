import pygame, sys, os, random, time

GAMEW = 1664
GAMEH = 936
UIX =  1248
FPS = 60

STARCOUNT = 150

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode((GAMEW, GAMEH))
pygame.display.set_caption("Space Game v0.1 (Alpha)")
fpsClock = pygame.time.Clock()

class Cursor(object):

	def __init__(self):
		self.selected = None
		self.texture = pygame.image.load(os.path.join('img', 'misc_icons', 'cursor.png')).convert()

	def pos(self):
		return pygame.mouse.get_pos()

	def x(self):
		return self.pos()[0]

	def y(self):
		return self.pos()[1]

	def render(self):
		if self.selected != None:
			screen.blit(self.texture, (self.selected.x - 5, self.selected.y - 5))
			if self.selected.owner != None:
				pygame.draw.circle(screen, (133, 133, 133), (self.selected.x, self.selected.y), self.selected.owner.jumpRange, 2) #Draws the jump range of ships on planet

class Star(object):

	stars = []

	def __init__(self, name, x, y):
		self.name = name
		self.x = x + 5
		self.y = y + 5
		self.rect = pygame.Rect(self.x - 5, self.y - 5, 10, 10)
		self.owner = None

	def render(self):
		if self.owner != None:
			self.color = self.owner.color
		else:
			self.color = (255, 255, 255)
		pygame.draw.circle(screen, self.color, (self.x, self.y), 5)

	def render_stars():
		for star in Star.stars:
			star.render()

class Empire(object):

	empires = []

	def __init__(self, name, color):
		self.name = name
		self.color = color
		self.player = False
		self.capital = self.generate_capital()
		self.jumpRange = 100

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
		randx = random.randint(10, UIX - 10)
		randy = random.randint(10, GAMEH - 10)
		if (randx, randy) not in alreadyOccupied:
			for i in range(randx - 10, randx + 10):
				for j in range(randy - 10, randy + 10):
					alreadyOccupied.append((i, j)) #Adds every coordinate in a 10 radius around the star to already occupied, preventing stars from spawning too close to eachother
			Star.stars.append(Star("Star", randx, randy))
			count += 1

def handle_input():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				sys.exit()

			if event.key == pygame.K_BACKQUOTE:
				Cursor.selected = None

		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			for star in Star.stars:
				if star.rect.collidepoint(Cursor.pos()):
					Cursor.selected = star

#Initializiation
Cursor = Cursor()
build_universe()

#Define empires
Republic = Empire("Galactic Republic", (0, 0, 255))
Jedi = Empire("The Jedi Order", (0, 255, 0))
Sith = Empire("The Sith Lords", (255, 0, 0))

#Game loop
while True:

	handle_input()

	screen.fill((0,0,0))
	Star.render_stars()
	Cursor.render()

	pygame.draw.rect(screen, (0,0,0), (UIX, 0, 1000, GAMEH))

	pygame.display.update()
	fpsClock.tick(FPS)