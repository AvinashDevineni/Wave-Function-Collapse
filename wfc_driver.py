import pygame; pygame.init()
import sys
import time

import tile
import rules
from wfc import WaveFunctionCollapse

GRID_SIZE: int = int(input("What size do you want the grid to be?\n"))
DELAY: float = int(float(input("What delay do you want when generating tiles (ms)?\n")))
TILE_SET: str = input("What tile set do you want to use (default OR landscape)?\n").strip().lower()

SCREEN_WIDTH: int = 600
SCREEN_HEIGHT: int = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wave Function Collapse')

TILE_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
TILE_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

#region Start
# drawRandTiles()
tilesProvider: tile.ITilesProvider
rulesProvider: rules.IRulesProvider
if (TILE_SET == "default"):
    tilesProvider = tile.DefaultTileFactory()
    rulesProvider = rules.DefaultTileRuleSetFactory()

elif (TILE_SET == "landscape"):
    tilesProvider = tile.LandscapeTileFactory()
    rulesProvider = rules.LandscapeTileRuleSetFactory()

else:
    print("INVALID TILESET PROVIDED.")
    sys.exit()

algo = WaveFunctionCollapse(tilesProvider, rulesProvider, GRID_SIZE)
#endregion

print("Generating...")

isGenerationDone: bool = False
genStartTime: float = time.time()

running: bool = True
while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

        if (event.type == pygame.MOUSEBUTTONDOWN):
            if (isGenerationDone):
                print("Regenerating...")
                algo = WaveFunctionCollapse(tilesProvider, rulesProvider, GRID_SIZE)
                
                isGenerationDone = False
                genStartTime = time.time()
                screen.fill((0, 0, 0))

    result: WaveFunctionCollapse.WFCIterationResult = algo.wfc()
    if (result == WaveFunctionCollapse.WFCIterationResult.COMPLETE):
        if (not isGenerationDone):
            print(f"Done. Generation (and displaying) took {time.time() - genStartTime} seconds.")
            isGenerationDone = True

    elif (result == WaveFunctionCollapse.WFCIterationResult.CONTRADICTION):
        print("CONTRADICTION! Restarting WFC.")
        algo = WaveFunctionCollapse(tilesProvider, rulesProvider, GRID_SIZE)
        screen.fill((0, 0, 0))
    
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if (algo.grid[r][c] == None):
                continue

            screen.blit(pygame.transform.scale(algo.grid[r][c].getImg(), # type: ignore
            (TILE_WIDTH, TILE_HEIGHT)), (TILE_WIDTH * c, TILE_HEIGHT * r))
    pygame.display.flip()

    pygame.time.wait(DELAY)

pygame.quit()