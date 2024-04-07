import pygame
from random import randint

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
  
class TileRuleSet:
    def __init__(self, up: set[Tile] = set(),
                 right: set[Tile] = set(), down: set[Tile] = set(), left: set[Tile] = set()) -> None:
        self._up: set[Tile] = up
        self._right: set[Tile] = right
        self._down: set[Tile] = down
        self._left: set[Tile] = left

    def getUp(self) -> set[Tile]:
        return self._up
    
    def getRight(self) -> set[Tile]:
        return self._right
    
    def getDown(self) -> set[Tile]:
        return self._down
    
    def getLeft(self) -> set[Tile]:
        return self._left
    
    def __str__(self) -> str:
        return f"(UP: {self._up}, RIGHT: {self._right}, DOWN: {self._down}, LEFT: {self._left})"
    
    def __repr__(self) -> str:
        return self.__str__()

DEFAULT_TILES_PATH = './tiles/default/'
class DefaultTileFactory:
    #region Tile IDs
    BLANK_ID: int = 0
    UP_ID: int = 1
    RIGHT_ID: int = 2
    DOWN_ID: int = 3
    LEFT_ID: int = 4
    #endregion

    # for flyweight pattern
    _createdTiles: dict[int, Tile] = {}

    @staticmethod
    def createAll() -> list[Tile]:
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

class DefaultTileRuleSetFactory:
    #region Tile Ruleset IDs
    BLANK_ID: int = 0
    UP_ID: int = 1
    RIGHT_ID: int = 2
    DOWN_ID: int = 3
    LEFT_ID: int = 4
    #endregion

    # for flyweight pattern
    _createdRuleSets: dict[int, TileRuleSet] = {}
    _allRuleSets: dict[Tile, TileRuleSet] | None = None

    @staticmethod
    def createAll() -> dict[Tile, TileRuleSet]:
        if (DefaultTileRuleSetFactory._allRuleSets != None):
            return DefaultTileRuleSetFactory._allRuleSets
        
        ruleSets: dict[Tile, TileRuleSet] = {}
        ruleSets[DefaultTileFactory.createBlank()] = DefaultTileRuleSetFactory.createBlank()
        ruleSets[DefaultTileFactory.createUp()] = DefaultTileRuleSetFactory.createUp()
        ruleSets[DefaultTileFactory.createRight()] = DefaultTileRuleSetFactory.createRight()
        ruleSets[DefaultTileFactory.createDown()] = DefaultTileRuleSetFactory.createDown()
        ruleSets[DefaultTileFactory.createLeft()] = DefaultTileRuleSetFactory.createLeft()

        DefaultTileRuleSetFactory._allRuleSets = ruleSets

        return ruleSets

    @staticmethod
    def createBlank() -> TileRuleSet:
        if (DefaultTileRuleSetFactory.BLANK_ID in DefaultTileRuleSetFactory._createdRuleSets):
            return DefaultTileRuleSetFactory._createdRuleSets[DefaultTileRuleSetFactory.BLANK_ID]
        
        up: set[Tile] = {DefaultTileFactory.createBlank(), DefaultTileFactory.createUp()}
        right: set[Tile] = {DefaultTileFactory.createBlank(), DefaultTileFactory.createRight()}
        down: set[Tile] = {DefaultTileFactory.createBlank(), DefaultTileFactory.createDown()}
        left: set[Tile] = {DefaultTileFactory.createBlank(), DefaultTileFactory.createLeft()}

        ruleSet = TileRuleSet(up, right, down, left)
        DefaultTileRuleSetFactory._createdRuleSets[DefaultTileRuleSetFactory.BLANK_ID] = ruleSet

        return ruleSet
    
    @staticmethod
    def createUp() -> TileRuleSet:
        if (DefaultTileRuleSetFactory.UP_ID in DefaultTileRuleSetFactory._createdRuleSets):
            return DefaultTileRuleSetFactory._createdRuleSets[DefaultTileRuleSetFactory.UP_ID]
        
        up: set[Tile] = {DefaultTileFactory.createDown(), DefaultTileFactory.createLeft(), DefaultTileFactory.createRight()}
        right: set[Tile] = {DefaultTileFactory.createDown(), DefaultTileFactory.createLeft(), DefaultTileFactory.createUp()}
        down: set[Tile] = {DefaultTileFactory.createBlank(), DefaultTileFactory.createDown()}
        left: set[Tile] = {DefaultTileFactory.createDown(), DefaultTileFactory.createRight(), DefaultTileFactory.createUp()}

        ruleSet = TileRuleSet(up, right, down, left)
        DefaultTileRuleSetFactory._createdRuleSets[DefaultTileRuleSetFactory.UP_ID] = ruleSet

        return ruleSet
    
    @staticmethod
    def createRight() -> TileRuleSet:
        if (DefaultTileRuleSetFactory.RIGHT_ID in DefaultTileRuleSetFactory._createdRuleSets):
            return DefaultTileRuleSetFactory._createdRuleSets[DefaultTileRuleSetFactory.RIGHT_ID]
        
        up: set[Tile] = {DefaultTileFactory.createDown(), DefaultTileFactory.createRight(), DefaultTileFactory.createLeft()}
        right: set[Tile] = {DefaultTileFactory.createLeft(), DefaultTileFactory.createUp(), DefaultTileFactory.createDown()}
        down: set[Tile] = {DefaultTileFactory.createUp(), DefaultTileFactory.createLeft(), DefaultTileFactory.createRight()}
        left: set[Tile] = {DefaultTileFactory.createBlank(), DefaultTileFactory.createLeft()}

        ruleSet = TileRuleSet(up, right, down, left)
        DefaultTileRuleSetFactory._createdRuleSets[DefaultTileRuleSetFactory.RIGHT_ID] = ruleSet

        return ruleSet
    
    @staticmethod
    def createDown() -> TileRuleSet:
        if (DefaultTileRuleSetFactory.DOWN_ID in DefaultTileRuleSetFactory._createdRuleSets):
            return DefaultTileRuleSetFactory._createdRuleSets[DefaultTileRuleSetFactory.DOWN_ID]
        
        up: set[Tile] = {DefaultTileFactory.createBlank(), DefaultTileFactory.createUp()}
        right: set[Tile] = {DefaultTileFactory.createLeft(), DefaultTileFactory.createUp(), DefaultTileFactory.createDown()}
        down: set[Tile] = {DefaultTileFactory.createUp(), DefaultTileFactory.createLeft(), DefaultTileFactory.createRight()}
        left: set[Tile] = {DefaultTileFactory.createRight(), DefaultTileFactory.createUp(), DefaultTileFactory.createDown()}

        ruleSet = TileRuleSet(up, right, down, left)
        DefaultTileRuleSetFactory._createdRuleSets[DefaultTileRuleSetFactory.DOWN_ID] = ruleSet

        return ruleSet
    
    @staticmethod
    def createLeft() -> TileRuleSet:
        if (DefaultTileRuleSetFactory.LEFT_ID in DefaultTileRuleSetFactory._createdRuleSets):
            return DefaultTileRuleSetFactory._createdRuleSets[DefaultTileRuleSetFactory.LEFT_ID]
        
        up: set[Tile] = {DefaultTileFactory.createDown(), DefaultTileFactory.createLeft(), DefaultTileFactory.createRight()}
        right: set[Tile] = {DefaultTileFactory.createBlank(), DefaultTileFactory.createRight()}
        down: set[Tile] = {DefaultTileFactory.createUp(), DefaultTileFactory.createLeft(), DefaultTileFactory.createRight()}
        left: set[Tile] = {DefaultTileFactory.createUp(), DefaultTileFactory.createDown(), DefaultTileFactory.createRight()}

        ruleSet = TileRuleSet(up, right, down, left)
        DefaultTileRuleSetFactory._createdRuleSets[DefaultTileRuleSetFactory.LEFT_ID] = ruleSet

        return ruleSet
    
