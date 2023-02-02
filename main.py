from scripts.bullet import *
from scripts.slime import *
from random import randint
import pygame

window = pygame.display.set_mode((960, 544))

clock = pygame.time.Clock()
deltaTime = 0

posx, posy = 256, 256
width, height = 25, 25
speed = 8
color = (0, 0, 255)	

sprite = pygame.image.load("assets/idle.png").convert_alpha()
sprite = pygame.transform.scale(sprite, (sprite.get_width()*2, sprite.get_height()*2))

slime_sprite = pygame.image.load("assets/slime.png").convert_alpha()
slime_sprite = pygame.transform.scale(slime_sprite, (slime_sprite.get_width()*2, slime_sprite.get_height()*2))

bullet_sprite = pygame.image.load("assets/bulletd.png").convert_alpha()
bullet_sprite = pygame.transform.scale(bullet_sprite, (bullet_sprite.get_width()*2, bullet_sprite.get_height()*2))

background = pygame.image.load("assets/background.png").convert_alpha()

bullets = []
slimes = []

def shoot():
	bullets.append(Bullet(posx + width / 2, posy + height / 2))

def spawn():
	slimes.append(Slime(960, randint(0, 500), 1))

while 1:

	# Input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				exit()
			if event.key == pygame.K_SPACE:
				shoot()
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
	spawn()

	for i in range(len(slimes)):
		slime = slimes[i]
		slime_rect = pygame.Rect((slime.x, slime.y), slime_sprite.get_size())
		for j in range(i, len(bullets)):
			if bullets[j].collide(bullet_sprite, slime_rect):
				slime.health -= 1
				bullets.pop(j)

	for slime in slimes:
		slime.update(deltaTime)
		if not(slime.alive):
			slimes.remove(slime)

	for bullet in bullets:
		bullet.update(deltaTime)

	# Render
	window.blit(background, (0, 0))

	# Bullets
	for slime in slimes:
		slime.render(window, slime_sprite)

	for bullet in bullets:
		bullet.render(window, bullet_sprite)
	# Player
	window.blit(sprite, (posx, posy))

	pygame.display.update()