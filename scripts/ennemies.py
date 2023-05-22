import pygame

from .entity import *


__all__ = ["Zombie"]


class Zombie(Entity):

    def __init__(self, data, target, animations, pos):
        super().__init__(animations, pos, data["speed"], (0,0), data["health"], data["damage"], data["anim_speed"], "zombie")
        self.target = target
        self.speed = 100
        self.jumpForce = 500
        self.health = data["health"]

        self.hit = False
        self.move_cooldown = 1
        self.hit_cooldown = 1
        self.last_hit = self.hit_cooldown

    def jump(self):
        self.velocity.y -= self.jumpForce

    def animate(self):
        if not self.hit:
            if self.direction == "right":
                self.play("run_right")
            else:
                self.play("run_left")

        super().animate()

    def set_animation_rect(self, animation, sprite):
        left, right, top, bottom = self.hitbox.left, self.hitbox.right, self.hitbox.top, self.hitbox.bottom # Saves old position
        self.set_size(sprite.get_size()) # Then resize the sprite to fit new animation

        # Finally reset the position before the sprite switch
        if self.direction == right: self.set_right(right)
        else: self.set_left(left)
        if self.velocity.y > 0: self.set_top(top)
        else: self.set_bottom(bottom)

    def update(self, deltaTime, gravityScale):
        self.hit = not self.last_hit >= self.move_cooldown
        self.last_hit += deltaTime

        self.velocity.x = 0
        if not self.hit:
            mouvement = (self.target.position - self.position).normalize()
            self.velocity.x = mouvement.x * self.speed
            if mouvement.y < 0 and self.grounded:
                self.jump()

            if self.velocity.x > 0:
                self.direction = "right"
            else:
                self.direction = "left"
        
        super().update(deltaTime, gravityScale)

    def take_damage(self, damage):
        if self.last_hit >= self.hit_cooldown:
            self.last_hit = 0
            self.health -= damage
            if self.direction == "right": self.play("hit_right")
            else: self.play("hit_left")