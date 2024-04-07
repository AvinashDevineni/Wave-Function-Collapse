import pygame
from random import randint

class Tile:
    def __init__(self, imgPath: str) -> None:
        self.img: pygame.Surface = pygame.image.load(imgPath)
        self.imgPath = imgPath

    def __eq__(self, compare: object) -> bool:
        if (type(compare) != Tile):
            return False
        
        return self.imgPath == compare.imgPath
    
    def __hash__(self) -> int:
        return self.imgPath.__hash__()
    
    def __str__(self) -> str:
        return self.imgPath
    
    def __repr__(self) -> str:
        return self.__str__()
    
class TileFactory:
    #region Tile IDs
    MAX_ID = 4

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

        tiles.append(TileFactory.createBlank())
        tiles.append(TileFactory.createUp())
        tiles.append(TileFactory.createRight())
        tiles.append(TileFactory.createDown())
        tiles.append(TileFactory.createLeft())

        return tiles

    @staticmethod
    def createRandTile() -> Tile:
        return TileFactory.createById(randint(0, TileFactory.MAX_ID))

    @staticmethod
    def createById(id: int) -> Tile:
        if (id == TileFactory.BLANK_ID):
            return TileFactory.createBlank()
        
        if (id == TileFactory.UP_ID):
            return TileFactory.createUp()
        
        if (id == TileFactory.RIGHT_ID):
            return TileFactory.createRight()
        
        if (id == TileFactory.DOWN_ID):
            return TileFactory.createDown()
        
        if (id == TileFactory.LEFT_ID):
            return TileFactory.createLeft()
        
        else:
            raise ValueError()

    @staticmethod
    def createBlank() -> Tile:
        return TileFactory._createdTiles.get(TileFactory.BLANK_ID, Tile('./tiles/blank.png'))
    
    @staticmethod
    def createUp() -> Tile:
        return TileFactory._createdTiles.get(TileFactory.UP_ID, Tile('./tiles/up.png'))
    
    @staticmethod
    def createRight() -> Tile:
        return TileFactory._createdTiles.get(TileFactory.RIGHT_ID, Tile('./tiles/right.png'))
    
    @staticmethod
    def createDown() -> Tile:
        return TileFactory._createdTiles.get(TileFactory.DOWN_ID, Tile('./tiles/down.png'))
    
    @staticmethod
    def createLeft() -> Tile:
        return TileFactory._createdTiles.get(TileFactory.LEFT_ID, Tile('./tiles/left.png'))
  
class TileRuleSet:
    def __init__(self, up: set[Tile] = set(),
                 right: set[Tile] = set(), down: set[Tile] = set(), left: set[Tile] = set()) -> None:
        self.up: set[Tile] = up
        self.right: set[Tile] = right
        self.down: set[Tile] = down
        self.left: set[Tile] = left