LANDSCAPE_TILES_PATH = './tiles/landscape/'
class LandscapeTileFactory:
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

    @staticmethod
    def createAll() -> list[Tile]:
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
    
class LandscapeTileRuleSetFactory:
    #region Tile Ruleset IDs
    GRASS_ID: int = 0
    WATER_ID: int = 1
    FLOWER_ID: int = 2
    LIGHT_FOREST_ID: int = 3
    #endregion

    # for flyweight pattern
    _createdRuleSets: dict[int, TileRuleSet] = {}
    _allRuleSets: dict[Tile, TileRuleSet] | None = None

    @staticmethod
    def createAll() -> dict[Tile, TileRuleSet]:
        if (LandscapeTileRuleSetFactory._allRuleSets != None):
            return LandscapeTileRuleSetFactory._allRuleSets
        
        ruleSets: dict[Tile, TileRuleSet] = {}
        ruleSets[LandscapeTileFactory.createFlower1()] = LandscapeTileRuleSetFactory.createFlowers()
        ruleSets[LandscapeTileFactory.createFlower2()] = LandscapeTileRuleSetFactory.createFlowers()
        ruleSets[LandscapeTileFactory.createWater1()] = LandscapeTileRuleSetFactory.createWaters()
        ruleSets[LandscapeTileFactory.createWater2()] = LandscapeTileRuleSetFactory.createWaters()
        ruleSets[LandscapeTileFactory.createGrass1()] = LandscapeTileRuleSetFactory.createGrasses()
        ruleSets[LandscapeTileFactory.createGrass2()] = LandscapeTileRuleSetFactory.createGrasses()
        ruleSets[LandscapeTileFactory.createLightForest1()] = LandscapeTileRuleSetFactory.createLightForests()
        ruleSets[LandscapeTileFactory.createLightForest2()] = LandscapeTileRuleSetFactory.createLightForests()
        
        LandscapeTileRuleSetFactory._allRuleSets = ruleSets

        return ruleSets

    @staticmethod
    def createGrasses() -> TileRuleSet:
        if (LandscapeTileRuleSetFactory.GRASS_ID in LandscapeTileRuleSetFactory._createdRuleSets):
            return LandscapeTileRuleSetFactory._createdRuleSets[LandscapeTileRuleSetFactory.GRASS_ID]
        
        possibilities: set[Tile] = {LandscapeTileFactory.createGrass1(), LandscapeTileFactory.createGrass2(),
        LandscapeTileFactory.createFlower1(), LandscapeTileFactory.createFlower2(),
        LandscapeTileFactory.createWater1(), LandscapeTileFactory.createWater2(),
        LandscapeTileFactory.createLightForest1(), LandscapeTileFactory.createLightForest2()}

        up: set[Tile] = possibilities
        right: set[Tile] = possibilities
        down: set[Tile] = possibilities
        left: set[Tile] = possibilities

        ruleSet = TileRuleSet(up, right, down, left)
        LandscapeTileRuleSetFactory._createdRuleSets[LandscapeTileRuleSetFactory.GRASS_ID] = ruleSet

        return ruleSet
    
    @staticmethod
    def createWaters() -> TileRuleSet:
        if (LandscapeTileRuleSetFactory.WATER_ID in LandscapeTileRuleSetFactory._createdRuleSets):
            return LandscapeTileRuleSetFactory._createdRuleSets[LandscapeTileRuleSetFactory.WATER_ID]
        
        possibilities: set[Tile] = {LandscapeTileFactory.createGrass1(), LandscapeTileFactory.createGrass2(),
        LandscapeTileFactory.createFlower1(), LandscapeTileFactory.createFlower2(),
        LandscapeTileFactory.createWater1(), LandscapeTileFactory.createWater2(),
        LandscapeTileFactory.createLightForest1(), LandscapeTileFactory.createLightForest2()}

        up: set[Tile] = possibilities
        right: set[Tile] = possibilities
        down: set[Tile] = possibilities
        left: set[Tile] = possibilities

        ruleSet = TileRuleSet(up, right, down, left)
        LandscapeTileRuleSetFactory._createdRuleSets[LandscapeTileRuleSetFactory.WATER_ID] = ruleSet

        return ruleSet
    
    @staticmethod
    def createFlowers() -> TileRuleSet:
        if (LandscapeTileRuleSetFactory.FLOWER_ID in LandscapeTileRuleSetFactory._createdRuleSets):
            return LandscapeTileRuleSetFactory._createdRuleSets[LandscapeTileRuleSetFactory.FLOWER_ID]
        
        possibilities: set[Tile] = {LandscapeTileFactory.createGrass1(), LandscapeTileFactory.createGrass2(),
        LandscapeTileFactory.createFlower1(), LandscapeTileFactory.createFlower2(),
        LandscapeTileFactory.createWater1(), LandscapeTileFactory.createWater2()}

        up: set[Tile] = possibilities
        right: set[Tile] = possibilities
        down: set[Tile] = possibilities
        left: set[Tile] = possibilities

        ruleSet = TileRuleSet(up, right, down, left)
        LandscapeTileRuleSetFactory._createdRuleSets[LandscapeTileRuleSetFactory.FLOWER_ID] = ruleSet

        return ruleSet
    
    @staticmethod
    def createLightForests() -> TileRuleSet:
        if (LandscapeTileRuleSetFactory.LIGHT_FOREST_ID in LandscapeTileRuleSetFactory._createdRuleSets):
            return LandscapeTileRuleSetFactory._createdRuleSets[LandscapeTileRuleSetFactory.LIGHT_FOREST_ID]
        
        possibilities: set[Tile] = {LandscapeTileFactory.createGrass1(), LandscapeTileFactory.createGrass2(),
        LandscapeTileFactory.createWater1(), LandscapeTileFactory.createWater2()}

        up: set[Tile] = possibilities
        right: set[Tile] = possibilities
        down: set[Tile] = possibilities
        left: set[Tile] = possibilities

        ruleSet = TileRuleSet(up, right, down, left)
        LandscapeTileRuleSetFactory._createdRuleSets[LandscapeTileRuleSetFactory.LIGHT_FOREST_ID] = ruleSet

        return ruleSet