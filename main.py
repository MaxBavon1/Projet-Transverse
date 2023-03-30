# ---- Development Branch (In Progress) ----
from pygame.locals import *
from scripts.camera import *
from scripts.entityManager import *
from scripts.level import *
from scripts.ui import *
import pygame
import time

#quoicoubeh dd

class GameManager:

	def __init__(self) -> None:
		pygame.init()
		Button.init(self)
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
		self.debugMode = False
		self.fixedUpdate = False
		self.mousePos = pygame.Vector2(0)
		self.ticks = 0
		self.font = pygame.font.Font("assets/fonts/rubik.ttf", 20)
		pygame.mouse.set_visible(False)
		# ==== Game ====
		self.gravityScale = 1500
		self.entityManager = EntityManager(self)
		self.camera = Camera(self, self.entityManager.player)
		self.level = Level(self)
		# ==== UI ====
		self.button = Button((0, 0), (200, 200), "Hello")

	def events(self):
		# --- Touch Keys ---
		for event in pygame.event.get():
			if event.type == QUIT:
				self.quit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.quit()
				if event.key == K_F3:
					self.debugMode = not self.debugMode
				if event.key == K_F5:
					self.fixedUpdate = not self.fixedUpdate
				# if event.key == K_F6:
				# 	self.FPS -= 10
				# if event.key == K_F7:
				# 	self.FPS += 10
				if event.key == K_SPACE or event.key == K_UP:
					if self.entityManager.player.grounded:	
						self.entityManager.player.jump()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:	
					self.entityManager.player.shoot()
		
		# --- Hold Keys ---
		keyboard = pygame.key.get_pressed()
		if keyboard[K_F6]:
			self.FPS -= 1
		if keyboard[K_F7]:
			self.FPS += 1

	def update(self):
		self.clock.tick(self.FPS)
		self.deltaTime =  time.time() - self.lastFrame
		if self.fixedUpdate: self.deltaTime = 1 / 144
		self.lastFrame = time.time()
		self.ticks = pygame.time.get_ticks() * 0.001
		self.currentFps = round(self.clock.get_fps())
		self.mousePos = pygame.Vector2(pygame.mouse.get_pos())

		self.entityManager.update(self.deltaTime, self.gravityScale)
		self.camera.update(self.deltaTime)

	def render(self):
		self.window.fill((135, 135, 135))

		self.level.render(self.window, self.camera)

		self.entityManager.render(self.window, self.camera)

		if self.debugMode:
			self.render_debug()
		if self.fixedUpdate:
			self.render_update_mode()
		
		self.button.update()

		self.window.blit(game_sprites["cursor"], self.mousePos - (pygame.Vector2(game_sprites["cursor"].get_size()) / 2))

		pygame.display.update()

	def render_debug(self):
		fps_txt = f"FPS : {self.currentFps} / MaxFPS : {self.FPS}"
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
		self.button.render(self.window)

		self.camera.render_debug(self.window)

	def render_update_mode(self):
		surface = pygame.Surface((self.WIDTH, self.HEIGHT))
		surface.set_alpha(25)
		surface.fill((255, 0, 0))
		self.window.blit(surface, (0, 0))

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