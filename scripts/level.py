from .image import *
import pygame
import csv


class Level:

    def __init__(self, game, lvl):
        self.game = game
        self.tiles = game.assets.tiles
        self.tilemap = list(csv.reader(open(f"data/levels/level{lvl}.csv")))
        if lvl == 1:
            self.tileset = self.tiles["forest"]
        elif lvl == 2:
            self.tileset = self.tiles["snow"]
        else:
            self.tileset = self.tiles["lava"]

        self.level_width = len(self.tilemap[0])
        self.level_height = len(self.tilemap)
        self.border = pygame.Rect(0, 0, game.WIDTH * 10, game.HEIGHT * 10)

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

    def render(self, surface, camera):
        offset, screen = camera.offset, camera.rect
        for y in range(len(self.tilemap)):
            for x in range(len(self.tilemap[0])):
                ID = int(self.tilemap[y][x])
                if ID != -1:
                    tile_pos = pygame.Vector2(x * TILE_SIZE, y * TILE_SIZE)
                    if screen.colliderect(pygame.Rect(tile_pos, (TILE_SIZE, TILE_SIZE))):
                        tile = self.tileset[ID]
                        surface.blit(tile, tile_pos - offset)

        if self.game.debugMode:
            self.render_debug(surface, offset)

    def render_debug(self, surface, offset):
        for y in range(len(self.tilemap)):
            for x in range(len(self.tilemap[0])):
                ID = int(self.tilemap[y][x])
                if ID > 10:
                    pygame.draw.rect(surface, (0,255,0), (x * TILE_SIZE - offset.x, y * TILE_SIZE - offset.y, TILE_SIZE, TILE_SIZE), 1)
        
        border = pygame.Rect(self.border.x - offset.x, self.border.y - offset.y, self.border.w, self.border.h)
        pygame.draw.rect(surface, (255,0,0), border, 2)