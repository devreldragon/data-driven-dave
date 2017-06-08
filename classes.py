def ErrorInvalidValue():
    raise ValueError("Please enter a valid value.")


class MapNode(object):
    ''' 
    MapNode represents a node that belongs to a map of the game.
    It has the following arguments:
        pos_x: integer stores the x position of the node.
        pos_y: integer stores the y position of the node.
        tile: Tile stores the current tile in this position.
    '''

    '''
    Constructors
    '''
    
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.tile = Tile()
    
    def __init__(self, pos_x, pos_y, tile):
        if not(isinstance(pos_x, int)) or not(isinstance(pos_y, int)) or not(Tile.checkinstance(tile)):
            ErrorInvalidValue()
        else:
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.tile = tile
    
    '''
    Other methods
    '''
        
    '''
    Getters and setters
    '''
    
    def setPos_x(self, pos_x):
        if isistance(pos_x, int):
            self.pos_x = pos_x
        else: ErrorInvalidValue()
            
    def setPos_y(self, pos_y):
        if isistance(pos_y, int):
            self.pos_y = pos_y
        else: ErrorInvalidValue()
            
    def setTile(self, tile):
        if Tile.checkinstance(tile):
            self.tile = tile
        else: ErrorInvalidValue()
            
    def getPos_x(self):
        return self.pos_x
        
    def getPos_y(self):
        return self.pos_y
        
    def getTile(self):
        return self.tile
        
        
class Tile(object):
    '''
    Tile is the base class for all available tiles within the game
    It has the following arguments:
        id: integer represents the id of the tile
        gfx_id: integer represents the id of the gfx to be used by the tile
    '''
    
    '''
    Constants (predefined tiles)
    '''
    
    TILESET = ("EMPTY", 
                "BLOCK_RED", "BLOCK_BLUE", "BLOCK_DIRT", "BLOCK_BRIDGE", "BLOCK_FLAT",
                "HAZ_WATER", "HAZ_FIRE", "HAZ_ALGAE",
                "ITEM_BLUE_DIAMOND", "ITEM_RED_DIAMOND", "ITEM_ORB", "ITEM_RING", "ITEM_CROWN", "ITEM_SCEPTER",
                "EQUIP_TROPHY", "EQUIP_JETPACK", "EQUIP_GUN", "GOAL_DOOR",
                "SCENERY_LEAVES", "SCENERY_TREE_LOG", "SCENERY_STARS", "SCENERY_FAKE_BRIDGE",
                "ENEMY_SPIDER", "ENEMY_PURPLE", "ENEMY_RED", "ENEMY_BATON", "ENEMY_CLOUD", "ENEMY_UFO", "ENEMY_GREEN", "ENEMY_DISC",
                "PLAYER_SPAWNER")
    
    
    '''
    Constructors
    '''
    
    def __init__(self):
        self.id = TILESET.index("EMPTY")
        self.gfx_id = TILESET.index("EMPTY")
        
    def __init__(self, id, gfx_id):
        if not(isinstance(id, int)) or not(isinstance(gfx_id, int)):
            ErrorInvalidValue()
        else:
            self.id = id
            self.gfx_id = gfx_id
    
    '''
    Other methods
    '''
    
    '''
    Getters and setters
    '''
    
    def setId(self, id):
        if isinstance(id, int):
            self.id = id
        else: ErrorInvalidValue()
    
    def setGfx_id(self, gfx_id):
        if isinstance(gfx_id, int):
            self.gfx_id = gfx_id
        else: ErrorInvalidValue()
        
    def getId(self):
        return self.id
        
    def getGfx_id(self):
        return self.gfx_id
        

class Solid(Tile):
    '''
    Solid is an abstract class which represents a solid tile (block) in the game
    It has no new arguments or methods
    '''   
    
        
