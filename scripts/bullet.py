from .entity import *
import pygame

class Bullet(Entity):
    
    lifeSpan = 4
    bulletForce = 1000

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.spawnTime = self.manager.game.ticks
    
    def update(self, deltaTime, gravityScale):
        if self.manager.game.ticks - self.spawnTime > self.lifeSpan:
            self.alive = False
        
        super().update(deltaTime, gravityScale)

    def on_collision(self, entity):
        if entity.tag == "slime":
            self.alive = False
    