class TileRuleSetFactory:
    #region Tile Ruleset IDs
    MAX_ID = 4

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
        if (TileRuleSetFactory._allRuleSets != None):
            return TileRuleSetFactory._allRuleSets
        
        ruleSets: dict[Tile, TileRuleSet] = {}

        ruleSets[TileFactory.createBlank()] = TileRuleSetFactory.createBlank()
        ruleSets[TileFactory.createUp()] = TileRuleSetFactory.createUp()
        ruleSets[TileFactory.createRight()] = TileRuleSetFactory.createRight()
        ruleSets[TileFactory.createDown()] = TileRuleSetFactory.createDown()
        ruleSets[TileFactory.createLeft()] = TileRuleSetFactory.createLeft()

        TileRuleSetFactory._allRuleSets = ruleSets

        return ruleSets

    @staticmethod
    def createBlank() -> TileRuleSet:
        if (TileRuleSetFactory.BLANK_ID in TileRuleSetFactory._createdRuleSets):
            return TileRuleSetFactory._createdRuleSets[TileRuleSetFactory.BLANK_ID]
        
        up: set[Tile] = {TileFactory.createBlank(), TileFactory.createUp()}
        right: set[Tile] = {TileFactory.createBlank(), TileFactory.createRight()}
        down: set[Tile] = {TileFactory.createBlank(), TileFactory.createDown()}
        left: set[Tile] = {TileFactory.createBlank(), TileFactory.createLeft()}

        ruleSet = TileRuleSet(up, right, down, left)
        TileRuleSetFactory._createdRuleSets[TileRuleSetFactory.BLANK_ID] = ruleSet

        return ruleSet
    
    @staticmethod
    def createUp() -> TileRuleSet:
        if (TileRuleSetFactory.UP_ID in TileRuleSetFactory._createdRuleSets):
            return TileRuleSetFactory._createdRuleSets[TileRuleSetFactory.UP_ID]
        
        up: set[Tile] = {TileFactory.createDown(), TileFactory.createLeft(), TileFactory.createRight()}
        right: set[Tile] = {TileFactory.createDown(), TileFactory.createLeft(), TileFactory.createUp()}
        down: set[Tile] = {TileFactory.createBlank(), TileFactory.createDown()}
        left: set[Tile] = {TileFactory.createDown(), TileFactory.createRight(), TileFactory.createUp()}

        ruleSet = TileRuleSet(up, right, down, left)
        TileRuleSetFactory._createdRuleSets[TileRuleSetFactory.UP_ID] = ruleSet

        return ruleSet
    
    @staticmethod
    def createRight() -> TileRuleSet:
        if (TileRuleSetFactory.RIGHT_ID in TileRuleSetFactory._createdRuleSets):
            return TileRuleSetFactory._createdRuleSets[TileRuleSetFactory.RIGHT_ID]
        
        up: set[Tile] = {TileFactory.createDown(), TileFactory.createRight(), TileFactory.createLeft()}
        right: set[Tile] = {TileFactory.createLeft(), TileFactory.createUp(), TileFactory.createDown()}
        down: set[Tile] = {TileFactory.createUp(), TileFactory.createLeft(), TileFactory.createRight()}
        left: set[Tile] = {TileFactory.createBlank(), TileFactory.createLeft()}

        ruleSet = TileRuleSet(up, right, down, left)
        TileRuleSetFactory._createdRuleSets[TileRuleSetFactory.RIGHT_ID] = ruleSet

        return ruleSet
    
    @staticmethod
    def createDown() -> TileRuleSet:
        if (TileRuleSetFactory.DOWN_ID in TileRuleSetFactory._createdRuleSets):
            return TileRuleSetFactory._createdRuleSets[TileRuleSetFactory.DOWN_ID]
        
        up: set[Tile] = {TileFactory.createBlank(), TileFactory.createUp()}
        right: set[Tile] = {TileFactory.createLeft(), TileFactory.createUp(), TileFactory.createDown()}
        down: set[Tile] = {TileFactory.createUp(), TileFactory.createLeft(), TileFactory.createRight()}
        left: set[Tile] = {TileFactory.createRight(), TileFactory.createUp(), TileFactory.createDown()}

        ruleSet = TileRuleSet(up, right, down, left)
        TileRuleSetFactory._createdRuleSets[TileRuleSetFactory.DOWN_ID] = ruleSet

        return ruleSet
    
    @staticmethod
    def createLeft() -> TileRuleSet:
        if (TileRuleSetFactory.LEFT_ID in TileRuleSetFactory._createdRuleSets):
            return TileRuleSetFactory._createdRuleSets[TileRuleSetFactory.LEFT_ID]
        
        up: set[Tile] = {TileFactory.createDown(), TileFactory.createLeft(), TileFactory.createRight()}
        right: set[Tile] = {TileFactory.createBlank(), TileFactory.createRight()}
        down: set[Tile] = {TileFactory.createUp(), TileFactory.createLeft(), TileFactory.createRight()}
        left: set[Tile] = {TileFactory.createUp(), TileFactory.createDown(), TileFactory.createRight()}

        ruleSet = TileRuleSet(up, right, down, left)
        TileRuleSetFactory._createdRuleSets[TileRuleSetFactory.LEFT_ID] = ruleSet

        return ruleSet