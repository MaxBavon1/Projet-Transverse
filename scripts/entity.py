import pygame
import math

__all__ = ["StaticEntity", "Entity"]

class StaticEntity(pygame.sprite.Sprite):

    entityManager = None

    def __init__(self, group, sprite, pos, speed=1, vel=0, health=1, damage=1, tag="Entity"):
        super().__init__(group) if group else super().__init__()
        # Physics
        self.position = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(vel)
        self.rect = sprite.get_rect()
        self.rect.center = self.position
        self.speed = speed
        self.grounded = False
        # Attributes
        self.maxHealth = health
        self.health = self.maxHealth
        self.damage = damage
        self.tag = tag
        self.set_sprite(sprite)

    @classmethod
    def init(cls, manager):
        cls.entityManager = manager
    
    def set_sprite(self, sprite):
        self.sprite = sprite
        middle, bottom = self.rect.centerx, self.rect.bottom
        self.rect.size = sprite.get_size()
        self.rect.centerx, self.rect.bottom = middle, bottom
        self.position.x, self.position.y = self.rect.center
        self.vertical_collision(self.entityManager.game.level)

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
        # Position
        pygame.draw.circle(surface, (0, 0, 0), self.position - offset, 2)
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


class Entity(StaticEntity):
     
    def __init__(self, group, animations, pos, speed=1, vel=0, health=1, damage=1, anim_speed=1, tag="StaticEntity"):
        self.animations = animations
        self.current_anim = list(animations.keys())[0]
        self.frame = 0
        self.anim_speed = anim_speed
        super().__init__(group, animations[self.current_anim][0], pos, speed, vel, health, damage, tag)

    def play(self, animation):
        if self.current_anim != animation:
            self.frame = 0
            self.current_anim = animation
            self.set_sprite(self.animations[self.current_anim][0])

    def animate(self):
        self.frame += 1
        self.frame %= len(self.animations[self.current_anim]) * self.anim_speed
        self.sprite = self.animations[self.current_anim][self.frame // self.anim_speed]

    def update(self, deltaTime, gravityScale):
        self.animate()
        super().update(deltaTime, gravityScale)