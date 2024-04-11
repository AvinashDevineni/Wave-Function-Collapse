import pygame
import abc

import utils

class Tile:
    def __init__(self, imgPath: str | None = None, surface: pygame.Surface | None = None) -> None:
        self._imgPath: str | None = None

        if (imgPath == None and surface == None):
            raise ValueError("Both imgPath and surface cannot be None. One must be provided.")
        
        if (imgPath != None and surface != None):
            raise ValueError("Both imgPath and surface cannot be provided. Only one must be provided.")
        
        if (imgPath != None):
            self._img: pygame.Surface = pygame.image.load(imgPath)
            self._imgPath = imgPath

        if (surface != None):
            self._img: pygame.Surface = surface

    def getImg(self) -> pygame.Surface:
        return self._img

    def __eq__(self, compare: object) -> bool:
        # __eq__ should only get called when hash codes are equal in dict, so it should be true
        return True 
    
    def __hash__(self) -> int:
        if (self._imgPath is not None):
            return self._imgPath.__hash__()
        
        else:
            return utils.getSurfaceHash(self._img)
    
    def __str__(self) -> str:
        if (self._imgPath is not None):
            return self._imgPath
        
        return "None"
    
    def __repr__(self) -> str:
        return self.__str__()

class ITilesProvider(abc.ABC):
    @abc.abstractmethod
    def provide() -> dict[Tile, float]:
        '''Returns a dictionary that represents a tiles' chance to spawn, a fliat from 0-1. The sum of values should approximately 1.'''
        ...

class InputTileReader(ITilesProvider):
    def __init__(self, sampleImgPath: str, regionSize: int, tileSetTileSize: int) -> None:
        self.sample: pygame.Surface = pygame.image.load(sampleImgPath)
        self.imgSize = self.sample.get_width()
        if (regionSize * tileSetTileSize > self.imgSize): # if region pixel width/height is greater than imgSize
            raise ValueError("regionSize and tileSetTileSize are too high for imgSize. " +
                             f"Variables are {regionSize}, {tileSetTileSize}, and {self.imgSize} respectively.")
        
        self.regionSize: int = regionSize
        self.tileSize: int = tileSetTileSize

    def provide(self) -> dict[Tile, float]:
        regionDisplacement: list[list[tuple[int, int]]] = []
        for r in range(self.regionSize):
            rowDisplacement: list[tuple[int, int]] = []
            for c in range(self.regionSize):
                rowDisplacement.append((c * self.tileSize, r * self.tileSize))
            regionDisplacement.append(rowDisplacement)

        regions: list[Tile] = []
        for regionTopRow in range(self.imgSize - (self.regionSize - 1)):
            for regionLeftCol in range(self.imgSize - (self.regionSize - 1)):
                regions.append(Tile(surface=self.sample.subsurface
                ((regionLeftCol, regionTopRow), (self.regionSize, self.regionSize))))
        
        regionsDict: dict[Tile, float] = {}
        numRegions: int = len(regions)
        for region in regions:
            regionsDict[region] = regionsDict.get(region, 0) + 1
        for region in regionsDict:
            regionsDict[region] = regionsDict[region] / numRegions
        
        return regionsDict

DEFAULT_TILES_PATH = './tiles/default/'
class DefaultTileFactory(ITilesProvider):
    #region Tile IDs
    BLANK_ID: int = 0
    UP_ID: int = 1
    RIGHT_ID: int = 2
    DOWN_ID: int = 3
    LEFT_ID: int = 4
    #endregion

    # for flyweight pattern
    _createdTiles: dict[int, Tile] = {}

    def provide(self) -> dict[Tile, float]:
        tiles: dict[Tile, float] = {}

        numTiles: int = 5
        tiles[DefaultTileFactory.createBlank()] = 1/numTiles
        tiles[DefaultTileFactory.createUp()] = 1/numTiles
        tiles[DefaultTileFactory.createRight()] = 1/numTiles
        tiles[DefaultTileFactory.createDown()] = 1/numTiles
        tiles[DefaultTileFactory.createLeft()] = 1/numTiles

        return tiles

    @staticmethod
    def createBlank() -> Tile:
        return DefaultTileFactory._createdTiles.get(DefaultTileFactory.BLANK_ID,
        Tile(f'{DEFAULT_TILES_PATH}blank.png'))
    
    @staticmethod
    def createUp() -> Tile:
        return DefaultTileFactory._createdTiles.get(DefaultTileFactory.UP_ID,
        Tile(f'{DEFAULT_TILES_PATH}up.png'))
    
    @staticmethod
    def createRight() -> Tile:
        return DefaultTileFactory._createdTiles.get(DefaultTileFactory.RIGHT_ID,
        Tile(f'{DEFAULT_TILES_PATH}right.png'))
    
    @staticmethod
    def createDown() -> Tile:
        return DefaultTileFactory._createdTiles.get(DefaultTileFactory.DOWN_ID,
        Tile(f'{DEFAULT_TILES_PATH}down.png'))
    
    @staticmethod
    def createLeft() -> Tile:
        return DefaultTileFactory._createdTiles.get(DefaultTileFactory.LEFT_ID,
        Tile(f'{DEFAULT_TILES_PATH}left.png'))
    
