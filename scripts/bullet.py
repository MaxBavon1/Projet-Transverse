from .entity import *
import pygame

class Bullet(StaticEntity):
    
    lifeSpan = 15
    bulletForce = 1200
    bounce = (0.75, 0.65)
    bulletDamage = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity *= self.bulletForce
        self.spawnTime = self.entityManager.game.ticks
        self.rebounce = self.lifeSpan
        self.damage = self.bulletDamage

    def bounce_off(self, axis=1):
        self.rebounce -= 1
        self.velocity.x *= axis * self.bounce[0]
        self.velocity.y *= -axis * self.bounce[1]

    def horizontal_collision(self, level):
        if self.rect.left < level.border.left: # Border Left
            self.rect.left = level.border.left
            self.position.x = self.rect.centerx
            self.bounce_off(-1)
        if self.rect.right > level.border.right: # Border Right
            self.rect.right = level.border.right
            self.position.x = self.rect.centerx
            self.bounce_off(-1)

        for tile in level.collide(self): # TileMap
            if self.velocity.x > 0 and self.rect.left < tile.left:
                self.rect.right = tile.left
                self.position.x = self.rect.centerx
                self.bounce_off(-1)
            elif self.velocity.x < 0 and self.rect.right > tile.right:
                self.rect.left = tile.right + 1
                self.position.x = self.rect.centerx
                self.bounce_off(-1)

    def vertical_collision(self, level):
         # ---- Vertical Collisions ----
        if self.rect.top < level.border.top: # Border Top
                self.rect.top = level.border.top
                self.position.y = self.rect.centery
                self.bounce_off(1)
        if self.rect.bottom > level.border.bottom: # Border Bottom
                self.rect.bottom = level.border.bottom
                self.position.y = self.rect.centery
                self.bounce_off(1)

        for tile in level.collide(self): # TileMap
            if self.velocity.y > 0 and self.rect.top < tile.top:
                self.rect.bottom = tile.top
                self.position.y = self.rect.centery
                self.bounce_off(1)

            elif self.velocity.y < 0 and self.rect.bottom > tile.bottom:
                self.rect.top = tile.bottom
                self.position.y = self.rect.centery
                self.bounce_off(1)

    def update(self, deltaTime, gravityScale):
        if (self.entityManager.game.ticks - self.spawnTime) > self.lifeSpan or self.rebounce <= 0:
            self.destroy()

        level = self.entityManager.game.level
        self.position.x += self.velocity.x * deltaTime
        self.rect.centerx = self.position.x
        self.horizontal_collision(level)

        self.velocity.y += gravityScale * deltaTime
        self.position.y += self.velocity.y * deltaTime
        self.rect.centery = self.position.y
        self.vertical_collision(level)

        if (self.grounded and self.velocity.y != 0):
            self.grounded = False

    def on_collision(self, entity):
        if entity.tag == "slime":
            self.alive = False
