import pygame
import time
import random
import threading



#---------- CHOOSE SOME COLORS ----------
white = (255,255,255)
green = (0,155,0)
black = (0,0,0)
red = (255,0,0)


#----------SET BACKGROUND OF THE GAME----------
introimg = pygame.image.load("C:\\Users\\lengu\\Desktop\\Pygame\\space2.jpg")
introimg2 = pygame.transform.scale(introimg, (1100,600))

#----------SET STRENGTH AS A GLOBAL VARIABLE----------
strength = 100

#----------DRAW THE ROCKET TO THE SCREEN ----------
class Rocket(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		imgload = pygame.image.load("C:\\Users\\lengu\\Desktop\\Pygame\\rocket.png")
		self.image = pygame.transform.scale(imgload, (100,100))
		self.rect = self.image.get_rect()

	#---------- COLLISION DETECTION SET TO FALSE SO ROCKET DON'T DISAPPEAR------------
	def collide(self, spriteGroup):
		global strength
		if pygame.sprite.spritecollide(self, spriteGroup, False):
			self.rect.x += 20
			strength -= 1
			message_to_screen("DAMAGE", red, 150, 300, 50)
			pygame.display.update()



#----------DRAW BULLETS TO THE SCREEN ----------
class Bullet(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		imgload = pygame.image.load("C:\\Users\\lengu\\Desktop\\Pygame\\download.png")
		self.image = pygame.transform.scale(imgload, (12,12))
		self.rect = self.image.get_rect()

	#---------- BULLET MOVES UPWARD ----------
	def update(self):
		self.rect.y -= 10

	#---------- COLLISION DETECTION SET TO TRUE SO OBJECTS DISAPPEAR WHEN HIT------------
	def collide(self, spriteGroup):
		pygame.sprite.spritecollide(self, spriteGroup, True)


#----------DRAW ASTEROIDS TO THE SCREEN ----------
class Asteroid(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		imgload = pygame.image.load("C:\\Users\\lengu\\Desktop\\Pygame\\asteroid.png")
		imgtran = pygame.transform.scale(imgload, (30,30))
		self.image =  pygame.transform.rotate(imgtran, 40)
		self.rect = self.image.get_rect()

	#------- ASTEROID MOVES DOWNWARD TO HIT THE ROCKET -------------
	def update(self):
		self.rect.y += 20


#----------INITIALIZE THE GAME----------
pygame.init()

#----------SET WIDTH AND HEIGHT OF GAME SCREEN ----------
display_width = 400
display_height = 600

#---------- CREATE THE SCREEN AND GIVE GAME A NAME----------
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Lunar')

#----------SET TIMER (HOW FAST GAME WILL RUN)----------
clock = pygame.time.Clock()


#---------- SET LIST THAT WILL CONTAIN IMAGE OF PLAYER AND BULLET ----------
all_sprites_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
asteroid_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()

#----------FUNCTION 1: CUSTOMIZE MESSAGE TO BE DISPLAYED----------
def message_to_screen(message, color, widthdis, heightdis, fontsize):
	myfont = pygame.font.SysFont(None, fontsize)
	screen_text = myfont.render(message, True, color)
	gameDisplay.blit(screen_text, [widthdis, heightdis])

#----------FUNCTION 2: KEEPING COUNT OF SCORE----------
def score(num, text, yaxis):
	myfont = pygame.font.SysFont(None, 20)
	screen_text = myfont.render(text + str(num), True, white)
	gameDisplay.blit(screen_text, [300, yaxis])


#----------FUNCTION 3: INTRO SCREEN --------------------
def gameIntro():
	rocket = pygame.image.load("C:\\Users\\lengu\\Desktop\\Pygame\\rocket.png")
	rocket2 = pygame.transform.scale(rocket, (100, 100))
	intro = True;

	#---------- WHILE IN INTRO, PRESS "Q" TO QUIT OR "P" TO PLAY
	while (intro):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					pygame.quit()
					quit()
				if event.key == pygame.K_p:
					intro = False

		#---------- DISPLAY MESSAGE TO THE SCREEN ----------
		gameDisplay.blit(introimg2, (-50,0))
		gameDisplay.blit(rocket2, (150, 500))
		message_to_screen("LUNAR LANDER", white, 90, 20, 40)
		message_to_screen("Developed by M. Le", white, 120, 60, 20)
		message_to_screen("Instructions:", white, 20, 240, 20)
		message_to_screen("1. You have 100 strength", white, 30, 260, 20)
		message_to_screen("2. Rock hit means damage", white, 30, 275, 20)
		message_to_screen("3. Press <- to move left, -> to move right", white, 30, 290, 20)
		message_to_screen("4. If you run out of damage protection, you die", white, 30, 305, 20)
		message_to_screen("5. Press P to play, Q to quit", white, 30, 320, 20)
		pygame.display.update()
		clock.tick(15)


#---------- FUNCTION 4: CREATE A TIMER FOR ASTEROIDS ----------
def asteroidTimer():
	asteroid = Asteroid()
	asteroid.rect.x = random.randrange(0,400)
	asteroid.rect.y = random.randrange(0,100)
	asteroid_list.add(asteroid)
	all_sprites_list.add(asteroid)
	threading.Timer(0.2, asteroidTimer).start()

asteroidTimer()


#---------- FUNCTION 5: CREATE THE GAME LOOP ----------
def gameLoop():
	gameExit = False
	gameOver = False
	rocket_change = 5

	#----------- KEEPING COUNT OF BULLET -------
	ammunition = 50
	distance = 0

	#---------- GENERATE A ROCKET ----------
	rocket = Rocket()
	all_sprites_list.add(rocket)
	player_list.add(rocket)
	rocket.rect.y = 500



#---------- WHILE USER PLAYS THE GAME ----------
	while not gameExit:


		#---------- GAME OVER SCREEN  ----------
		while gameOver == True:
			gameDisplay.blit(introimg2, (-70,0))
			message_to_screen("You die", white, 150, 260, 50)
			message_to_screen("Press P to Play Again or Q to Quit", white, 120, 300, 20)
			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameOver = False
					gameExit = True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p:
						gameIntro()
					if event.key == pygame.K_q:
						gameOver = False
						gameExit = True


		#---------- HOW USERS WILL INTERACT WITH KEYBOARD ----------
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					pygame.quit()
					quit()
				if event.key == pygame.K_LEFT:
					rocket_change = -5
				if event.key == pygame.K_RIGHT:
					rocket_change = 5
				if event.key == pygame.K_SPACE:
					if ammunition > 0:
						bullet = Bullet()
						bullet.rect.x = rocket.rect.x + 48
						bullet.rect.y = rocket.rect.y
						all_sprites_list.add(bullet)
						bullet_list.add(bullet)
						ammunition -= 1

		#---------- ROCKET MOVEMENT ------------
		rocket.rect.x += rocket_change
		if rocket.rect.x > 330:
			rocket.rect.x = 330
		if rocket.rect.x < -10:
			rocket.rect.x = -10


		#---------- DETECTING COLLISION BETWEEN BULLET AND ASTEROIDS
		for bullet in bullet_list:
			bullet_list.remove(bullet)
			bullet.collide(asteroid_list)
			bullet_list.add(bullet)

		#---------- DETECTING COLLISION BETWEEN ROKCET AND ASTEROIDS
		for rocket in player_list:
			player_list.remove(rocket)
			rocket.collide(asteroid_list)
			player_list.add(rocket)

		if ammunition < 0:
			ammunition = 0

		if strength <= 0:
			gameOver = True

		# Call the update() method on all the sprites
		all_sprites_list.update()

		# ---------- DISPLAY THINGS ON SCREEN ----------
		gameDisplay.blit(introimg2, (-70,0))
		score(strength, "Strength: ", 30)
		score(ammunition, "Bullets: ", 50)
		score(distance, "Distance: ", 70)
		distance += 1;


		# Draw all the spites
		all_sprites_list.draw(gameDisplay)

		#---------- UPDATE SCREEN ----------
		pygame.display.flip()

		# --- CLOCK TICK IN FPS ----------
		clock.tick(30)

	# --- END OF WHILE LOOP MEANS QUIT ----------
	pygame.quit()
	quit()

#----- CALLING THE GAME INTRO AND GAME LOOP --------
gameIntro()
gameLoop()
