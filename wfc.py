import sys
import random as rand
from enum import Enum

from tile import Tile, TileRuleSet

class WaveFunctionCollapse:
    class WFCIterationResult(Enum):
        COMPLETE = 0,
        CONTRADICTION = 1,
        GENERATING = 2
    
    def __init__(self, startingTiles: list[Tile], rules: dict[Tile, TileRuleSet], gridSize: int) -> None:
        self.possibleTiles: list[Tile] = startingTiles
        self.gridSize: int = gridSize
        self.ruleSet: dict[Tile, TileRuleSet] = rules

        self.grid: list[list[Tile | None]] = []
        self.entropies: list[list[int]] = []
        self.options: list[list[list[Tile]]] = []
        for r in range (gridSize):
            self.grid.append([])
            self.entropies.append([])
            self.options.append([])

            for c in range(gridSize):
                self.grid[r].append(None)

                self.entropies[r].append(len(startingTiles))

                self.options[r].append([])
                self.options[r][c] = startingTiles.copy()

    def wfc(self) -> WFCIterationResult:
        minEntropy: int = sys.maxsize
        for r in range(self.gridSize):
            for c in range(self.gridSize):
                entropy: int = self.entropies[r][c]
                if (entropy == 0):
                    continue

                if (entropy < minEntropy):
                    minEntropy = entropy

        if (minEntropy == sys.maxsize):
            return self.WFCIterationResult.COMPLETE

        minEntropyTileIndexes: list[tuple[int, int]] = []
        for r in range(self.gridSize):
            for c in range(self.gridSize):
                if (self.entropies[r][c] == minEntropy):
                    minEntropyTileIndexes.append((r, c))

        chosen: tuple[int, int] = rand.choice(minEntropyTileIndexes)
        if (not self._collapse(chosen[0], chosen[1])):
            return self.WFCIterationResult.CONTRADICTION

        return self.WFCIterationResult.GENERATING

    def _collapse(self, ROW: int, COL: int) -> bool:
        self.grid[ROW][COL] = rand.choice(self.options[ROW][COL])
        self.options[ROW][COL] = []
        self.entropies[ROW][COL] = 0

        # handle up
        if (ROW != 0):
            newOptions: list[Tile] = []
            for option in self.options[ROW - 1][COL]:
                if (option in self.ruleSet[self.grid[ROW][COL]].getUp() and option in self.options[ROW - 1][COL]): # type: ignore
                    newOptions.append(option)

            newEntropy: int = len(newOptions)
            if (newEntropy == 0 and len(self.options[ROW - 1][COL]) != 0):
                return False

            self.options[ROW - 1][COL] = newOptions
            self.entropies[ROW - 1][COL] = newEntropy

        # handle right
        if (COL != self.gridSize - 1):
            newOptions: list[Tile] = []
            for option in self.options[ROW][COL + 1]:
                if (option in self.ruleSet[self.grid[ROW][COL]].getRight() and option in self.options[ROW][COL + 1]): # type: ignore
                    newOptions.append(option)

            newEntropy: int = len(newOptions)
            if (newEntropy == 0 and len(self.options[ROW][COL + 1]) != 0):
                return False

            self.options[ROW][COL + 1] = newOptions
            self.entropies[ROW][COL + 1] = newEntropy
            
        # handle down
        if (ROW != self.gridSize - 1):
            newOptions: list[Tile] = []
            for option in self.options[ROW + 1][COL]:
                if (option in self.ruleSet[self.grid[ROW][COL]].getDown() and option in self.options[ROW + 1][COL]): # type: ignore
                    newOptions.append(option)

            newEntropy: int = len(newOptions)
            if (newEntropy == 0 and len(self.options[ROW + 1][COL]) != 0):
                return False

            self.options[ROW + 1][COL] = newOptions
            self.entropies[ROW + 1][COL] = newEntropy
        
        # handle left
        if (COL != 0):
            newOptions: list[Tile] = []
            for option in self.options[ROW][COL - 1]:
                if (option in self.ruleSet[self.grid[ROW][COL]].getLeft() and option in self.options[ROW][COL - 1]): # type: ignore
                    newOptions.append(option)

            newEntropy: int = len(newOptions)
            if (newEntropy == 0 and len(self.options[ROW][COL - 1]) != 0):
                return False

            self.options[ROW][COL - 1] = newOptions
            self.entropies[ROW][COL - 1] = newEntropy

        return True
    
    @staticmethod
    def _twoDimToOneDim(row: int, col: int, gridSize: int):
        return row * gridSize + col