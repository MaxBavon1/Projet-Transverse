from pygame.locals import *
import pygame
import time

from .ui import *
from .game import *


class Rules(Menu):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.UIManager = UIManager()
        self.UIManager.add_button((0, 0), (200, 200), "RULES")
    
    def events(self):
		# --- Touch Keys ---
        for event in pygame.event.get():
            if event.type == QUIT:
               self.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.UIManager.clicked()

    def update(self):
        self.app.clock.tick(self.app.FPS)

        self.app.mousePos = pygame.Vector2(pygame.mouse.get_pos())

        self.UIManager.update()

    def render(self):
        self.app.window.fill((135, 135, 135))
        self.UIManager.render(self.app.window)
        pygame.display.update()

class Settings(Menu):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.UIManager = UIManager()
        self.UIManager.add_button((0, 0), (200, 200), "SETTINGS")
    
    def events(self):
		# --- Touch Keys ---
        for event in pygame.event.get():
            if event.type == QUIT:
               self.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.UIManager.clicked()

    def update(self):
        self.app.clock.tick(self.app.FPS)

        self.app.mousePos = pygame.Vector2(pygame.mouse.get_pos())

        self.UIManager.update()

    def render(self):
        self.app.window.fill((135, 135, 135))
        self.UIManager.render(self.app.window)
        pygame.display.update()

class Credits(Menu):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.UIManager = UIManager()
        self.UIManager.add_button((0, 0), (200, 200), "CREDITS")
        self.UIManager.buttons.append(Label((500, 600), "TEST", (49,175,212), (226,40,220)))
    
    def events(self):
		# --- Touch Keys ---
        for event in pygame.event.get():
            if event.type == QUIT:
               self.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.UIManager.clicked()

    def update(self):
        self.app.clock.tick(self.app.FPS)

        self.app.mousePos = pygame.Vector2(pygame.mouse.get_pos())

        self.UIManager.update()

    def render(self):
        self.app.window.fill((135, 135, 135))
        self.UIManager.render(self.app.window)
        pygame.display.update()

class Levels(Menu):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.UIManager = UIManager()
        self.UIManager.add_button((0, 0), (200, 200), "LEVELS")
        self.UIManager.buttons.append(Label((800, 400), "LEVEL1", (49,175,212), (226,40,220), command=lambda:self.app.load_menu("game", 1)))
        self.UIManager.buttons.append(Label((800, 500), "LEVEL2", (49,175,212), (226,40,220), command=lambda:self.app.load_menu("game", 2)))
        self.UIManager.buttons.append(Label((800, 600), "LEVEL3", (49,175,212), (226,40,220), command=lambda:self.app.load_menu("game", 3)))

    def events(self):
		# --- Touch Keys ---
        for event in pygame.event.get():
            if event.type == QUIT:
               self.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.UIManager.clicked()

    def update(self):
        self.app.clock.tick(self.app.FPS)

        self.app.mousePos = pygame.Vector2(pygame.mouse.get_pos())

        self.UIManager.update()

    def render(self):
        self.app.window.fill((135, 135, 135))
        self.UIManager.render(self.app.window)
        pygame.display.update()

class MainMenu(Menu):

    def __init__(self):
        super().__init__()
        pygame.init()
        Button.init(self)
        Label.init(self)
        # ==== Window ====
        self.WIDTH = 0 ; self.HEIGHT = 0
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.WIDTH, self.HEIGHT = self.window.get_size()
        self.clock = pygame.time.Clock()
        self.FPS = 144
        self.mousePos = pygame.Vector2(0)
        self.ticks = 0

        self.font = pygame.font.Font("assets/fonts/rubik.ttf", 20)
        self.font_UI = pygame.font.Font("assets/fonts/rubik.ttf", 50)
        self.assets = Assets(self)
        self.assets.ui["main_bg"] = pygame.transform.scale(self.assets.ui["main_bg"], (self.WIDTH, self.HEIGHT))
        

        self.menus = {
            "game" : GameManager(self),
            "rules" : Rules(self),
            "settings" : Settings(self),
            "credits" : Credits(self),
            "levels" : Levels(self)
        }
        self.current_menu = ""

        self.UIManager = UIManager()
        self.UIManager.add_button((self.WIDTH // 2, self.HEIGHT // 4), (200, 100), "PLAY", command=lambda:self.load_menu("levels"))
        self.UIManager.add_button((self.WIDTH // 2, self.HEIGHT // 4 + 100), (200, 100), "RULES", command=lambda:self.load_menu("rules"))
        self.UIManager.add_button((self.WIDTH // 2, self.HEIGHT // 4 + 200), (200, 100), "SETTINGS", command=lambda:self.load_menu("settings"))
        self.UIManager.add_button((self.WIDTH // 2, self.HEIGHT // 4 + 300), (200, 100), "CREDITS", command=lambda:self.load_menu("credits"))
        self.UIManager.add_button((self.WIDTH // 2, self.HEIGHT // 4 + 400), (200, 100), "QUIT", command=self.quit)
    
    def load_menu(self, menu, lvl=0):
        self.current_menu = menu
        if menu != "game":
            self.menus[self.current_menu].run()
        else:
            self.menus[self.current_menu].run(lvl)

    def events(self):
		# --- Touch Keys ---
        for event in pygame.event.get():
            if event.type == QUIT:
               self.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.UIManager.clicked()

    def update(self):
        self.clock.tick(self.FPS)

        self.mousePos = pygame.Vector2(pygame.mouse.get_pos())

        self.UIManager.update()

    def render(self):
        self.window.fill((135, 135, 135))
        self.window.blit(self.assets.ui["main_bg"], (0, 0))
        self.UIManager.render(self.window)
        pygame.display.update()