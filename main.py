from scripts.bullet import *
import pygame

window = pygame.display.set_mode((512, 512))

clock = pygame.time.Clock()
deltaTime = 0

posx, posy = 256, 256
width, height = 25, 25
speed = 8
color = (0, 0, 255)	

sprite = pygame.image.load("D:/Programmation/Python/Projects/Example/assets/idle.png").convert_alpha()
sprite = pygame.transform.scale(sprite, (sprite.get_width()*2, sprite.get_height()*2))

bullet_sprite = pygame.image.load("D:/Programmation/Python/Projects/Example/assets/bulletd.png").convert_alpha()
bullet_sprite = pygame.transform.scale(bullet_sprite, (bullet_sprite.get_width()*2, bullet_sprite.get_height()*2))

background = pygame.image.load("D:/Programmation/Python/Projects/Example/assets/background.png").convert_alpha()

bullets = []

def shoot():
	bullets.append(Bullet(posx + width / 2, posy + height / 2))

while 1:

	# Input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				shoot()


	keyboard = pygame.key.get_pressed()
	if keyboard[pygame.K_d]:
		posx += speed * deltaTime
	if keyboard[pygame.K_q]:
		posx -= speed * deltaTime
	if keyboard[pygame.K_z]:
		posy -= speed * deltaTime
	if keyboard[pygame.K_s]:
		posy += speed * deltaTime

	# Update
	deltaTime = clock.tick(60) * 0.01

	for bullet in bullets:
		bullet.update(deltaTime)

	# Render
	window.blit(background, (0, 0))

	# Bullets
	for bullet in bullets:
		bullet.render(window, bullet_sprite)
	# Player
	window.blit(sprite, (posx, posy))

	pygame.display.update()