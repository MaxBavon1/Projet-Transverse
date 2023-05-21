from .entity import *
from .bullet import *
import pygame


class Player(Entity):
    
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.anim_speed = 8
        self.jumpForce = 600
        self.speed = 250
        self.health = 300
        self.flyingSpeed = 2500
        self.direction = "right"
        self.play("walk_right")
    
    def animate(self):
        if self.direction == "right":
            if self.velocity.y == 0:
                self.play("idle_right") if self.velocity.x == 0 else self.play("walk_right")
            else:
                self.play("fall_right") if self.velocity.y > 0 else self.play("jump_right")
        else:
            if self.velocity.y == 0:
                self.play("idle_left") if self.velocity.x == 0 else self.play("walk_left")
            else:
                self.play("fall_left") if self.velocity.y > 0 else self.play("jump_left")

        super().animate()

    def update(self, *args):
        if self.health <= 0:
            self.entityManager.game.quit()

        keyboard = pygame.key.get_pressed()
        self.velocity.x = 0
        if keyboard[pygame.K_d] or keyboard[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.direction = "right"
        if keyboard[pygame.K_q] or keyboard[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.direction = "left"

        if keyboard[pygame.K_TAB]:
            self.shoot()
        if keyboard[pygame.K_LSHIFT]:
            self.velocity.y -= self.flyingSpeed * args[0]

        super().update(*args)
    
    def jump(self):
        self.velocity.y -= self.jumpForce
    
    def shoot(self):
        cursor = self.entityManager.game.camera.screen_to_world_point(pygame.mouse.get_pos())
        direction = (pygame.Vector2(cursor) - self.position)
        self.entityManager.bullets.spawn(self.position, vel=direction.normalize())

    def render(self, surface, camera):
        super().render(surface, camera.offset, camera.rect)

        health_txt = f"HP : {self.health}"
        self.entityManager.game.render_text(health_txt, (0, 0))