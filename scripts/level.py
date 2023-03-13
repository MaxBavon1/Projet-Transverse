from .image import *
import pygame
import csv

class Level:

    def __init__(self):
        self.tilemap = list(csv.reader(open("data/test map.csv")))
        self.tileset = game_sprites["tileset"]

    def collide(self, entity):
        tileX = entity.position.x // UNIT_SIZE
        tileY = entity.position.y // UNIT_SIZE
        tiles = [
            pygame.Rect(tileX * UNIT_SIZE, tileY * UNIT_SIZE, UNIT_SIZE, UNIT_SIZE),
            pygame.Rect((tileX+1) * UNIT_SIZE, tileY * UNIT_SIZE, UNIT_SIZE, UNIT_SIZE),
            pygame.Rect(tileX * UNIT_SIZE, (tileY+1) * UNIT_SIZE, UNIT_SIZE, UNIT_SIZE),
            pygame.Rect((tileX+1) * UNIT_SIZE, (tileY+1) * UNIT_SIZE, UNIT_SIZE, UNIT_SIZE)]
        return entity.rect.collideobjectsall(tiles)

    def render(self, surface):
        for y in range(len(self.tilemap)):
            for x in range(len(self.tilemap[0])):
                ID = int(self.tilemap[y][x])
                if ID != -1:
                    tile = game_sprites["tileset"][ID]
                    surface.blit(tile, (x * UNIT_SIZE, y * UNIT_SIZE))
