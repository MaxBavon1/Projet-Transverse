import pygame

class Entity2(pygame.sprite.Sprite):

    def __init__(self, group, sprite, pos, speed, health=1, tag="Entity"):
        super().__init__(group) if group else super().__init__()
        self.sprite = sprite
        self.position = pygame.Vector2(pos)
        self.velocity = pygame.Vector2()
        self.rect = sprite.get_rect()
        self.rect.center = pos
        self.speed = speed
        self.maxHealth = health
        self.health = self.maxHealth
        self.grounded = False
        self.tag = tag
    
    @classmethod
    def init(self, entityManager):
        Entity2.entityManager = entityManager

    def update(self, deltaTime, gravityScale):
        if not self.grounded:
            self.velocity.y += gravityScale * deltaTime

        self.position += self.velocity * self.speed * deltaTime
        self.rect.center = self.position

    def render(self, surface):
        if self.rect.colliderect(surface.get_rect()):
            surface.blit(self.sprite, self.rect.topleft)
    
    def render_debug(self, surface):
        # HitBox
        pygame.draw.rect(surface, (255,0,0), self.get_rect(), 2)
        # Velocity
        movement = self.velocity * 50
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
        pygame.draw.rect(surface, (255,0,0), self.get_rect(), 2)
        # Velocity
        movement = self.velocity * 50
        pygame.draw.aaline(surface, (0,0,255), self.position, self.position + movement, 2)
    
    def on_collision(self, entity):
        pass

    def on_death(self):
        pass