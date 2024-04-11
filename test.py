import pygame
pygame.init()

import tile

provider = tile.InputTileReader('./tiles/landscape/flower1.png', 2, 1)
regionsDict = provider.provide()

print(regionsDict)

regionsList: list[tile.Tile] = []
for region in regionsDict:
    regionsList.append(region)

screen = pygame.display.set_mode((600, 600))

running = True
index = 0
while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

        if (event.type == pygame.MOUSEBUTTONDOWN):
            index += 1
            print(f"Index now {index}")

    screen.blit(pygame.transform.scale(regionsList[index].getImg(), (600, 600)), (0, 0))
    pygame.display.flip()

pygame.quit()