import pygame
pygame.init()

import tile
from wfc import WaveFunctionCollapse

GRID_SIZE = int(input("What size do you want the grid to be?\n"))

SCREEN_WIDTH: int = 600
SCREEN_HEIGHT: int = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wave Function Collapse')

TILE_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
TILE_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

#region Funcs
def drawRandTiles():
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            img = tile.TileFactory.createRandTile().img
            img = pygame.transform.scale(img, (TILE_WIDTH, TILE_HEIGHT))
            screen.blit(img, (r * TILE_WIDTH, c * TILE_HEIGHT))

    pygame.display.flip()
#endregion

#region Start
# drawRandTiles()
algo = WaveFunctionCollapse(tile.TileFactory.createAll(), tile.TileRuleSetFactory.createAll(), GRID_SIZE)
#endregion

print("Generating...")
running: bool = True
isGenerationDone: bool = False
while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

        if (event.type == pygame.MOUSEBUTTONDOWN):
            if (isGenerationDone):
                print("Regenerating...")
                algo = WaveFunctionCollapse(tile.TileFactory.createAll(),
                                                tile.TileRuleSetFactory.createAll(), GRID_SIZE)
                
                isGenerationDone = False
                screen.fill((0, 0, 0))

    if (not algo.wfc() and not isGenerationDone):
        print("Done")
        isGenerationDone = True
    
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if (algo.grid[r][c] == None):
                continue

            screen.blit(pygame.transform.scale(algo.grid[r][c].img, (TILE_WIDTH, TILE_HEIGHT)), # type: ignore
                        (TILE_WIDTH * c, TILE_HEIGHT * r))
    pygame.display.flip()

pygame.quit()