class Bullet:

    def __init__(self, posx, posy):
        self.x = posx
        self.y = posy
        self.speed = 30
    
    def update(self, dt):
        self.x += self.speed * dt

    def render(self, window, sprite):
	    window.blit(sprite, (self.x, self.y))