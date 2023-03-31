import pygame
import os

__all__ = ["game_sprites", "load_image", "load_game_sprites2", "TILE_SIZE"]

PATH = os.getcwd()
PIXEL_RATIO = 2
PIXEL_UNIT = 16
TILE_SIZE = PIXEL_RATIO * PIXEL_UNIT
game_sprites = {}

def load_image(path, size=PIXEL_RATIO, alpha=True):
    surf = pygame.image.load(path)
    surf = pygame.transform.scale(surf, (surf.get_width() * size, surf.get_height() * size))
    surf = surf.convert_alpha() if alpha else surf.convert()
    return surf

def load_animation(path, frames=1, size=PIXEL_RATIO, alpha=True):
    sheet = load_image(path, size, alpha)
    sprite_size = sheet.get_width() // frames
    # print(sprite_size, sheet.get_width())
    animation = []
    for x in range(frames):
        animation.append(sheet.subsurface((x * sprite_size, 0, sprite_size, sheet.get_height())))
    return animation


def load_tileset(path, pxunit=PIXEL_UNIT):
    pxunit *= PIXEL_RATIO
    tiles = load_image(path)
    width = tiles.get_width()
    height = tiles.get_height()
    tileset = []
    for y in range(0, height, pxunit):
        for x in range(0, width, pxunit):
            tileset.append(tiles.subsurface(x, y, pxunit, pxunit))
    return tileset

def load_game_sprites():
    global game_sprites

    game_sprites["player"] = load_image("assets/idle.png")
    game_sprites["bullet"] = load_image("assets/bulleta.png")
    game_sprites["slime"] = load_image("assets/slime2.png")
    game_sprites["tileset"] = load_tileset("assets/maps/tileset forest.png")
    game_sprites["cursor"] = load_image("assets/3crosshair.png")
    game_sprites["player_anim"] = load_animation("assets/Walk.png", 7)
    return game_sprites


def load_game_sprites2():
    global game_sprites
    path = "assets/images"
    for (root, dirs, files) in os.walk(path, topdown=True):
        for file_ in files:
            game_sprites[file_[:-4]] = load_image(root + '/' + file_)
    game_sprites["tileset"] = load_tileset("assets/maps/tileset forest.png")   
    game_sprites["cursor"] = load_image("assets/ui/3crosshair.png")
    game_sprites["player_anim"] = load_animation("assets/images/player/Walk.png", 7)
    return game_sprites
