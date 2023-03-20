# ---- Development Branch (In Progress) ----
from pygame.locals import *
from scripts.entityManager import *
from scripts.level import *
import pygame
import time

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
		self.lastFrame = 0
		self.debugMode = True
		self.ticks = 0
		self.font = pygame.font.Font("assets/fonts/rubik.ttf", 20)
		# ==== Game ====
		self.gravityScale = 9.81
		self.entityManager = EntityManager(self)
		self.level = Level(self)

	def events(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.quit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.quit()
				if event.key == K_F3:
					self.debugMode = not self.debugMode
				if event.key == K_SPACE or event.key == K_UP:
					if self.entityManager.player.grounded:	
						self.entityManager.player.jump()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:	
					self.entityManager.player.shoot()

	def update(self):
		self.clock.tick(self.FPS)
		self.deltaTime =  time.time() - self.lastFrame
		self.lastFrame = time.time()
		self.ticks = pygame.time.get_ticks() * 0.001
		self.currentFps = round(self.clock.get_fps())

		self.entityManager.update(self.deltaTime, self.gravityScale)

	def render(self):
		self.window.fill((135, 135, 135))

		self.level.render(self.window)

		self.entityManager.render(self.window)

		if self.debugMode:
			self.render_debug()

		pygame.display.update()

	def render_debug(self):
		fps_txt = f"FPS : {self.currentFps}"
		entity_txt = f"E : {self.entityManager.size}"
		fps_surf = self.font.render(fps_txt, 1, (255,255,255))
		entity_surf = self.font.render(entity_txt, 1, (255,255,255))
		self.window.blit(fps_surf, (self.WIDTH - self.font.size(fps_txt)[0], 0))
		self.window.blit(entity_surf, (self.WIDTH - self.font.size(entity_txt)[0], 20))

		pos_txt = f"X,Y : {round(self.entityManager.player.position.x)} / {round(self.entityManager.player.position.y)}"
		vel_txt = f"Vel : {round(self.entityManager.player.velocity.x)} / {round(self.entityManager.player.velocity.y)}"
		
		pos_surf = self.font.render(pos_txt, 1, (255,255,255))
		vel_surf = self.font.render(vel_txt, 1, (255,255,255))
		self.window.blit(pos_surf, (self.WIDTH - self.font.size(pos_txt)[0], 40))
		self.window.blit(vel_surf, (self.WIDTH - self.font.size(vel_txt)[0], 60))

	def run(self):
		print("[LAUNCHING GAME...]")
		self.lastFrame = time.time()
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