
from pygame.locals import *
import pygame
import time
import json

from .data import *
from .assets import *
from .ui import *
from .menus import *
from .game import *


__all__ = ["Launch", "Quit"]


# _____ Application Configurations  ____
pygame.init()
DEFAULT_W, DEFAULT_H = 1920, 1080
# MONITO_SIZE = pygame.display.Info().current_w, pygame.display.Info().current_h
window = pygame.display.set_mode((0, 0), DOUBLEBUF | FULLSCREEN, vsync=1)
MONITO_SIZE = window.get_size()
RESIZING = MONITO_SIZE[0] / DEFAULT_W, MONITO_SIZE[1] / DEFAULT_H
print("MONITOR :", MONITO_SIZE)
pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN])
clock = pygame.time.Clock()
FPS = 90

# Assets Game Loading
loading_img = pygame.image.load("assets/ui/loading.jpg").convert()
loading_img = pygame.transform.scale(loading_img, MONITO_SIZE)
window.blit(loading_img, (0, 0))
pygame.display.update()

time.sleep(0) # Prentending loading the game assets takes time...
assets = Assets()
assets.ui["backgroundfinal2"] = pygame.transform.scale(assets.ui["backgroundfinal2"], MONITO_SIZE)
data = Data()
data.load_progress()
Menu.init(window, clock, data, assets)

def Launch():
    MainMenu().run()

def Quit():
    pygame.quit()
    exit()


# class Rules(Menu):

#     def __init__(self, app):
#         super().__init__()
#         self.app = app
#         self.UIManager = UIManager()
#         self.UIManager.add_button((0, 0), (200, 200), "RULES")
    
#     def events(self):
# 		# --- Touch Keys ---
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                self.quit()
#             if event.type == KEYDOWN:
#                 if event.key == K_ESCAPE:
#                     self.quit()
#             if event.type == MOUSEBUTTONDOWN:
#                 if event.button == 1:
#                     self.UIManager.clicked()

#     def update(self):
#         self.app.clock.tick(self.app.FPS)

#         self.app.mousePos = pygame.Vector2(pygame.mouse.get_pos())

#         self.UIManager.update()

#     def render(self):
#         self.app.window.fill((135, 135, 135))
#         self.UIManager.render(self.app.window)
#         pygame.display.update()

# class Settings(Menu):

#     def __init__(self):
#         super().__init__(window, clock)
#         self.UIManager = UIManager()
#         back_but = Label()
#         self.UIManager.add_button((0, 0), (200, 200), "SETTINGS")
    
#     def events(self):
#         pass

#     def update(self):
#         self.UIManager.update(pygame.Vector2(pygame.mouse.get_pos()))

#     def render(self):
#         self.UIManager.render(self.window)


# class Credits(Menu):

#     def __init__(self, app):
#         super().__init__()
#         self.app = app
#         self.UIManager = UIManager()
#         self.UIManager.add_button((0, 0), (200, 200), "CREDITS")
#         # self.UIManager.buttons.append(Label((500, 600), "TEST", (49,175,212), (226,40,220)))

#     def events(self):
# 		# --- Touch Keys ---
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                self.quit()
#             if event.type == KEYDOWN:
#                 if event.key == K_ESCAPE:
#                     self.quit()
#             if event.type == MOUSEBUTTONDOWN:
#                 if event.button == 1:
#                     self.UIManager.clicked()

#     def update(self):
#         self.app.clock.tick(self.app.FPS)

#         self.app.mousePos = pygame.Vector2(pygame.mouse.get_pos())

#         self.UIManager.update()

#     def render(self):
#         self.app.window.fill((135, 135, 135))
#         self.UIManager.render(self.app.window)
#         pygame.display.update()


class Levels(Menu):

    def __init__(self, main, *args, **kargs):
        super().__init__(*args, **kargs)
        self.main = main
        self.UIManager = UIManager()
        
        levels_label = ButtonLabel((MONITO_SIZE[0] / 2, 250 * RESIZING[1]), assets.fonts["rubik80"], "Levels", COLORS["blue"], COLORS["blue"])
        level1_label = ButtonLabel((MONITO_SIZE[0] / 2, 450 * RESIZING[1]), assets.fonts["rubik40"], "Level 1", COLORS["blue"], COLORS["green"], command=lambda:self.load_level(1))
        level2_label = ButtonLabel((MONITO_SIZE[0] / 2, 550 * RESIZING[1]), assets.fonts["rubik40"], "Level 2", COLORS["blue"], COLORS["green"], command=lambda:self.load_level(2))
        level3_label = ButtonLabel((MONITO_SIZE[0] / 2, 650 * RESIZING[1]), assets.fonts["rubik40"], "Level 3", COLORS["blue"], COLORS["green"], command=lambda:self.load_level(3))
        self.UIManager.adds(levels_label, level1_label, level2_label, level3_label)

    def load_level(self, lvl):
        if lvl == 1 or data.progress[f"level {lvl - 1}"]:
            self.main.load_menu("game", lvl)

    def events(self, event):
        pass

    def update(self):
        self.UIManager.update(pygame.Vector2(pygame.mouse.get_pos()))

    def render(self):
        self.UIManager.render(self.window)
    
    def run(self):
        self.UIManager.objects = []
        for i in range(1, data.progress["nb_levels"]):
            if (not data.progress[f"level {i}"]):
                button = self.UIManager.buttons[i + 1]
                self.UIManager.add(Image((button.rect.x - 25, button.rect.centery), assets.ui["lock"]))
                button.hover_color = (255, 0, 0)

        super().run()


class MainMenu(Menu):

    def __init__(self):
        super().__init__(COLORS["grey"], FPS)

        self.UIManager = UIManager()

        play_but = ButtonLabel((MONITO_SIZE[0] / 2, 200 * RESIZING[1]), assets.fonts["rubik80"], "Play", COLORS["cyan"], COLORS["purple"], command=lambda:self.load_menu("levels", 1))
        rules_but = ButtonLabel((MONITO_SIZE[0] / 2, 400 * RESIZING[1]), assets.fonts["rubik60"], "Rules", COLORS["cyan"], COLORS["purple"])
        settings_but = ButtonLabel((MONITO_SIZE[0] / 2, 500 * RESIZING[1]), assets.fonts["rubik60"], "Settings", COLORS["cyan"], COLORS["purple"])
        credits_but = ButtonLabel((MONITO_SIZE[0] / 2, 600 * RESIZING[1]), assets.fonts["rubik60"], "Credits", COLORS["cyan"], COLORS["purple"])
        quit_but = ButtonLabel((MONITO_SIZE[0] / 2, 700 * RESIZING[1]), assets.fonts["rubik60"], "Quit", COLORS["cyan"], COLORS["purple"], command=Quit)

        self.UIManager.adds(play_but, rules_but, settings_but, credits_but, quit_but)


        self.menus = {
            "levels" : Levels(self, COLORS["white"], 90),
            "game" : GameManager(COLORS["blue"], 144)
        }
        self.currentMenu = ""

    def load_menu(self, menu, lvl=0):
        if self.currentMenu and self.menus[self.currentMenu].running:
            self.menus[self.currentMenu].quit()

        self.currentMenu = menu
        if menu != "game":

            self.menus[menu].run()
        else:
            self.menus[menu].run(lvl)

    def events(self, event):
        pass

    def update(self):
        self.UIManager.update(pygame.Vector2(pygame.mouse.get_pos()))

    def render(self):
        self.window.blit(assets.ui["backgroundfinal2"], (0, 0))
        self.UIManager.render(self.window)