LANDSCAPE_TILES_PATH = './tiles/landscape/'
class LandscapeTileFactory(ITilesProvider):
    #region Tile IDs
    GRASS_1_ID: int = 0
    GRASS_2_ID: int = 1

    FLOWER_1_ID: int = 2
    FLOWER_2_ID: int = 3

    LIGHT_FOREST_1_ID: int = 4
    LIGHT_FOREST_2_ID: int = 5

    WATER_1_ID: int = 6
    WATER_2_ID: int = 7
    #endregion

    # for flyweight pattern
    _createdTiles: dict[int, Tile] = {}

    def provide(self) -> dict[Tile, float]:
        tiles: dict[Tile, float] = {}

        numTiles: int = 8
        tiles[LandscapeTileFactory.createGrass1()] = 1/numTiles
        tiles[LandscapeTileFactory.createGrass2()] = 1/numTiles
        tiles[LandscapeTileFactory.createFlower1()] = 1/numTiles
        tiles[LandscapeTileFactory.createFlower2()] = 1/numTiles
        tiles[LandscapeTileFactory.createLightForest1()] = 1/numTiles
        tiles[LandscapeTileFactory.createLightForest2()] = 1/numTiles
        tiles[LandscapeTileFactory.createWater1()] = 1/numTiles
        tiles[LandscapeTileFactory.createWater2()] = 1/numTiles

        return tiles

    @staticmethod
    def createGrass1() -> Tile:
        return LandscapeTileFactory._createdTiles.get(LandscapeTileFactory.GRASS_1_ID,
        Tile(f'{LANDSCAPE_TILES_PATH}grass1.png'))
    
    @staticmethod
    def createGrass2() -> Tile:
        return LandscapeTileFactory._createdTiles.get(LandscapeTileFactory.GRASS_2_ID,
        Tile(f'{LANDSCAPE_TILES_PATH}grass2.png'))
    
    @staticmethod
    def createFlower1() -> Tile:
        return LandscapeTileFactory._createdTiles.get(LandscapeTileFactory.FLOWER_1_ID,
        Tile(f'{LANDSCAPE_TILES_PATH}flower1.png'))
    
    @staticmethod
    def createFlower2() -> Tile:
        return LandscapeTileFactory._createdTiles.get(LandscapeTileFactory.FLOWER_2_ID,
        Tile(f'{LANDSCAPE_TILES_PATH}flower2.png'))
    
    @staticmethod
    def createLightForest1() -> Tile:
        return LandscapeTileFactory._createdTiles.get(LandscapeTileFactory.LIGHT_FOREST_1_ID,
        Tile(f'{LANDSCAPE_TILES_PATH}lightForest1.png'))
    
    @staticmethod
    def createLightForest2() -> Tile:
        return LandscapeTileFactory._createdTiles.get(LandscapeTileFactory.LIGHT_FOREST_2_ID,
        Tile(f'{LANDSCAPE_TILES_PATH}lightForest2.png'))
    
    @staticmethod
    def createWater1() -> Tile:
        return LandscapeTileFactory._createdTiles.get(LandscapeTileFactory.WATER_1_ID,
        Tile(f'{LANDSCAPE_TILES_PATH}water1.png'))
    
    @staticmethod
    def createWater2() -> Tile:
        return LandscapeTileFactory._createdTiles.get(LandscapeTileFactory.WATER_2_ID,
        Tile(f'{LANDSCAPE_TILES_PATH}water2.png'))