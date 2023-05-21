from .assets import *
import pygame
import csv
import os

class Level:

    levels = {1 : "forest", 2 : "snow", 3 : "lava"}

    def __init__(self, game, lvl):
        self.game = game
        self.tiles = game.assets.tiles
        self.tilemap = []
        self.layers = {}
        self.tilesets = {}

        self.name = self.levels[lvl]
        self.width = 0
        self.height = 0
        self.load_level(lvl)

        self.border = pygame.Rect(0, 0, game.WIDTH * 10, game.HEIGHT * 10)

    def load_tilemaps(self, lvl):
        path = f"data/level{lvl}/"
        for tilemap in os.listdir(path):
            name = tilemap.replace(".csv", "")
            if name == "collisions":
                self.tilemap = list(csv.reader(open(path + tilemap)))
            else:
                self.layers[name] = list(csv.reader(open(path + tilemap)))

    def load_tilesets(self):
        self.tilesets["collisions"] = self.tiles[self.name]
        for name in self.layers:
            self.tilesets[name] = self.tiles[name]

    def load_level(self, lvl):
        self.load_tilemaps(lvl)
        self.load_tilesets()

        self.width = len(self.tilemap[0])
        self.height = len(self.tilemap)

    def collide(self, entity, range_=2):
        tileX = int(entity.hitbox.x // TILE_SIZE)
        tileY = int(entity.hitbox.y // TILE_SIZE)
        tiles = []
        detection_range = range_
        for y in range(tileY - detection_range, tileY + detection_range + 1):
            for x in range(tileX - detection_range, tileX + detection_range + 1):
                if (x >= 0 and x < self.width) and (y >= 0 and y < self.height):
                    if int(self.tilemap[y][x]) > 10:
                        tile = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if entity.hitbox.colliderect(tile):
                            tiles.append(tile)
        return tiles

    def render_old(self, surface, camera):
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
    
    def render_tilemap(self, surface, camera, tilemap, tileset):
        offset, screen = camera.offset, camera.rect
        for y in range(self.height):
            for x in range(self.width):
                ID = int(tilemap[y][x])
                if ID != -1:
                    tile_pos = pygame.Vector2(x * TILE_SIZE, y * TILE_SIZE)
                    if screen.colliderect(pygame.Rect(tile_pos, (TILE_SIZE, TILE_SIZE))):
                        tile = tileset[ID]
                        surface.blit(tile, tile_pos - offset)
    
    def render_debug(self, surface, offset):
        for y in range(self.height):
            for x in range(self.width):
                ID = int(self.tilemap[y][x])
                if ID > 10:
                    pygame.draw.rect(surface, (0,255,0), (x * TILE_SIZE - offset.x, y * TILE_SIZE - offset.y, TILE_SIZE, TILE_SIZE), 1)
        
        border = pygame.Rect(self.border.x - offset.x, self.border.y - offset.y, self.border.w, self.border.h)
        pygame.draw.rect(surface, (255,0,0), border, 2)

    def render(self, surface, camera):
        """ Render all level layers and main collision tilemap in order (to create depth) """
        self.render_tilemap(surface, camera, self.layers["traps"], self.tilesets["traps"])
        self.render_tilemap(surface, camera, self.layers["objects"], self.tilesets["objects"])
        self.render_tilemap(surface, camera, self.tilemap, self.tilesets["collisions"])

        if self.game.debugMode:
            self.render_debug(surface, camera.offset)