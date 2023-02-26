# ---- Development Branch (In Progress) ----
from scripts.image import *
from scripts.entity import *
from scripts.bullet import *
import pygame

print(PATH)

class GameManager:

	def __init__(self) -> None:
		# ==== Window ====
		self.WIDTH = 1024
		self.HEIGHT = 512
		self.window = pygame.display.set_mode((1024, 512))
		self.clock = pygame.time.Clock()
		self.deltaTime = 0
		# ==== Game ====
		self.player = Entity((256, 256), 8, load_image("assets/idle.png", 2))
		self.bullets = []

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					pass
					# shoot()

	def update(self):
		self.deltaTime = self.clock.tick(60) * 0.01

		self.player.update(self.deltaTime)

		for bullet in self.bullets:
			bullet.update(self.deltaTime)

	def render(self):
		self.window.fill((135, 135, 135))

		self.player.render(self.window)

		for bullet in self.bullets:
			bullet.render(self.window)

		pygame.display.update()

	def run(self):
		print("[LAUNCHING GAME...]")
		while 1:
			self.events()
			self.update()
			self.render()

	def quit(self):
		print("[QUITING GAME...]")
		pygame.quit()
		exit()


if __name__ == "__main__":
	GameManager().run()