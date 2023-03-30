import pygame
import math


class Entity(pygame.sprite.Sprite):

    entityManager = None

    def __init__(self, group, sprite, pos, speed=1, vel=0, health=1, damage=1, tag="Entity"):
        super().__init__(group) if group else super().__init__()
        self.sprite = sprite
        self.position = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(vel)
        self.rect = sprite.get_rect()
        self.rect.center = self.position
        self.speed = speed
        self.maxHealth = health
        self.health = self.maxHealth
        self.damage = damage
        self.grounded = False
        self.tag = tag
    
    @classmethod
    def init(cls, manager):
        Entity.entityManager = manager
    
    def horizontal_collision(self, level):
        # ---- Horizontal Collisions ----
        if self.rect.left < level.border.left: # Border Left
                self.rect.left = level.border.left
                self.position.x = self.rect.centerx
        if self.rect.right > level.border.right: # Border Right
                self.rect.right = level.border.right
                self.position.x = self.rect.centerx

        for tile in level.collide(self): # TileMap
            if self.velocity.x > 0:
                self.rect.right = tile.left
                self.position.x = self.rect.centerx
            if self.velocity.x < 0:
                self.rect.left = tile.right
                self.position.x = self.rect.centerx

    def vertical_collision(self, level):
        # ---- Vertical Collisions ----
        if self.rect.top < level.border.top: # Border Top
                self.rect.top = level.border.top
                self.position.y = self.rect.centery
                self.velocity.y = 0
        if self.rect.bottom > level.border.bottom: # Border Bottom
                self.rect.bottom = level.border.bottom
                self.position.y = self.rect.centery
                self.velocity.y = 0
                self.grounded = True

        for tile in level.collide(self): # TileMap
            if self.velocity.y > 0:
                self.rect.bottom = tile.top
                self.position.y = self.rect.centery
                self.velocity.y = 0
                self.grounded = True
            if self.velocity.y < 0:
                self.rect.top = tile.bottom
                self.position.y = self.rect.centery
                self.velocity.y = 0
    
    def health_update(self):
        if self.health <= 0:
            self.destroy()

    def update(self, deltaTime, gravityScale):
        self.health_update()

        level = self.entityManager.game.level
        self.position.x += self.velocity.x * deltaTime
        self.rect.centerx = self.position.x
        self.horizontal_collision(level)

        self.velocity.y += gravityScale * deltaTime
        self.position.y += self.velocity.y * deltaTime
        self.rect.centery = math.ceil(self.position.y)
        self.vertical_collision(level)

        if (self.grounded and self.velocity.y != 0):
            self.grounded = False

    def render(self, surface, offset, screen):
        if self.rect.colliderect(screen):
            surface.blit(self.sprite, pygame.Vector2(self.rect.topleft) - offset)
 
    def render_debug(self, surface, offset):
        # HitBox
        hitbox = pygame.Rect(self.rect.x - offset.x, self.rect.y - offset.y, self.rect.w, self.rect.h)
        if self.grounded: pygame.draw.rect(surface, (0,255,0), hitbox, 2)
        else: pygame.draw.rect(surface, (255,0,0), hitbox, 2)
        # Velocity
        movement = self.velocity * 0.2
        pygame.draw.aaline(surface, (0,0,255), self.position - offset, self.position + movement - offset, 2)
    
    def destroy(self):
        self.kill()
        self.on_death()

    def on_collision(self, entity):
        pass

    def on_death(self):
        pass