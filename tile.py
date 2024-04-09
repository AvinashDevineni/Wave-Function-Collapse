import pygame
import abc

class Tile:
    def __init__(self, imgPath: str) -> None:
        self._img: pygame.Surface = pygame.image.load(imgPath)
        self._imgPath = imgPath

    def getImg(self) -> pygame.Surface:
        return self._img

    def __eq__(self, compare: object) -> bool:
        if (type(compare) != Tile):
            return False
        
        return self._imgPath == compare._imgPath
    
    def __hash__(self) -> int:
        return self._imgPath.__hash__()
    
    def __str__(self) -> str:
        return self._imgPath
    
    def __repr__(self) -> str:
        return self.__str__()

class ITilesProvider(abc.ABC):
    @abc.abstractmethod
    def provide() -> list[Tile]:
        ...

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

    def provide(self) -> list[Tile]:
        tiles: list[Tile] = []

        tiles.append(DefaultTileFactory.createBlank())
        tiles.append(DefaultTileFactory.createUp())
        tiles.append(DefaultTileFactory.createRight())
        tiles.append(DefaultTileFactory.createDown())
        tiles.append(DefaultTileFactory.createLeft())

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

    def provide(self) -> list[Tile]:
        tiles: list[Tile] = []

        tiles.append(LandscapeTileFactory.createGrass1())
        tiles.append(LandscapeTileFactory.createGrass2())
        tiles.append(LandscapeTileFactory.createFlower1())
        tiles.append(LandscapeTileFactory.createFlower2())
        tiles.append(LandscapeTileFactory.createLightForest1())
        tiles.append(LandscapeTileFactory.createLightForest2())
        tiles.append(LandscapeTileFactory.createWater1())
        tiles.append(LandscapeTileFactory.createWater2())

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