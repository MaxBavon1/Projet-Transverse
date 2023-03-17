from .entity import *
from .bullet import *
import pygame

class Player(Entity2):
    
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.jumpForce = 475
        self.speed = 200

    def update(self, *args):
        keyboard = pygame.key.get_pressed()
        self.velocity.x = 0
        if keyboard[pygame.K_d]:
            self.velocity.x = 1
        if keyboard[pygame.K_q]:
            self.velocity.x = -1

        if keyboard[pygame.K_j]:
            self.shoot()
        if keyboard[pygame.K_UP]:
            self.velocity.y -= 20

        super().update(*args)
    
    def jump(self):
        self.velocity.y -= self.jumpForce
    
    def shoot(self):
        direction = pygame.Vector2(pygame.mouse.get_pos()) - self.position
        self.manager.spawn("bullet", self.position, Bullet.bulletForce, vel=direction.normalize())