class Item(Tile):
    '''
    Item represents a tile that can be collected by the player
    It extends Tile, and has the following arguments:
        score: integer represents the score given to the player when collecting it.
    '''    
    
    '''
    Constructors
    '''
    
    def __init__(self):
        self.id = TILESET.index("ITEM_BLUE_DIAMOND")
        self.gfx_id = TILESET.index("ITEM_BLUE_DIAMOND")
        self.score = 100
    
    def __init__(self, id, gfx_id, score):
        if not(isinstance(id, int)) or not(isinstance(gfx_id, int)) or not(isinstance(score, int) or score < 0):
            ErrorInvalidValue()
        else:
            self.id = id
            self.gfx_id = gfx_id 
            self.score = score
    
    '''
    Other methods
    '''
    
    '''
    Getters and setters
    '''
    
    def setScore(self, score):
        if isinstance(score, int) and score > 0:
            self.score = score
        else: ErrorInvalidValue()
        
    def getScore(self):
        return self.score
    
    
class Equipment(Item):
    '''
    Collectible represents an item that gives scores to the player when collected
    It extends Item, and has the following arguments:
        type: string represents if the equipment is a trophy, jetpack or gun
    '''    
    
    def __init__(self):
        self.id = TILESET.index("EQUIP_TROPHY")
        self.gfx_id = TILESET.index("EQUIP_TROPHY")
        self.score = 1000
        self.type = "trophy"
    
    def __init__(self, id, gfx_id, score, type):
        if not(isinstance(id, int)) or not(isinstance(gfx_id, int)) or not(isinstance(score, int)) or not(self.validType(type)) or score < 0:
            ErrorInvalidValue()
        else:
            self.id = id
            self.gfx_id = gfx_id 
            self.score = score
            self.type = type
    
    '''
    Other methods
    '''
    
    def validType(self, type):
        if type in ["trophy", "jetpack", "gun"]:
            return 1
        else: return 0
    
    '''
    Getters and setters
    '''
    
    def setType(self, type):
        if self.validType(type):
            self.type = type
        else: ErrorInvalidValue()
        
    def getType(self):
        return self.type 
    

class InteractiveScenery(Tile):
    '''
    InteractiveScenery represents a scenery tile which the player can interact with
    It has the following arguments:
        player_state: string indicating the state the player can get when interacting with this object
        auto: boolean indicating if the state above is called automatically when having contact with the object
    '''   

    '''
    Constructors
    '''
    
    def __init__(self):
        self.id = TILESET.index("GOAL_DOOR")
        self.gfx_id = TILESET.index("GOAL_DOOR")
        self.player_state = "endmap"
        self.auto = 1
        
    def __init__(self, id, gfx_id, player_state, auto):
        if not(isinstance(id, int)) or not(isinstance(gfx_id, int)) or not(self.validState(player_state)) or (auto not in [0, 1]):
            ErrorInvalidValue()
        else:
            self.id = id
            self.gfx_id = gfx_id
            self.player_state = player_state
            self.auto = auto
            
    '''
    Other methods
    '''
    
    def validState(state):
        if state in ["endmap", "climb", "die"]:
            return 1
        else: return 0
    
    '''
    Getters and setters
    '''
    
    def setPlayerState(self, player_state):
        if self.validState(player_state):
            self.player_state = player_state
        else: ErrorInvalidValue()
        
    def setAuto(self, auto):
        if auto in [0,1]:
            self.auto = auto
        else: ErrorInvalidValue()
        
    def getPlayerState():
        return self.player_state
        
    def getAuto():
        return self.auto


class Dynamic(Tile):
    '''
    Dynamic represents a dynamic object in the game, which can be a player or an enemy (two different classes)
    It has no new arguments.
    '''
    
    '''
    Other methods
    '''
    
    def moveLeft(self):
        self.pos_x += 1
    
    def moveRight(self):
        self.pos_x -= 1
    
    def moveUp(self):
        self.pos_y -= 1
        
    def moveDown(self):
        self.pos_y += 1
    
    def setState(self, state):
    ''' puts the object into the given state '''
        pass
    