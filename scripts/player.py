from .entity import *
import pygame

class Player(Entity):
    
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
    
    def update(self, deltaTime):
        self.velocity = pygame.Vector2(0)
        keyboard = pygame.key.get_pressed()
        if keyboard[pygame.K_d]:
            self.velocity.x = 1
        if keyboard[pygame.K_q]:
            self.velocity.x = -1
        if keyboard[pygame.K_z]:
            self.velocity.y = -1
        if keyboard[pygame.K_s]:
            self.velocity.y = 1

        super().update(deltaTime)
