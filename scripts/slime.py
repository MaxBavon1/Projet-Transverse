from .entity import *
import pygame

class Slime(Entity):

    def __init__(self, *args, **kwargs):
        self.target = args[-1]
        args = list(args)
        args.pop(-1)
        super().__init__(*args, anim_speed=15, **kwargs)

    def update(self, deltaTime, gravityScale):
        movement = pygame.Vector2(self.target.position - self.position).normalize()
        self.velocity.x = movement.x * self.speed
        super().update(deltaTime, gravityScale)

    def on_collision(self, entity):
        if entity.tag == "bullet":
            self.health -= 1
    
