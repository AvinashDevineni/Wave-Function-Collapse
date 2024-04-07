import pygame; pygame.init()
import sys

import tile
from wfc import WaveFunctionCollapse

GRID_SIZE: int = int(input("What size do you want the grid to be?\n"))
DELAY: float = int(input("What delay do you want when generating tiles (ms)?\n"))
TILE_SET: str = input("What tile set do you want to use (default OR landscape)?\n").strip().lower()

SCREEN_WIDTH: int = 600
SCREEN_HEIGHT: int = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wave Function Collapse')

TILE_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
TILE_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

#region Start
# drawRandTiles()
tileSet: list[tile.Tile] = []
tileRules: dict[tile.Tile, tile.TileRuleSet] = {}
if (TILE_SET == "default"):
    tileSet = tile.DefaultTileFactory.createAll()
    tileRules = tile.DefaultTileRuleSetFactory.createAll()

elif (TILE_SET == "landscape"):
    tileSet = tile.LandscapeTileFactory.createAll()
    tileRules = tile.LandscapeTileRuleSetFactory.createAll()

else:
    print("INVALID TILESET PROVIDED.")
    sys.exit()

algo = WaveFunctionCollapse(tileSet, tileRules, GRID_SIZE)
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
                algo = WaveFunctionCollapse(tileSet, tileRules, GRID_SIZE)
                
                isGenerationDone = False
                screen.fill((0, 0, 0))

    if (not algo.wfc() and not isGenerationDone):
        print("Done")
        isGenerationDone = True
    
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if (algo.grid[r][c] == None):
                continue

            screen.blit(pygame.transform.scale(algo.grid[r][c].getImg(), # type: ignore
            (TILE_WIDTH, TILE_HEIGHT)), (TILE_WIDTH * c, TILE_HEIGHT * r))
    pygame.display.flip()

    pygame.time.wait(DELAY)

pygame.quit()