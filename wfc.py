import sys
import random as rand
from enum import Enum

from tile import Tile, ITilesProvider
from rules import TileRuleSet, IRulesProvider
from utils import Direction

class WaveFunctionCollapse:
    class WFCIterationResult(Enum):
        COMPLETE = 0,
        CONTRADICTION = 1,
        GENERATING = 2
    
    def __init__(self, tilesProvider: ITilesProvider, rulesProvider: IRulesProvider,
    gridSize: int, seed: int | None = None, areTilesWeighted: bool = False) -> None:
        self.areTilesWeighted = areTilesWeighted
        self.possibleTiles: dict[Tile, float] = tilesProvider.provide()
        self.gridSize: int = gridSize
        self.ruleSet: dict[Tile, TileRuleSet] = rulesProvider.provide()

        self.grid: list[list[Tile | None]] = []
        self.entropies: list[list[int]] = []
        self.options: list[list[dict[Tile, float]]] = []
        for r in range (gridSize):
            self.grid.append([])
            self.entropies.append([])
            self.options.append([])

            for c in range(gridSize):
                self.grid[r].append(None)
                self.entropies[r].append(len(self.possibleTiles))
                self.options[r].append(self.possibleTiles.copy())

        self.rand = rand.Random(seed)

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

        chosen: tuple[int, int] = self.rand.choice(minEntropyTileIndexes)
        if (not self._collapse(chosen[0], chosen[1])):
            return self.WFCIterationResult.CONTRADICTION

        return self.WFCIterationResult.GENERATING

    def _collapse(self, ROW: int, COL: int) -> bool:
        selfOptions: dict[Tile, float] = self.options[ROW][COL]
        if (self.areTilesWeighted):
            randVal: float = rand.random()
            chanceSum: float = 0
            for option in selfOptions:
                chanceSum += selfOptions[option]
                if (randVal < chanceSum):
                    self.grid[ROW][COL] = option
                    break


        else:
            tileOptions: list[Tile] = []
            for option in selfOptions:
                tileOptions.append(option)
            
            self.grid[ROW][COL] = self.rand.choice(tileOptions)
        
        self.options[ROW][COL] = {}
        self.entropies[ROW][COL] = 0

        for dir in Direction:
            deltaRow: int = 0
            deltaCol: int = 0
            possibleTileSet: set[Tile]
            if (dir == Direction.RIGHT):
                deltaCol = 1
                possibleTileSet = self.ruleSet[self.grid[ROW][COL]].getRight() # type: ignore

            elif (dir == Direction.LEFT):
                deltaCol = -1
                possibleTileSet = self.ruleSet[self.grid[ROW][COL]].getLeft() # type: ignore

            elif (dir == Direction.UP):
                deltaRow = -1
                possibleTileSet = self.ruleSet[self.grid[ROW][COL]].getUp() # type: ignore

            else:
                deltaRow = 1
                possibleTileSet = self.ruleSet[self.grid[ROW][COL]].getDown() # type: ignore
            
            if (ROW + deltaRow == -1 or ROW + deltaRow == self.gridSize):
                continue

            if (COL + deltaCol == -1 or COL + deltaCol == self.gridSize):
                continue

            newOptions: dict[Tile, float] = {}
            chanceSum: float = 0
            for option in self.options[ROW + deltaRow][COL + deltaCol]:
                if (option in possibleTileSet):
                    chance: float = self.options[ROW + deltaRow][COL + deltaCol][option]
                    newOptions[option] = chance
                    chanceSum += chance

            newEntropy: int = len(newOptions)
            if (newEntropy == 0 and len(self.options[ROW + deltaRow][COL + deltaCol]) != 0):
                return False
            
            if (self.areTilesWeighted):
                chanceMultiplier: float = 1 / chanceSum
                for option in newOptions:
                    newOptions[option] = newOptions[option] * chanceMultiplier

            self.options[ROW + deltaRow][COL + deltaCol] = newOptions
            self.entropies[ROW + deltaRow][COL + deltaCol] = newEntropy

        return True
    
    @staticmethod
    def _twoDimToOneDim(row: int, col: int, gridSize: int):
        return row * gridSize + col