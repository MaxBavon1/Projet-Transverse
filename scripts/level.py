from .image import *
import pygame
import csv

class Level:

    def __init__(self):
        self.tilemap = list(csv.reader(open("data/test map.csv")))
        self.level_width = len(self.tilemap[0])
        self.level_height = len(self.tilemap)
        self.tileset = game_sprites["tileset"]

    def collide(self, entity):
        tileX = int(entity.rect.x // TILE_SIZE)
        tileY = int(entity.rect.y // TILE_SIZE)
        tiles = []
        for y in range(self.level_height):
            for x in range(self.level_width):
                if int(self.tilemap[y][x]) > 10:
                    tile = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if entity.rect.colliderect(tile):
                        tiles.append(tile)
        # if (tileX >= 0 and tileX+1 < self.level_width) and (tileY >= 0 and tileY+1 < self.level_height):
        #     if int(self.tilemap[tileY][tileX]) > 10: tiles.append(pygame.Rect(tileX * TILE_SIZE, tileY * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        #     if int(self.tilemap[tileY][tileX+1]) > 10: tiles.append(pygame.Rect((tileX+1) * TILE_SIZE, tileY * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        #     if int(self.tilemap[tileY+1][tileX]) > 10: tiles.append(pygame.Rect(tileX * TILE_SIZE, (tileY+1) * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        #     if int(self.tilemap[tileY+1][tileX+1]) > 10: tiles.append(pygame.Rect((tileX+1) * TILE_SIZE, (tileY+1) * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        #     return entity.rect.collideobjectsall(tiles)
        # else:
        #     return []
        return tiles

    def render(self, surface):
        for y in range(len(self.tilemap)):
            for x in range(len(self.tilemap[0])):
                ID = int(self.tilemap[y][x])
                if ID != -1:
                    tile = game_sprites["tileset"][ID]
                    surface.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))
