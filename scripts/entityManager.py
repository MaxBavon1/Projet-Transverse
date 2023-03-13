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
        return self.entityManager.types[self.entityType](self, game_sprites[self.entityType], *args, tag=self.entityType, **kwargs)

    def render(self, surface):
        for entiy in self:
            entiy.render(surface)
            if self.game.debugMode:
                entiy.render_debug(surface)


class EntityManager2:

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.types = {
            "player" : Player,
            "bullet": Bullet,
            "slime" : Slime}
        load_game_sprites()
        self.player = Player(None, game_sprites["player"], (512, 0), 200, tag="player")
        self.ennemies = EntityGroup(self, "slime")
        self.bullets = EntityGroup(self, "bullet")

    def update(self, deltaTime, gravityScale):
        self.player.update(deltaTime, gravityScale)
        self.ennemies.update(deltaTime, gravityScale)
        self.bullets.update(deltaTime, gravityScale)
        # ---- Collisions ----
        # for i in range(self.size-1):
        #     for j in range(i+1, self.size):
        #         if self.entities[i].collide(self.entities[j]):
        #             self.entities[i].on_collision(self.entities[j])
        #             self.entities[j].on_collision(self.entities[i])
        # # ---- Physics ----
        # for entity in self.entities:
        #     if entity.alive and entity.health > 0:
        #         if entity.tag == "bullet":
        #             entity.update(deltaTime, gravityScale/5)
        #             if entity.collide_rect(self.game.ground):
        #                 if abs(entity.velocity.y) > 0.1:
        #                     entity.velocity.y *= -0.8
        #                     entity.position.y = self.game.ground.y - entity.sprite.get_height() / 2
        #                 else:
        #                     entity.velocity.y = 0
        #                     entity.position.y = self.game.ground.y - entity.sprite.get_height() / 2 + 1
        #                     entity.grounded = True
        #             else:
        #                 entity.grounded = False
        #         else:
        #             entity.update(deltaTime, gravityScale)
        #             if entity.collide_rect(self.game.ground):
        #                 entity.velocity.y = 0
        #                 entity.position.y = self.game.ground.y - entity.sprite.get_height() / 2 + 1
        #                 entity.grounded = True
        #             else:
        #                 entity.grounded = False
        #     else:
        #         self.kill(entity)
    
    def render(self, surface):
        self.player.render(surface)
        self.ennemies.render(surface)
        self.bullets.render(surface)


class EntityManager:

    def __init__(self, game):
        self.game = game
        self.entities = []
        self.size = 0
        self.types = {
            "player" : Player,
            "bullet": Bullet,
            "slime" : Slime}
        Entity.init(self)
    
    def init(self):
        load_game_sprites()
        self.add(Player((512, 0), 200, game_sprites["player"], tag="player"))
        self.player = self.get("player")
        self.spawn("slime", self.player, (512, 256), 40)
        self.spawn("slime", self.player, (400, 256), 40, health=5)
        self.spawn("slime", self.player, (100, 256), 40, health=15)

    def add(self, entity):
        self.entities.append(entity)
        self.size += 1
    
    def kill(self, entity):
        if entity in self.entities:
            entity.on_death()
            self.entities.remove(entity)
            self.size -= 1
    
    def spawn(self, type_, *args, **kwargs):
        entity = self.types[type_](*args, game_sprites[type_], tag=type_, **kwargs)
        self.add(entity)

    def get(self, tag):
        for entity in self.entities:
            if entity.tag == tag:
                return entity
    
    def update(self, deltaTime, gravityScale):
        # ---- Collisions ----
        for i in range(self.size-1):
            for j in range(i+1, self.size):
                if self.entities[i].collide(self.entities[j]):
                    self.entities[i].on_collision(self.entities[j])
                    self.entities[j].on_collision(self.entities[i])
        # ---- Physics ----
        for entity in self.entities:
            if entity.alive and entity.health > 0:
                if entity.tag == "bullet":
                    entity.update(deltaTime, gravityScale/5)
                    if entity.collide_rect(self.game.ground):
                        if abs(entity.velocity.y) > 0.1:
                            entity.velocity.y *= -0.8
                            entity.position.y = self.game.ground.y - entity.sprite.get_height() / 2
                        else:
                            entity.velocity.y = 0
                            entity.position.y = self.game.ground.y - entity.sprite.get_height() / 2 + 1
                            entity.grounded = True
                    else:
                        entity.grounded = False  
                else:
                    entity.update(deltaTime, gravityScale)
                    if entity.collide_rect(self.game.ground):
                        entity.velocity.y = 0
                        entity.position.y = self.game.ground.y - entity.sprite.get_height() / 2 + 1
                        entity.grounded = True
                    else:
                        entity.grounded = False
            else:
                self.kill(entity)
    
    def render(self, surface):
        for entiy in self.entities:
            entiy.render(surface)
            if self.game.debugMode:
                entiy.render_debug(surface)