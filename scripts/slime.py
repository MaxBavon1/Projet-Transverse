from .entity import *
import pygame

class Slime(Entity2):

    def __init__(self, target, *args, **kargs):
        super().__init__(*args, **kargs)
        self.target = target
    
    def update(self, deltaTime, gravityScale):
        movement = (pygame.Vector2self.target.rect.center - self.rect.center).normalize()
        self.velocity.x = movement.x
        super().update(deltaTime, gravityScale)

    def on_collision(self, entity):
        if entity.tag == "bullet":
            self.health -= 1
    
