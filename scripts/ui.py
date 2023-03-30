import pygame

class Button:

    game = None

    def __init__(self, pos, size, text="", txt_color=(255,255,255), bg=(0,0,0), command=None):
        self.rect = pygame.Rect(pos, size)
        self.text_surface = self.game.font.render(text, 1, txt_color)
        self.text_position = self.rect.centerx - self.game.font.size(text)[0], self.rect.centery
        self.background = bg
        self.hover_color = (bg[0] + 100, bg[1] + 100, bg[2] + 100)
        self.hover = False
    
    @classmethod
    def init(cls, game):
        cls.game = game

    def update(self):
        self.hover = False
        if self.rect.collidepoint(self.game.mousePos.x, self.game.mousePos.y):
            self.hover = True
    
    def render(self, surface):
        if self.hover:
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.background, self.rect)
        surface.blit(self.text_surface, self.text_position)