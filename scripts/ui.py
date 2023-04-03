import pygame

class UIManager:

    def __init__(self, game):
        self.buttons = []
        #self.add_button((0, 0), (100, 80), "Hello")

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

    game = None

    def __init__(self, pos, size, text="", txt_color=(255,255,255), bg=(0,0,0), border=(255, 255, 255), command=lambda:0):
        self.rect = pygame.Rect(pos, size)
        self.text_surface = self.game.font.render(text, 1, txt_color)
        self.text_position = self.rect.centerx - (self.game.font.size(text)[0]/2), self.rect.centery - (self.game.font.size(text)[1]/2)
        self.background = bg
        self.hover_color = (bg[0] + 100, bg[1] + 100, bg[2] + 100)
        self.border = border
        self.hover = False
        self.command = command
    
    @classmethod
    def init(cls, game):
        cls.game = game
    
    def collide(self):
        return self.rect.collidepoint(self.game.mousePos.x, self.game.mousePos.y)

    def render(self, surface):
        if self.hover:
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.background, self.rect)
        surface.blit(self.text_surface, self.text_position)
    
        pygame.draw.rect(surface, self.border, self.rect, 2)