import pygame
import os

__all__ = ["game_sprites", "load_image", "load_game_sprites"]

PATH = os.getcwd()
PIXEL_UNIT = 2
game_sprites = {}

def load_image(path, size=1, alpha=True):
    surf = pygame.image.load(path)
    surf = pygame.transform.scale(surf, (surf.get_width() * size, surf.get_height() * size))
    surf = surf.convert_alpha() if alpha else surf.convert()
    return surf

def load_game_sprites():
    global game_sprites
    game_sprites["player"] = load_image("assets/idle.png", PIXEL_UNIT)
    game_sprites["bullet"] = load_image("assets/bulletd.png", PIXEL_UNIT)
    game_sprites["slime"] = load_image("assets/slime2.png", PIXEL_UNIT)
    return game_sprites