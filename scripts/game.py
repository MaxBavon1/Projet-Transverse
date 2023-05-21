import pygame
import time
from pygame.locals import *

from .camera import *
from .entityManager import *
from .level import *
from .ui import *
from .menus import *


__all__ = ["GameManager"]


class GameManager(Menu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ==== Window ====
        self.WIDTH, self.HEIGHT = self.window.get_size()

        self.currentFps = 0
        self.deltaTime = 0
        self.lastFrame = 0
        self.debugMode = False
        self.fixedUpdate = False
        self.mousePos = pygame.Vector2(pygame.mouse.get_pos())
        self.ticks = 0

        self.level = Level(self)
        self.entityManager = EntityManager(self)
        self.camera = Camera(self)
    
    def load_level(self, lvl):
        """ Game Loading Datas, Entities, Levels """
        self.lastFrame = time.time()
        pygame.mouse.set_visible(False)
        self.gravityScale = 1700

        self.level.load_level(lvl)
        self.entityManager.load_level(self.level.layers["entities"])
        self.camera.follow(self.entityManager.player)
        # self.UIManager = UIManager()

    def events(self, event):
        if event.type == KEYDOWN:
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

    def update(self):
        keyboard = pygame.key.get_pressed()
        if keyboard[K_F6]:
            self.FPS -= 1
        if keyboard[K_F7]:
            self.FPS += 1

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
        self.level.render(self.window, self.camera)

        self.entityManager.render(self.window, self.camera)

        if self.debugMode:
            self.render_debug()
        if self.fixedUpdate:
            self.render_update_mode()
           
        # self.UIManager.render(self.window)

        self.window.blit(self.assets.ui["cursor"], self.mousePos - (pygame.Vector2(self.assets.ui["cursor"].get_size()) / 2))

    def render_text(self, text, pos, font="rubik20"):
        current_font = self.assets.fonts[font]
        surf = current_font.render(text, 1, (255, 255, 255))
        self.window.blit(surf, pos)

    def render_text_debug(self, text, y, font="rubik20"):
        current_font = self.assets.fonts[font]
        surf = current_font.render(text, 1, (255, 255, 255))
        self.window.blit(surf, (self.WIDTH - current_font.size(text)[0], y))

    def render_debug(self):
        fps_txt = f"FPS : {self.currentFps} / MaxFPS : {self.FPS}"
        entity_txt = f"E : {self.entityManager.size}"
        pos_txt = f"X,Y : {round(self.entityManager.player.position.x)} / {round(self.entityManager.player.position.y)}"
        vel_txt = f"Vel : {round(self.entityManager.player.velocity.x)} / {round(self.entityManager.player.velocity.y)}"

        self.render_text_debug(fps_txt, 0)
        self.render_text_debug(entity_txt, 20)
        self.render_text_debug(pos_txt, 40)
        self.render_text_debug(vel_txt, 60)

        self.camera.render_debug(self.window)

    def render_update_mode(self):
        surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        surface.set_alpha(25)
        surface.fill((255, 0, 0))
        self.window.blit(surface, (0, 0))

    def run(self, lvl):
        print("[LAUNCHING GAME...]")

        self.load_level(lvl)
        super().run()

    def quit(self):
        print("[QUITING GAME...]")
        pygame.mouse.set_visible(True)
        self.running = False


# if __name__ == "__main__":
# 	GameManager().run()