from .entity import *
from .bullet import *
import pygame

class Player(Entity):
    
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.jumpForce = 2.5

    def update(self, deltaTime, gravityScale):
        self.velocity.x = 0
        keyboard = pygame.key.get_pressed()
        if keyboard[pygame.K_d]:
            self.velocity.x = 1
        if keyboard[pygame.K_q]:
            self.velocity.x = -1
        if keyboard[pygame.K_j]:
            self.shoot()

        super().update(deltaTime, gravityScale)
    
    def jump(self):
        self.velocity.y -= self.jumpForce
    
    def shoot(self):
        direction = pygame.Vector2(pygame.mouse.get_pos()) - self.position
        self.manager.spawn("bullet", self.position, Bullet.bulletForce, vel=direction.normalize())