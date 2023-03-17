from .image import *
import pygame
import csv

class Level:

    def __init__(self, game):
        self.game = game
        self.tilemap = list(csv.reader(open("data/test map.csv")))
        self.level_width = len(self.tilemap[0])
        self.level_height = len(self.tilemap)
        self.tileset = game_sprites["tileset"]
        self.border = pygame.Rect(0, 0, game.WIDTH, game.HEIGHT)

    def collide(self, entity, range_=2):
        tileX = int(entity.rect.x // TILE_SIZE)
        tileY = int(entity.rect.y // TILE_SIZE)
        tiles = []
        detection_range = range_
        for y in range(tileY - detection_range, tileY + detection_range + 1):
            for x in range(tileX - detection_range, tileX + detection_range + 1):
                if (x >= 0 and x < self.level_width) and (y >= 0 and y < self.level_height):
                    if int(self.tilemap[y][x]) > 10:
                        tile = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if entity.rect.colliderect(tile):
                            tiles.append(tile)
        return tiles

    def render(self, surface):
        for y in range(len(self.tilemap)):
            for x in range(len(self.tilemap[0])):
                ID = int(self.tilemap[y][x])
                if ID != -1:
                    tile = game_sprites["tileset"][ID]
                    surface.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))

        if self.game.debugMode:
            self.render_debug(surface)

    def render_debug(self, surface):
        for y in range(len(self.tilemap)):
            for x in range(len(self.tilemap[0])):
                ID = int(self.tilemap[y][x])
                if ID > 10:
                    pygame.draw.rect(surface, (0,255,0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
        
        pygame.draw.rect(surface, (255,0,0), self.border, 2)