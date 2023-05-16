# ---- Development Branch (In Progress) ----
from pygame.locals import *
from .camera import *
from .entityManager import *
from .level import *
from .ui import *
import pygame
import time

#quoicoubeh

class GameManager(Menu):

    def __init__(self, app) -> None:
        super().__init__()
        # ==== Window ====
        self.WIDTH, self.HEIGHT = app.WIDTH, app.HEIGHT
        self.window = app.window
        self.clock = app.clock
        self.FPS = app.FPS
        self.currentFps = 0
        self.deltaTime = 0
        self.lastFrame = 0
        self.debugMode = False
        self.fixedUpdate = False
        self.mousePos = app.mousePos
        self.ticks = app.ticks
        self.font = app.font
        # ==== Game ====
        self.gravityScale = 1700
        self.assets = app.assets
        self.level = None
        self.entityManager = EntityManager(self)
        self.camera = Camera(self, self.entityManager.player)
        # self.UIManager = UIManager()

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
                if event.key == K_SPACE or event.key == K_UP:
                    if self.entityManager.player.grounded:	
                        self.entityManager.player.jump()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:	
                    self.entityManager.player.shoot()
                    # self.UIManager.clicked()
           
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
        # self.UIManager.update()

    def render(self):
        self.window.fill((135, 135, 135))

        self.level.render(self.window, self.camera)

        self.entityManager.render(self.window, self.camera)

        if self.debugMode:
            self.render_debug()
        if self.fixedUpdate:
            self.render_update_mode()
           
        # self.UIManager.render(self.window)

        self.window.blit(self.assets.ui["cursor"], self.mousePos - (pygame.Vector2(self.assets.ui["cursor"].get_size()) / 2))

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

        self.camera.render_debug(self.window)

    def render_update_mode(self):
        surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        surface.set_alpha(25)
        surface.fill((255, 0, 0))
        self.window.blit(surface, (0, 0))

    def load_level(self, lvl):
        self.lastFrame = time.time()
        self.entityManager = EntityManager(self)
        self.camera = Camera(self, self.entityManager.player)
        self.level = Level(self, lvl)


    def run(self, lvl):
        print("[LAUNCHING GAME...]")

        self.load_level(lvl)
        pygame.mouse.set_visible(False)
        
        super().run()

    def quit(self):
        print("[QUITING GAME...]")
        pygame.mouse.set_visible(True)
        super().quit()


# if __name__ == "__main__":
# 	GameManager().run()