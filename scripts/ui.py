from pygame.locals import *
import pygame
from abc import ABC, abstractmethod


class UIManager:

    def __init__(self):
        self.buttons = []

    def add_button(self, *args, **kwargs):
        self.buttons.append(Button(*args, **kwargs))

    def clicked(self):
        for button in self.buttons:
            if button.collide():
                button.command()
        
    def update(self):
        for button in self.buttons:
            button.hover = False
            if button.collide():
                button.hover = True
    
    def render(self, surface):
        for button in self.buttons:
            button.render(surface)


class Button:

    app = None

    def __init__(self, pos, size, text="", txt_color=(255,255,255), bg=(0,0,0), border=(255, 255, 255), command=lambda:0):
        self.rect = pygame.Rect(pos, size)
        self.text_surface = self.app.font.render(text, 1, txt_color)
        self.text_position = self.rect.centerx - (self.app.font.size(text)[0]/2), self.rect.centery - (self.app.font.size(text)[1]/2)
        self.background = bg
        self.hover_color = (bg[0] + 100, bg[1] + 100, bg[2] + 100)
        self.border = border
        self.hover = False
        self.command = command
    
    @classmethod
    def init(cls, app):
        cls.app = app
    
    def collide(self):
        return self.rect.collidepoint(self.app.mousePos.x, self.app.mousePos.y)

    def render(self, surface):
        if self.hover:
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.background, self.rect)
        surface.blit(self.text_surface, self.text_position)
    
        pygame.draw.rect(surface, self.border, self.rect, 2)

class Label:
    
    app = None

    def __init__(self, pos, text="", txt_color=(255,255,255), hover_color=(0,0,0), command=lambda:0):
        self.txt = text
        self.text_surface = self.app.font_UI.render(text, 1, txt_color)
        self.rect = pygame.Rect(pos, (self.app.font_UI.size(text)[0], self.app.font_UI.size(text)[1]))
        self.txt_color = txt_color
        self.hover_color = hover_color
        self.hover = False
        self.command = command
    
    @classmethod
    def init(cls, app):
        cls.app = app
    
    def collide(self):
        return self.rect.collidepoint(self.app.mousePos.x, self.app.mousePos.y)

    def render(self, surface):
        if self.hover:
            self.text_surface = self.app.font_UI.render(self.txt, 1, self.hover_color)
        else:
            self.text_surface = self.app.font_UI.render(self.txt, 1, self.txt_color)

        surface.blit(self.text_surface, self.rect.topleft)


class Menu(ABC):

    def __init__(self):
        self.running = True

    def events(self):
        # --- Touch Keys ---
        for event in pygame.event.get():
            if event.type == QUIT:
               self.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()

    def run(self):
        self.running = True
        while self.running:
            self.events()
            self.update()
            self.render()

    def quit(self):
        self.running = False

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass