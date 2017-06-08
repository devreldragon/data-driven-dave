
import sys

'''
Constants
'''

TILESET = ("EMPTY", 
            "BLOCK_RED", "BLOCK_BLUE", "BLOCK_DIRT", "BLOCK_BRIDGE", "BLOCK_FLAT",
            "HAZ_WATER", "HAZ_FIRE", "HAZ_ALGAE",
            "ITEM_BLUE_DIAMOND", "ITEM_RED_DIAMOND", "ITEM_ORB", "ITEM_RING", "ITEM_CROWN", "ITEM_SCEPTER",
            "EQUIP_TROPHY", "EQUIP_JETPACK", "EQUIP_GUN", "GOAL_DOOR",
            "SCENERY_LEAVES", "SCENERY_TREE_LOG", "SCENERY_STARS", "SCENERY_FAKE_BRIDGE",
            "ENEMY_SPIDER", "ENEMY_PURPLE", "ENEMY_RED", "ENEMY_BATON", "ENEMY_CLOUD", "ENEMY_UFO", "ENEMY_GREEN", "ENEMY_DISC",
            "PLAYER_SPAWNER")
            
TILETERMINAL = (' ', 'B', 'B', 'B', 'B', 'B', 'H', 'H', 'H', 'b', 'd', 'o', 'r', 'c', 's', 'T', 'J', 'G', 'D', ';', '|', '*', 'B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'P')



def ErrorInvalidValue():
    raise ValueError("Please enter a valid value.")
    
    
class Map(object):
    '''
    Map represents a logic map of the level
    It has the following arguments:
        height: height of the map
        width: width of the map
        node_matrix: a matrix of MapNodes representing the map
    '''
    
    def __init__(self):
        self.height = 11
        self.width = 150
        self.node_matrix = [[MapNode() for i in range(self.width)] for j in range(self.height)]
        
    def addMapLine(self):
        self.height += 1
        self.node_matrix.append([MapNode() for i in range(self.width)])
        
    def addMapColumn(self):
        self.width += 1
        for map_line in self.node_matrix:
            map_line.append(MapNode())
            
    def setNodeTile(self, x, y, tile):
        if (x < self.width) and (y < self.height):
            self.node_matrix[y][x].setTile(tile)
            #print (self.node_matrix[y][x].pos_x)
        else: ErrorInvalidValue()
        
    def printMap(self):
        for map_line in self.node_matrix:
            for node in map_line:
                print(TILETERMINAL[node.tile.id], end='', flush=True)
            print()
            
    def getNode(self, x, y):
        return self.node_matrix[y][x]
            
    '''
    Getters and Setters
    '''
    
    def setHeight(self, height):
        if(height >= 0):
            self.height = height
        else: ErrorInvalidValue()
        
    def setWidth(self, width):
        if(width >= 0):
            self.width = width
        else: ErrorInvalidValue()
    
    def getHeight(self):
        return self.height
        
    def getWidth(self):
        return self.width


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
    
    def Construct(self, pos_x, pos_y, tile):
        if not(isinstance(pos_x, int)) or not(isinstance(pos_y, int)): #or not(Tile.isTileValid(tile)):
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
    
    def setPosX(self, pos_x):
        if isistance(pos_x, int):
            self.pos_x = pos_x
        else: ErrorInvalidValue()
            
    def setPosY(self, pos_y):
        if isistance(pos_y, int):
            self.pos_y = pos_y
        else: ErrorInvalidValue()
            
    def setTile(self, tile):
        self.tile = tile
        #if Tile.isTileValid(tile):
        #    self.tile = tile
        #else: ErrorInvalidValue()
            
    def getPosX(self):
        return self.pos_x
        
    def getPosY(self):
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
    Constructors
    '''
    
    def __init__(self):
        self.id = TILESET.index("EMPTY")
        self.gfx_id = TILESET.index("EMPTY")
        
    def Construct(self, id, gfx_id):
        if not(isinstance(id, int)) or not(isinstance(gfx_id, int)):
            ErrorInvalidValue()
        else:
            self.id = id
            self.gfx_id = gfx_id
    
    '''
    Other methods
    '''
    
    def isTileValid(tile):
        if isinstance(tile, Tile):
            if (tile.id < 0) or (tile.gfx_id < 0):
                return 0
            else: return 1
    
    '''
    Getters and setters
    '''
    
    def setId(self, id):
        if isinstance(id, int):
            self.id = id
        else: ErrorInvalidValue()
    
    def setGfxId(self, gfx_id):
        if isinstance(gfx_id, int):
            self.gfx_id = gfx_id
        else: ErrorInvalidValue()
        
    def getId(self):
        return self.id
        
    def getGfxId(self):
        return self.gfx_id

        
class Solid(Tile):
    '''
    Solid is an abstract class which represents a solid tile (block) in the game
    It has no new arguments
    '''   
    
    '''
    Constructors
    '''
    
    def __init__(self):
        self.id = TILESET.index("BLOCK_RED")
        self.gfx_id = TILESET.index("BLOCK_RED")
    
        
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
    
    @classmethod
    def Construct(self, id, gfx_id, score):
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
    
    @classmethod
    def Construct(self, id, gfx_id, score, type):
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
    
    def validType(type):
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
        target_state: string indicating the state the player can go when interacting with this object
        auto: boolean indicating if the state above is called automatically when having contact with the object
    '''   

    '''
    Constructors
    '''
    
    def __init__(self):
        self.id = TILESET.index("GOAL_DOOR")
        self.gfx_id = TILESET.index("GOAL_DOOR")
        self.target_state = "endmap"
        self.auto = 1
    
    @classmethod
    def Construct(self, id, gfx_id, target_state, auto, possible_states):
        if not(isinstance(id, int)) or not(isinstance(gfx_id, int)) or not(self.isStateValid(target_state, possible_states)) or (auto not in [0, 1]):
            ErrorInvalidValue()
        else:
            self.id = id
            self.gfx_id = gfx_id
            self.target_state = target_state
            self.auto = auto
            
    '''
    Other methods
    '''
    
    def isStateValid(state, possible_states):
        if state in possible_states:
            return 1
        else: return 0
    
    '''
    Getters and setters
    '''
    
    def setTargetState(self, target_state, possible_states):
        if self.isStateValid(target_state, possible_states):
            self.target_state = target_state
        else: ErrorInvalidValue()
        
    def setAuto(self, auto):
        if auto in [0,1]:
            self.auto = auto
        else: ErrorInvalidValue()
        
    def getTargetState(self):
        return self.target_state
        
    def getAuto(self):
        return self.auto


class Dynamic(Tile):
    '''
    Dynamic represents a dynamic object in the game, which can be a player or an enemy (two different classes)
    It has the following arguments:
        state: string represents the state of the object, which configures how the object behaves
        state_list: list of strings represents the available states of the object
    '''
    
    '''
    Constructors
    '''
    
    def __init__(self):
        self.id = -1
        self.gfx_id = -1
        self.state = -1
        self.state_list = []
        
    def Construct(self, id, gfx_id, state, state_list):
        pass
    
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
        
    def isStateValid(self, state):
        if state in self.state_list:
            return 1
        else: return 0
       
    def appendState(self, state):
        if isinstance(state, str):
            self.state_list.append(state)
        else: ErrorInvalidValue()
       
    '''
    Getters and setters
    '''
    
    def setState(self, state):
        if self.isStateValid(state):
            self.state = state
            self.gfx_id = 100 + state_list.index(state)
        else: ErrorInvalidValue()
        
    def setStateList(self, state_list):
        for state in state_list:
            if not(isinstance(state, str)):
                ErrorInvalidValue()
                return;
        self.state_list = state_list
        
    def getState(self):
        return self.state
        
    def getStateList(self):
        return self.state_list
    
    
class Player(Dynamic):
    '''
    Player represents the player object (not the controller) in the game
    It has no new arguments
    '''
    
    '''
    Constructors
    '''
    
    def __init__(self):
        self.id = TILESET.index("PLAYER_SPAWNER")
        self.gfx_id = TILESET.index("PLAYER_SPAWNER")
        self.state = "normal"
        self.state_list = ["endmap", "normal", "fly", "climb", "die"]
        
    def Construct(self, id, gfx_id, state, state_list):
        '''TODO: IMPLEMENT THIS (I'M TOO LAZY)'''
        pass
    
    '''
    Other methods
    '''
        
        
class Enemy(Dynamic):
    '''
    Enemy represents a moving enemy in the game
    It has the following arguments:
        shot_frequency: float represents the time interval, in seconds, the enemy can fire into the player
        shot_chance: float represents the chance of firing a projectile into the player the enemy has
        movement type: integer represents the movement of the enemy
        speed: float represents the enemy speed
    '''
    
    MOVEMENT_TYPES = ("idle", "straight", "back_and_forth", "ellipse", "cross", "spider", "special_purple", "special_red")
    
    '''
    Constructors
    '''
    
    def __init__(self):
        self.id = TILESET.index("ENEMY_SPIDER")
        self.gfx_id = TILESET.index("ENEMY_SPIDER")
        self.state = "normal"
        self.state_list = ["normal", "die"]
        self.shot_frequency = 2
        self.shot_chance = 0.3
        self.speed = 1
        self.movement_type = 1
        
    def Construct(self, id, gfx_id, state, state_list):
        '''TODO: IMPLEMENT THIS (I'M TOO LAZY NOW)'''
        pass
    
    '''
    Other methods
    '''
    
    '''
    Getters and setters
    '''
    
    '''TODO: IMPLEMENT THIS (I'M TOO LAZY NOW)'''
        