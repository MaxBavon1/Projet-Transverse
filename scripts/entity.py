import pygame

class Entity:

    def __init__(self, pos, speed, sprite):
        self.position = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(0)
        self.speed = speed
        self.sprite = sprite

    def update(self, deltaTime):
        self.position += self.velocity * self.speed * deltaTime

    def render(self, surface):
        surface.blit(self.sprite, self.position)