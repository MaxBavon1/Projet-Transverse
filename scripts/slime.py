from pygame import Rect

class Slime:

    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.speed = 3
        self.health = health
        self.alive = True
    
    def collide(self, rect, other):
        return Rect((self.x, self.y), rect.get_size()).colliderect(other)

    def update(self, dt):
        self.x -= self.speed * dt
        if self.health <= 0:
            self.alive = False

    def render(self, window, sprite):
	    window.blit(sprite, (self.x, self.y))