from .entity import *
from .bullet import *
import pygame


class Player(Entity):
    
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.jumpForce = 475
        self.speed = 200
        self.health = 300

    def update(self, *args):
        if self.health <= 0:
            self.entityManager.game.quit()

        keyboard = pygame.key.get_pressed()
        self.velocity.x = 0
        if keyboard[pygame.K_d] or keyboard[pygame.K_RIGHT]:
            self.velocity.x = self.speed
        if keyboard[pygame.K_q] or keyboard[pygame.K_LEFT]:
            self.velocity.x = -self.speed

        if keyboard[pygame.K_j]:
            self.shoot()
        if keyboard[pygame.K_LSHIFT]:
            self.velocity.y -= 20

        super().update(*args)
    
    def jump(self):
        self.velocity.y -= self.jumpForce
    
    def shoot(self):
        direction = pygame.Vector2(pygame.mouse.get_pos()) - self.position
        self.entityManager.bullets.spawn(self.position, vel=direction.normalize())
    
    def render(self, surface):
        super().render(surface)

        health_txt = f"HP : {self.health}"
        health_surf = self.entityManager.game.font.render(health_txt, 1, (255,255,255))
        surface.blit(health_surf, (0, 0))