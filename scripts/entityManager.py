from .image import *
from .entity import *
from .player import *
from .bullet import *
from .slime import *


class EntityGroup(pygame.sprite.Group):

    def __init__(self, entityManager, entityType, *entites):
        super().__init__(*entites)
        self.entityManager = entityManager
        self.entityType = entityType

    def spawn(self, *args, **kwargs):
        entity = self.entityManager.types[self.entityType](self, game_sprites[self.entityType], *args, **kwargs, tag=self.entityType)
        self.add(entity)

    def render(self, surface, camera):
        for entiy in self:
            entiy.render(surface, camera.offset, camera.rect)
            if self.entityManager.game.debugMode:
                entiy.render_debug(surface, camera.offset)


class EntityManager:

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.types = {
            "player" : Player,
            "bullet": Bullet,
            "slime" : Slime}
        load_game_sprites()
        Entity.init(self)
        self.player = Player(None, game_sprites["player"], (750, 400), 0, tag="player")
        self.ennemies = EntityGroup(self, "slime")
        self.bullets = EntityGroup(self, "bullet")
        self.ennemies.spawn((600, 400), self.player, speed=75, health=3)
        self.ennemies.spawn((1100, 500), self.player, speed=75, health=5)
        self.ennemies.spawn((200, 500), self.player, speed=75, health=1)
        self.ennemies.spawn((900, 900), self.player, speed=75, health=10)
        self.ennemies.spawn((400, 20), self.player, speed=75, health=20)
        self.ennemies.spawn((200, 0), self.player, speed=75, health=50)

    @property
    def size(self):
        return 1 + len(self.ennemies) + len(self.bullets)

    def update(self, deltaTime, gravityScale):
        self.bullets.update(deltaTime, gravityScale)
        self.ennemies.update(deltaTime, gravityScale)
        self.player.update(deltaTime, gravityScale)

        self.handle_collisions()

    def render(self, surface, camera):
        self.player.render(surface, camera)
        if self.game.debugMode:
            self.player.render_debug(surface, camera.offset)
        self.ennemies.render(surface, camera)
        self.bullets.render(surface, camera)
    
    def handle_collisions(self):
        for bullet, slimes in pygame.sprite.groupcollide(self.bullets, self.ennemies, False, False).items():
            bullet.destroy()
            for slime in slimes:
                slime.health -= bullet.damage

        self.player.health -= len(pygame.sprite.spritecollide(self.player, self.ennemies, False))
