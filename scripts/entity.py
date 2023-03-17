import pygame
import math

class Entity2(pygame.sprite.Sprite):

    def __init__(self, group, sprite, pos, speed, health=1, tag="Entity"):
        super().__init__(group) if group else super().__init__()
        self.sprite = sprite
        self.position = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(0)
        self.rect = sprite.get_rect()
        self.rect.center = self.position
        self.speed = speed
        self.maxHealth = health
        self.health = self.maxHealth
        self.grounded = False
        self.tag = tag
    
    @classmethod
    def init(self, entityManager):
        Entity2.entityManager = entityManager

    def update(self, deltaTime, gravityScale):
        level = self.entityManager.game.level
        self.position.x += self.velocity.x * self.speed * deltaTime
        self.rect.centerx = self.position.x
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

        self.velocity.y += gravityScale
        self.position.y += self.velocity.y * deltaTime
        self.rect.centery = math.ceil(self.position.y)
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

        if (self.grounded and self.velocity.y != 0):
            self.grounded = False

    def render(self, surface):
        if self.rect.colliderect(surface.get_rect()):
            surface.blit(self.sprite, self.rect.topleft)
    
    def render_debug(self, surface):
        # HitBox
        if self.grounded: pygame.draw.rect(surface, (0,255,0), self.rect, 2)
        else: pygame.draw.rect(surface, (255,0,0), self.rect, 2)
        # Velocity
        movement = self.velocity * 0.2
        movement.x *= self.speed
        pygame.draw.aaline(surface, (0,0,255), self.position, self.position + movement, 2)
    
    def on_collision(self, entity):
        pass

    def on_death(self):
        pass




class Entity:

    manager = None

    def __init__(self, pos, speed, sprite, vel=(0,0), health=1, tag="Entity"):
        self.position = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(vel)
        self.speed = speed
        self.sprite = sprite
        self.alive = True
        self.maxHealth = health
        self.health = self.maxHealth
        self.grounded = False
        self.tag = tag
    
    @classmethod
    def init(cls, manager):
        cls.manager = manager

    def get_rect(self):
        rect = self.sprite.get_rect()
        rect.center = self.position
        return rect

    def collide_rect(self, other):
        return self.get_rect().colliderect(other)

    def collide(self, entity):
        return self.collide_rect(entity.get_rect())

    def update(self, deltaTime, gravityScale):
        if not self.grounded:
            self.velocity.y += gravityScale * deltaTime

        self.position += self.velocity * self.speed * deltaTime
        self.position.x = round(self.position.x, 2)
        self.position.y = round(self.position.y, 2)

    def render(self, surface):
        if self.get_rect().colliderect(surface.get_rect()):
            surface.blit(self.sprite, self.position - (pygame.Vector2(self.sprite.get_size())/2))
    
    def render_debug(self, surface):
        # HitBox
        if self.grounded: pygame.draw.rect(surface, (0,255,0), self.get_rect(), 2)
        else: pygame.draw.rect(surface, (255,0,0), self.get_rect(), 2)
        # Velocity
        movement = self.velocity * 50
        pygame.draw.aaline(surface, (0,0,255), self.position, self.position + movement, 2)
    
    def on_collision(self, entity):
        pass

    def on_death(self):
        pass