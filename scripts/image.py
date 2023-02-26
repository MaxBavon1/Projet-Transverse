import pygame
import os

__all__ = ["PATH", "load_image"]

PATH = os.getcwd()

def load_image(path, size=1, alpha=True):
    surf = pygame.image.load(path)
    surf = pygame.transform.scale(surf, (surf.get_width() * size, surf.get_height() * size))
    surf = surf.convert_alpha() if alpha else surf.convert()
    return surf