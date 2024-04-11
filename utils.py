import pygame
from enum import Enum

def getColorHash(color: pygame.Color) -> int:
    return color.r * 31 * (color.g * 17 + 11) * color.b * 13

def getSurfaceHash(surf: pygame.Surface) -> int:
    hash: int = 0
    for r in range(surf.get_height()):
        for c in range(surf.get_width()):
            hash += getColorHash(surf.get_at((r, c))) * (47 + r) * (53 + c)
    
    return hash

class Direction(Enum):
    UP = 0,
    RIGHT = 1,
    DOWN = 2,
    LEFT = 3

def mergeSurfaces(surf1: pygame.Surface, surf2: pygame.Surface, surf2MergeDir: Direction) -> pygame.Surface:
    mergedSurface: pygame.Surface
    if surf2MergeDir == Direction.UP:
        mergedSurface = pygame.Surface((surf1.get_width(), surf1.get_height() + surf2.get_height()))
        mergedSurface.blit(surf1, (0, 0))
        mergedSurface.blit(surf2, (0, surf1.get_height()))

    elif surf2MergeDir == Direction.DOWN:
        mergedSurface = pygame.Surface((surf1.get_width(), surf1.get_height() + surf2.get_height()))
        mergedSurface.blit(surf1, (0, surf2.get_height()))
        mergedSurface.blit(surf2, (0, 0))

    elif surf2MergeDir == Direction.RIGHT:
        mergedSurface = pygame.Surface((surf1.get_width() + surf2.get_width(), surf1.get_height()))
        mergedSurface.blit(surf1, (surf2.get_width(), 0))
        mergedSurface.blit(surf2, (0, 0))

    else:
        mergedSurface = pygame.Surface((surf1.get_width() + surf2.get_width(), surf1.get_height()))
        mergedSurface.blit(surf1, (0, 0))
        mergedSurface.blit(surf2, (surf1.get_width(), 0))

    return mergedSurface