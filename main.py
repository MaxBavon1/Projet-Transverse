# ---- Development Branch (In Progress) ----
from scripts.entityManager import *
from pygame.locals import *
import pygame


class GameManager:

	def __init__(self) -> None:
		pygame.init()
		# ==== Window ====
		self.WIDTH = 0
		self.HEIGHT = 0
		self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
		self.WIDTH, self.HEIGHT = self.window.get_size()
		self.clock = pygame.time.Clock()
		self.FPS = 144
		self.currentFps = 0
		self.deltaTime = 0
		self.debugMode = False
		self.ticks = 0
		self.gravityScale = 9.81
		# ==== Game ====
		self.entityManager = EntityManager(self)
		self.entityManager.init()
		self.ground = pygame.Rect(0, self.HEIGHT-400, 1000 , 256)
		self.font = pygame.font.Font("assets/fonts/rubik.ttf", 20)

	def events(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.quit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.quit()
				if event.key == K_F3:
					self.debugMode = not self.debugMode
				if event.key == K_SPACE:
					if self.entityManager.player.grounded:	
						self.entityManager.player.jump()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					self.entityManager.player.shoot()

	def update(self):
		self.deltaTime = self.clock.tick(self.FPS) * 0.001
		self.ticks = pygame.time.get_ticks() * 0.001
		self.currentFps = round(self.clock.get_fps())

		self.entityManager.update(self.deltaTime, self.gravityScale)

	def render(self):
		self.window.fill((135, 135, 135))
		pygame.draw.rect(self.window, (100,200,100), self.ground)
		pygame.draw.rect(self.window, (70,70,70), self.ground, 10)

		self.entityManager.render(self.window)
	
		if self.debugMode:
			fps_txt = f"FPS : {self.currentFps}"
			entity_txt = f"E : {self.entityManager.size}"
			fps_surf = self.font.render(fps_txt, 1, (255,255,255))
			entity_surf = self.font.render(entity_txt, 1, (255,255,255))
			self.window.blit(fps_surf, (self.WIDTH - self.font.size(fps_txt)[0], 0))
			self.window.blit(entity_surf, (self.WIDTH - self.font.size(entity_txt)[0], 20))

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