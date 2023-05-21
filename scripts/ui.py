from pygame.locals import *
import pygame


__all__ = ["UIManager", "Button", "Label"]


class UIManager:

    __slots__ = ["objects"]

    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def adds(self, *objs):
        for obj in objs:
            self.objects.append(obj)

    def update(self, mousePos):
        for obj in self.objects:
            obj.update(mousePos)
    
    def render(self, surface):
        for obj in self.objects:
            obj.render(surface)


class Button:

    __slots__ = ["image", "rect", "hover_color", "hover_scale", "hover", "command"]

    def __init__(self, pos, img, hover_col=(200, 200, 200), hover_scale=1.1, command=lambda:0):
        self.image = img
        self.rect = img.get_rect(center=pos)
        self.hover_color = hover_col
        self.hover_scale = hover_scale
        self.hover = False
        self.command = command
    
    def collide(self, mousePos):
        return self.rect.collidepoint(mousePos.x, mousePos.y)

    def update(self, mousePos):
        self.hover = self.collide(mousePos)
        
        if (self.hover and pygame.mouse.get_pressed()[0]):
            self.command()

    def render(self, surface):
        if self.hover:
            surf = self.image.copy()
            hover_surf = pygame.Surface(surf.get_size())
            hover_surf.set_alpha(100)
            hover_surf.fill(self.hover_color)
            surf.blit(hover_surf, (0, 0))
            surf = pygame.transform.scale_by(surf, self.hover_scale)
            surface.blit(surf, (self.rect.centerx - surf.get_width() / 2, self.rect.centery - surf.get_height() / 2))
        else:
            surface.blit(self.image, self.rect.topleft)


class Label:
    
    __slots__ = ["text", "font", "rect", "txt_color", "hover_color", "hover_scale", "hover", "command"]

    def __init__(self, pos, font, txt="", txt_color=(255,255,255), hover_color=(0,0,0), command=lambda:0):
        self.text = txt
        self.font = font
        self.rect = pygame.Rect((0, 0, 0, 0))
        self.rect.size = self.font.size(txt)[0], self.font.size(txt)[1]
        self.rect.center = pos
        self.txt_color = txt_color
        self.hover_color = hover_color
        self.hover = False
        self.command = command
    
    def collide(self, mousePos):
        return self.rect.collidepoint(mousePos.x, mousePos.y)

    def update(self, mousePos):
        self.hover = self.collide(mousePos)
        
        if (self.hover and pygame.mouse.get_pressed()[0]):
            self.command()

    def render(self, surface):
        if self.hover:
            surf = self.font.render(self.text, 1, self.hover_color)
        else:
            surf = self.font.render(self.text, 1, self.txt_color)
        
        surface.blit(surf, self.rect.topleft)