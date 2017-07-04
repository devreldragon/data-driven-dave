
import sys
from math import floor
from enum import Enum
from random import randint
import pygame

'''
Constants and enumerations
'''

TILE_SCALE_FACTOR = 2
WIDTH_OF_MAP_NODE = 16
HEIGHT_OF_MAP_NODE = 16
ANIMATION_VELOCITY = 2

BOUNDARY_DISTANCE_TRIGGER = 25

SCREEN_WIDTH = 320 * TILE_SCALE_FACTOR
SCREEN_HEIGHT = 208 * TILE_SCALE_FACTOR

TILE_IDS = []

class DIRECTION(Enum):
    LEFT = -1
    IDLE = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    
class COLLISION(Enum):
    SOLID = 0
    ITEM = 1
    ENEMY = 2
    INTSCEN = 3
    NONE = 4

class INTSCENERYTYPE(Enum):
    GOAL = 0
    HAZARD = 1
    TREE = 2

class STATE(Enum):
    ENDMAP = -1 
    WALK = 0
    FALL = 1
    JUMP = 2
    FLY = 3
    CLIMB = 4
    BLINK = 5
    DESTROY = 6 
    
''' TODO : CHECK IF THIS IS NECESSARY '''
class EQUIPTYPE(Enum):
    TROPHY = 0
    GUN = 1
    JETPACK = 2
    
'''
Errors
'''

def ErrorInvalidValue():
    raise ValueError("Please enter a valid value.")

def ErrorInvalidConstructor():
    raise ValueError("The entered constructor is not valid.")

'''
Classes
'''

class Screen(object):
    '''
    Screen is a class used to store the game screen (and the display along with it)
    It has the following attributes:
        width: integer represents the width of the screen in pixels
        height: integer represents the height of the screen in pixels
        x_pos: integer represents the X position of the screen inside the map (in tiles)
        display: pygame.display contains the display used in pygame to display the screen
    '''
    
    '''
    Constants
    '''
    
    GAME_SCREEN_START = 15
    GAME_SCREEN_END = 163
    SCREEN_SHIFTING_VELOCITY = 0.5
    
    '''
    Constructors
    '''
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x_pos = 0      
        self.display = pygame.display.set_mode((width, height))
        self.display.fill((0, 0, 0))  
        
    '''
    Other methods
    '''
        
    def isXInScreen(self, x):
        return (x >= self.x_pos) and (x < self.x_pos + self.getWidthInTiles())

    def printTile(self, x, y, tile_graphic):
        scaled_x = x * TILE_SCALE_FACTOR
        scaled_y = y * TILE_SCALE_FACTOR    
    
        # print the tile only if it's out of the UI
        if (y > self.GAME_SCREEN_START) and (y < self.GAME_SCREEN_END):
            self.display.blit(tile_graphic, (scaled_x, scaled_y))

    def printMap(self, map, tileset):
        for y, row in enumerate(map.getNodeMatrix()):
            for x, col in enumerate(row):
                tile = map.getNode(x,y).getTile()
                absolute_y = y * HEIGHT_OF_MAP_NODE
                
                # won't print the first line, neither other tiles that aren't in the game screen (considering the current x position)
                if self.isXInScreen(x) and (absolute_y > self.GAME_SCREEN_START) and (absolute_y < self.GAME_SCREEN_END):
                    adjusted_x = x - self.x_pos                                     #print the tile accordingly to the screen shift
                    absolute_x = adjusted_x * WIDTH_OF_MAP_NODE                     #store the x pos in pixels
                    tile_graphic = tile.getGraphic(tileset)                         #get the tile graphic
                    self.printTile(absolute_x, absolute_y, tile_graphic)
                    
    def printPlayer(self, player, player_x, player_y, tileset):
        player_graphic = player.getGraphic(tileset) 
        player.setSpriteDirection()
            
        if (player.isSpriteFlipped()):
            player_graphic = pygame.transform.flip(player_graphic,1,0)
                
        self.printTile(player_x, player_y, player_graphic)
                    
    def moveScreenX(self, map, amount, tileset):
        screen_shift = 0
        reached_level_left_boundary = (self.x_pos <= 0)
        reached_level_right_boundary = (self.x_pos + self.getWidthInTiles() >= map.getWidth())
        
        #going left
        while (screen_shift > amount) and not reached_level_left_boundary:
            self.printMap(map, tileset)
            pygame.display.flip()

            screen_shift -= self.SCREEN_SHIFTING_VELOCITY
            self.x_pos -= self.SCREEN_SHIFTING_VELOCITY 
            reached_level_left_boundary = (self.x_pos <= 0)

        #going right
        while (screen_shift < amount) and not reached_level_right_boundary:
            self.printMap(map, tileset)
            pygame.display.flip()
            
            screen_shift += self.SCREEN_SHIFTING_VELOCITY
            self.x_pos += self.SCREEN_SHIFTING_VELOCITY 
            reached_level_right_boundary = (self.x_pos + self.getWidthInTiles() >= map.getWidth())      
            
    '''
    Getters and setters
    '''
    
    def getWidth(self):
        return self.width
        
    def getUnscaledWidth(self):
        return int(self.width / TILE_SCALE_FACTOR)
        
    def getWidthInTiles(self):
        return int(self.width / (WIDTH_OF_MAP_NODE * TILE_SCALE_FACTOR))
        
    def getHeight(self):
        return self.height

    def getUnscaledHeight(self):
        return int(self.height / TILE_SCALE_FACTOR)
        
    def getHeightInTiles(self):
        return int(self.height / (HEIGHT_OF_MAP_NODE * TILE_SCALE_FACTOR))
        
    def getXPosition(self):
        return self.x_pos
        
    def getXPositionInPixelsUnscaled(self):
        return self.x_pos * WIDTH_OF_MAP_NODE
        
    def getDisplay(self):
        return self.display
        
    def setWidth(self, width):
        if not isinstance(width, int) and width < 0:
            ErrorInvalidValue()
        else:
            self.width = width;
            
    def setHeight(self, height):
        if not isinstance(height, int) and height < 0:
            ErrorInvalidValue()
        else:
            self.height = height;
            
    def setXPosition(self, x_position):
        if not isinstance(x_position, int) and x_position < 0:
            ErrorInvalidValue()
        else:
            self.x_pos = x_position;
            
    '''
    TODO: Does this work? Do we need it?
    def setDisplay(self, new_display):
        if not isinstance(new_display, pygame.display):
            ErrorInvalidValue()
        else:
            self.display = new_display
            '''

            
class Map(object):
    '''
    Map represents a logic map of the level
    It has the following arguments:
        height: height of the map
        width: width of the map
        node_matrix: a matrix of MapNodes representing the map
    '''

    '''
    Methods
    '''

    def __init__(self, *args):
        #default constructor
        if(len(args) == 0):
            self.height = 11
            self.width = 150
            self.node_matrix = self.buildMapMatrix()
        #alternative constructor (height, width)
        elif(len(args) == 2):
            if not self.validConstructorArgs(*args):
                ErrorInvalidValue()
            
            self.height = args[0]
            self.width = args[1]
            self.node_matrix = self.buildMapMatrix()
        else: ErrorInvalidConstructor()

    def buildMapMatrix(self):
        return [[MapNode() for i in range(self.width)] for j in range(self.height)]

    def validConstructorArgs(self, *args):
        height = args[0]
        width = args[1]
        
        return (isinstance(height, int) and isinstance(width, int) and height >= 0 and width >= 0)
        
    def validateCoordinates(self, x, y):
        return (isinstance(x, int) and isinstance(y, int) and x >= 0 and y >= 0 and x < self.width and y < self.height)
        
    def setNodeTile(self, x, y, tile):
        if self.validateCoordinates(x, y) and isinstance(tile, Tile):
            self.node_matrix[y][x].setTile(tile)
        else: ErrorInvalidValue()

    def getNode(self, x, y):
        if self.validateCoordinates(x, y):
            return self.node_matrix[y][x]
        else: ErrorInvalidValue()

    def getPlayerSpawnerPosition(self, spawner_id):
        for y, line in enumerate(self.node_matrix):
            for x, col in enumerate(line):
                if self.node_matrix[y][x].getTile().getId() == "player_spawner" and self.node_matrix[y][x].getTile().getSpawnerId() == spawner_id:
                    return (x, y)
        return (-1, -1)
                    
    def getCollisionType(self, x, y):
        if not self.validateCoordinates(x, y):
            ErrorInvalidValue()
    
        solid = isinstance(self.node_matrix[y][x].getTile(), Solid)
        item = isinstance(self.node_matrix[y][x].getTile(), Item)
        intscen = isinstance(self.node_matrix[y][x].getTile(), InteractiveScenery)
        enemy = isinstance(self.node_matrix[y][x].getTile(), Enemy)

        if solid:
            return COLLISION.SOLID
        elif item:
            return COLLISION.ITEM
        elif intscen:
            return COLLISION.INTSCEN
        elif enemy:
            return COLLISION.ENEMY
        else:
            return COLLISION.NONE

    def checkPlayerCollision(self, player_x, player_y, player_width, player_height, solid_only=False):
        TOLERANCE_VALUE = 3 #the dave can walk a little bit "into" the blocks
        
        ''' TODO: TEST X AND Y MAYBE? '''
        
        x_left = int((player_x + TOLERANCE_VALUE) // WIDTH_OF_MAP_NODE)
        y_top = int(player_y // HEIGHT_OF_MAP_NODE)
        x_right = int((player_x + player_width-1 - TOLERANCE_VALUE) // WIDTH_OF_MAP_NODE)
        y_bottom = int((player_y + player_height-1) // HEIGHT_OF_MAP_NODE)
   
        collision_topleft = self.getCollisionType(x_left, y_top)
        collision_topright = self.getCollisionType(x_right, y_top)
        collision_bottomleft = self.getCollisionType(x_left, y_bottom)
        collision_bottomright = self.getCollisionType(x_right, y_bottom)

        for col_type in COLLISION:
            if collision_topleft == col_type:
                return (collision_topleft, (x_left, y_top))
            elif collision_topright == col_type:
                return (collision_topright, (x_right, y_top))
            elif collision_bottomleft == col_type:
                return (collision_bottomleft, (x_left, y_bottom))
            elif collision_bottomright == col_type:
                return (collision_bottomright, (x_right, y_bottom))
            if solid_only: break
        
        return (COLLISION.NONE, (-1, -1))

    ''' TODO : PLAYER SIZE '''
    def isPlayerCollidingWithSolid(self, player_x, player_y, player_width=20, player_height=16):
        return (self.checkPlayerCollision(player_x, player_y, player_width, player_height, True)[0] == COLLISION.SOLID)

    def spawnFriendlyFire(self, direction):
        if (direction == DIRECTION.RIGHT) or (direction == DIRECTION.IDLE):
            shot = Shot()
        elif (direction == DIRECTION.LEFT): 
            shot = Shot("bullet", 1, DIRECTION.LEFT)
        else: ErrorInvalidValue()
        
        return shot
        
    def checkShotCollision(self, shot_x, shot_y, shot_width=12, shot_height=3):
        ''' TODO: TEST X AND Y MAYBE?'''
    
        x_left = int(shot_x // 16)
        y_top = int(shot_y // 16)
        x_right = int((shot_x + shot_width-1) // 16)
        y_bottom = int((shot_y + shot_height-1) // 16)
        
        collision_topleft = self.getCollisionType(x_left, y_top)
        collision_topright = self.getCollisionType(x_right, y_top)
        collision_bottomleft = self.getCollisionType(x_left, y_bottom)
        collision_bottomright = self.getCollisionType(x_right, y_bottom)  

        priority = [COLLISION.ENEMY, COLLISION.SOLID]
        
        for col_type in priority:
            if collision_topleft == col_type:
                return (collision_topleft, (x_left, y_top))
            elif collision_topright == col_type:
                return (collision_topright, (x_right, y_top))
            elif collision_bottomleft == col_type:
                return (collision_bottomleft, (x_left, y_bottom))
            elif collision_bottomright == col_type:
                return (collision_bottomright, (x_right, y_bottom))       
        
        return (COLLISION.NONE, (-1,-1))
        
    '''
    Getters and Setters
    '''

    def setHeight(self, height):
        if isinstance(height, int) and (height >= 0):
            self.height = height
        else: ErrorInvalidValue()

    def setWidth(self, width):
        if isinstance(width, int) and (width >= 0):
            self.width = width
        else: ErrorInvalidValue()

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def getNodeMatrix(self):
        return self.node_matrix


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

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.pos_x = 0
            self.pos_y = 0
            self.tile = Tile()
        #alternative constructor (pos_x, pos_y, tile)
        elif len(args) == 3:
            if not self.validConstructorArgs(*args):
                ErrorInvalidValue()
            
            self.pos_x = args[0]
            self.pos_y = args[1]
            self.tile = args[2]
        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''

    def validConstructorArgs(self, *args):
        pos_x = args[0]
        pos_y = args[1]
        tile = args[2]
        
        return (isinstance(pos_x, int) and isinstance(pos_y, int) and isinstance(tile, Tile) and pos_x >= 0 and pos_y >= 0)
    
    '''
    Getters and setters
    '''

    def setPosX(self, pos_x):
        if isistance(pos_x, int) and pos_x >= 0:
            self.pos_x = pos_x
        else: ErrorInvalidValue()

    def setPosY(self, pos_y):
        if isistance(pos_y, int) and pos_y >= 0:
            self.pos_y = pos_y
        else: ErrorInvalidValue()

    def setTile(self, tile):
        if isinstance(tile, Tile):
            self.tile = tile

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
        id: string represents the id of the tile
        gfx_id: integer represents the id of the gfx to be used by the tile
    '''

    '''
    Constructors
    '''

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "scenery"
            self.gfx_id = 0
        #alternative constructor (id, gfx_id)
        elif len(args) == 2:
            if not self.validConstructorArgs(*args):
                ErrorInvalidValue()
                
            self.id = args[0]
            self.gfx_id = args[1]
        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''
           
    def validConstructorArgs(self, *args):
        id = args[0]
        gfx_id = args[1]
        
        return (isinstance(id, str) and isinstance(gfx_id, int) and id in TILE_IDS and gfx_id >= -1)
           
    def getGraphic(self, tileset):   
        #if the tile id is a spawner, print a black scenery instead
        if self.isSpawner():
            subtileset = tileset["scenery"]
        else: subtileset = tileset[self.id]

        tile_width = subtileset[2]
        tile_height = subtileset[1]
        subtileset_image = subtileset[0]   

        #if the gfx_id is -1, print black scenery instead
        if(self.gfx_id == -1):
            return pygame.Surface((tile_width * TILE_SCALE_FACTOR, tile_height * TILE_SCALE_FACTOR))

        desired_tile_pos = self.gfx_id * tile_width

        #select the tile to crop (y is always 0)
        rectangle = (desired_tile_pos, 0, tile_width, tile_height)
        size_of_rectangle = (tile_width * TILE_SCALE_FACTOR, tile_height * TILE_SCALE_FACTOR)
        cropped_tile = pygame.transform.scale(subtileset_image.subsurface(rectangle), size_of_rectangle)
        
        return cropped_tile      

    def isSpawner(self):
        return ("spawner" in self.id)

    '''
    Getters and setters
    '''

    def setId(self, id):
        if isinstance(id, str) and id in TLE_IDS:
            self.id = id
        else: ErrorInvalidValue()

    def setGfxId(self, gfx_id):
        if isinstance(gfx_id, int) and gfx_id >= -1:
            self.gfx_id = gfx_id
        else: ErrorInvalidValue()

    def getId(self):
        return self.id

    def getGfxId(self):
        return self.gfx_id


class Scenery(Tile):
    '''
    Scenery represents a scenery tile in the game
    It has no new arguments or methods
    '''


class Solid(Tile):
    '''
    Solid is an abstract class which represents a solid tile (block) in the game
    It has no new arguments
    '''

    '''
    Constructors
    '''

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "solid"
            self.gfx_id = 2
        #alternative constructor (id, gfx_id)
        elif len(args) == 2:
            if not super(Solid, self).validConstructorArgs(*args):
                ErrorInvalidValue()
                
            self.id = args[0]
            self.gfx_id = args[1]
        else: ErrorInvalidConstructor()


class Item(Tile):
    '''
    Item represents a tile that can be collected by the player
    It extends Tile, and has the following arguments:
        score: integer represents the score given to the player when collecting it.
    '''

    '''
    Constructors
    '''

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "items"
            self.gfx_id = 1
            self.score = 100
        #alternative constructor (id, gfx_id, score)
        elif len(args) == 3:
            if not self.validConstructorArgs(*args):
                ErrorInvalidValue()

            self.id = args[0]
            self.gfx_id = args[1]
            self.score = args[2]
        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''

    def validConstructorArgs(self, *args):
        score = args[2]
        
        return (isinstance(score, int) and score >= 0 and super(Item, self).validConstructorArgs(args[0], args[1]))
    
    '''
    Getters and setters
    '''

    def setScore(self, score):
        if isinstance(score, int) and score >= 0:
            self.score = score
        else: ErrorInvalidValue()

    def getScore(self):
        return self.score


class Equipment(Item):
    '''
    Collectible represents an item that gives scores to the player when collected
    It extends Item, and has the following arguments:
        anim_timer: integer represents a timer for the animation of a trophy
    '''

    '''
    Constants
    '''
    
    ANIM_TIMER_MAX = 30
    
    '''
    Constructors
    '''
    
    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "trophy"
            self.gfx_id = 0
            self.score = 1000
            self.anim_timer = self.ANIM_TIMER_MAX
        #alternative constructor (id, gfx_id, score)
        elif len(args) == 3:
            if not super(Equipment, self).validConstructorArgs(*args):
                ErrorInvalidValue()
                
            self.id = args[0]
            self.gfx_id = args[1]
            self.score = args[2]
            self.anim_timer = self.ANIM_TIMER_MAX
        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''

    def getGraphic(self, tileset):
        #if it's a trophy, animate
        if self.id == "trophy":
            self.animateItem()

        #call superclass method
        return super(Equipment, self).getGraphic(tileset)    

    def animateItem(self):
        self.anim_timer -= ANIMATION_VELOCITY
        
        #if timer == 0, update
        if self.anim_timer == 0:
            self.anim_timer = self.ANIM_TIMER_MAX

            if self.gfx_id == 4:
                self.gfx_id = 0 
            else: self.gfx_id += 1
        
    '''
    Getters and setters
    
    ## There are no getters and setter for anim_timer as it is used only inside the class
    '''
    

class InteractiveScenery(Tile):
    '''
    InteractiveScenery represents a scenery tile which the player can interact with
    It has the following arguments:
        type: enumeration indicating the type of the tile
        anim_timer = integer represents the timer of the animation
    '''
    
    ANIM_TIMER_MAX = 30

    '''
    Constructors
    '''

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "door"
            self.gfx_id = 0
            self.type = INTSCENERYTYPE.GOAL
            self.anim_timer = self.ANIM_TIMER_MAX
        #alternative constructor (id, gfx_id, type)
        elif len(args) == 3:
            if not self.validConstructorArgs(*args):
                ErrorInvalidValue()
                
            self.id = args[0]
            self.gfx_id = args[1]
            self.type = args[2]
            self.anim_timer = self.ANIM_TIMER_MAX
        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''
    
    def validConstructorArgs(self, *args):
        type = args[2]
        
        return (isinstance(type, INTSCENERYTYPE) and super(InteractiveScenery, self).validConstructorArgs(args[0], args[1]))

    def getGraphic(self, tileset):
        if self.type == INTSCENERYTYPE.HAZARD:
            self.animateItem()

        #call superclass method
        return super(InteractiveScenery, self).getGraphic(tileset)
    
    def animateItem(self):
        self.anim_timer -= ANIMATION_VELOCITY
            
        if (self.anim_timer == 0):
            self.anim_timer = self.ANIM_TIMER_MAX
            if self.gfx_id == 3:
                self.gfx_id = 0 
            else: self.gfx_id += 1
    
    '''
    Getters and setters
    '''

    def setType(self, type):
        if isinstance(type, INTSCENERYTYPE):
            self.type = type
        else: ErrorInvalidValue()

    def getType(self):
        return self.type


class PlayerSpawner(Tile):
    '''
    PlayerSpawner represents a spawn point for the player in the map
    Note that one map can contain more than one spawner, but they must have different ids
    It has the following arguments:
        spawner_id: integer represents the id of the spawner
    '''
    
    '''
    Constructors
    '''
    
    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "player_spawner"
            self.gfx_id = -1
            self.spawner_id = 0
        #alternative constructor (id, gfx_id, spawner_id)
        elif len(args) == 3:
            if not self.validConstructorArgs(*args):
                ErrorInvalidValue()
            
            self.id = args[0]
            self.gfx_id = args[1]
            self.spawner_id = args[2]
        else: ErrorInvalidConstructor()
       
    '''
    Other methods
    '''
    
    def validConstructorArgs(self, *args):
        id = args[0]
        gfx_id = args[1]
        spawner_id = args[2]
        
        return (id == "player_spawner" and isinstance(gfx_id, int) and isinstance(spawner_id, int) and gfx_id >= -1 and spawner_id >= 0)   
    
    '''
    Getters and setters
    '''
       
    def getSpawnerId(self):
        return self.spawner_id
        
    def setSpawnerId(self, id):
        if not isinstance(id, int) or id < 0:
            ErrorInvalidValue()
        else:
            self.spawner_id = id

        
class Dynamic(Tile):
    '''
    Dynamic represents a dynamic object in the game, which can be a player, an enemy, a buller or an animated sprite (explosion for example)
    It has the following arguments:
        cur_state: enumeration represents the state of the object, which configures how the object behaves
    '''
    
    '''
    Constructors
    '''

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "undefined"
            self.gfx_id = -1
            self.cur_state = STATE.BLINK
        #alternative constructor (id, gfx_id, cur_state)
        elif len(args) == 3:
            if not self.validConstructorArgs(*args):
                ErrorInvalidValue()
                
            self.id = args[0]
            self.gfx_id = args[1]
            self.cur_state = args[2]
        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''
    
    def validConstructorArgs(self, *args):
        cur_state = args[2]
        
        return (isinstance(cur_state, STATE) and super(Dynamic, self).validConstructorArgs(args[0], args[1])) 
    
    '''
    Getters and setters
    '''

    def setCurrentState(self, state):
        if isinstance(state, STATE):
            self.cur_state = state
        else: ErrorInvalidValue()

    def getCurrentState(self):
        return self.cur_state


class Player(Dynamic):
    '''
    Player represents the player object (not the controller) in the game
    It has the following arguments:
        acceleration_y: acceleration in the y axis
        acceleration_x: acceleration in the x axis
    '''

    '''
    Constants
    '''

    SCALE_FACTOR = 2
    MAX_SPEED_X = 0.4 * SCALE_FACTOR
    MAX_SPEED_Y = 0.4 * SCALE_FACTOR
    JUMP_SPEED = 0.8
    X_SPEED_FACTOR = 0.75   #factor to be used when not falling (x speed only hits its maximum when falling)
    GRAVITY = 0.01          #gravity acceleration
    ANIMATION_COUNTER_MAX = 20
    MAX_LIFES = 5
    BLINKING_SPEED = 1

    '''
    Constructors
    '''

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "player"
            self.gfx_id = 0
            self.cur_state = STATE.BLINK
            self.velocity_y = 0                                             # The velocity and direction in the y axis (module + value)
            self.velocity_x = self.MAX_SPEED_X * self.X_SPEED_FACTOR        # The velocity in the x axis (only value)
            self.direction_x = DIRECTION.IDLE                               # Shows the current direction of movement (-1 = left, 1 = right, 0 = none)
            self.flip_sprite = True
            self.inventory = {"jetpack": 0, "gun": 0, "trophy": 0, "tree": 0}
            self.score = 0
            self.lifes = 3

            ##animation stuff
            self.animation_index = 0               # Number used to index the animation list of the corresponding state
            self.animation_counter = 0             # Counter that ticks until the next frame of animation should be displayed
            self.blinking_timer = self.BLINKING_SPEED
            self.animation_index_list = {STATE.WALK : [1, 2, 3, 2],
                                            STATE.BLINK : [0, -1],
                                            STATE.FALL : [12],
                                            STATE.JUMP : [12],
                                            STATE.CLIMB : [15, 16, 17],
                                            STATE.FLY : [24, 25, 26],
                                            STATE.DESTROY : [-1]}     # Dict of lists that specifies the index (displacement) of each animation frame based on the player tile. Indexed by the name of the STATE. (indexes are not integer because the tiles are not exactly the same size, apparently?)

        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''

    def getGraphic(self, tileset):
        return Tile.getGraphic(self, tileset)
    
    ## INPUT/KEYS TREATMENT
    def movementInput(self, pressed_keys):
        if self.cur_state in [STATE.ENDMAP, STATE.DESTROY]:
            return 0

        k_uparrow = (pressed_keys[0])
        k_leftarrow = (pressed_keys[1])
        k_rightarrow = (pressed_keys[2])
        k_downarrow = (pressed_keys[3])

        if k_uparrow:
            if self.cur_state in [STATE.BLINK, STATE.WALK] and self.inventory["tree"] == 1:
                self.setCurrentState(STATE.CLIMB)
                self.velocity_y = - self.MAX_SPEED_Y
                self.updateAnimation()
            elif self.cur_state in [STATE.BLINK, STATE.WALK]:
                self.setCurrentState(STATE.JUMP)
                self.velocity_y = - self.JUMP_SPEED
            elif self.cur_state in [STATE.FLY, STATE.CLIMB]:
                self.velocity_y = - self.MAX_SPEED_Y
                if self.cur_state == STATE.CLIMB and self.inventory["tree"] == 0:
                    self.setCurrentState(STATE.FALL)
                    self.velocity_y = self.MAX_SPEED_Y  
        if k_leftarrow:
            self.direction_x = DIRECTION.LEFT

            if self.cur_state in [STATE.BLINK, STATE.WALK, STATE.JUMP, STATE.CLIMB, STATE.FLY]:
                self.velocity_x = self.MAX_SPEED_X * self.X_SPEED_FACTOR
            elif self.cur_state == STATE.FALL:
                self.velocity_x = self.MAX_SPEED_X #when falling, velocity increases to the max
            if self.cur_state == STATE.BLINK:
                self.setCurrentState(STATE.WALK)
            elif self.cur_state == STATE.CLIMB and self.inventory["tree"] == 0:
                self.setCurrentState(STATE.FALL)
                self.velocity_y = self.MAX_SPEED_Y
        if k_rightarrow:
            self.direction_x = DIRECTION.RIGHT

            if self.cur_state in [STATE.BLINK, STATE.WALK, STATE.JUMP, STATE.CLIMB, STATE.FLY]:
                self.velocity_x = self.MAX_SPEED_X * self.X_SPEED_FACTOR
            elif self.cur_state == STATE.FALL:
                self.velocity_x = self.MAX_SPEED_X #when falling, velocity increases to the max

            if self.cur_state == STATE.BLINK:
                self.setCurrentState(STATE.WALK)
            elif self.cur_state == STATE.CLIMB and self.inventory["tree"] == 0:
                self.setCurrentState(STATE.FALL)
                self.velocity_y = self.MAX_SPEED_Y
        if k_downarrow:
            if self.cur_state in [STATE.CLIMB, STATE.FLY]:
                self.velocity_y = self.MAX_SPEED_Y
                if self.cur_state == STATE.CLIMB and self.inventory["tree"] == 0:
                    self.setCurrentState(STATE.FALL)
                    self.velocity_y = self.MAX_SPEED_Y                    

    def inventoryInput(self, key):
        if self.cur_state in [STATE.ENDMAP, STATE.DESTROY]:
            return -1

        k_ctrl = (key == 0) or (key == 1)
        k_alt = (key == 2) or (key == 3)

        if k_ctrl and self.inventory["jetpack"]:
            if self.cur_state == STATE.FLY:
                self.setCurrentState(STATE.FALL)
                self.velocity_x = self.MAX_SPEED_X #when falling, velocity increases to the max
                self.velocity_y = self.MAX_SPEED_Y
            else:
                self.setCurrentState(STATE.FLY)
                self.velocity_x = 0
                self.velocity_y = 0
                self.updateAnimation()
        if k_alt and self.inventory["gun"]:
            return 1    #treat gunfire externally (because we need the map)
        return 0

    def setSpriteDirection(self):
        if (self.direction_x == DIRECTION.RIGHT):
            self.flip_sprite = True
        elif (self.direction_x == DIRECTION.LEFT):
            self.flip_sprite = False  
            
    def isSpriteFlipped(self):
        return self.flip_sprite
        
    ## LIFES
    def takeLife(self):
        self.lifes -= 1

    def giveLife(self):
        if self.lifes < self.MAX_LIFES:
            self.lifes += 1
            
    def resetPosAndState(self):
        if self.lifes < 0:
            return -1
        
        self.setCurrentState(STATE.BLINK)
        self.gfxId = 0
        self.velocity_y = 0
        self.velocity_x = 0
        self.direction_x = DIRECTION.IDLE 
        self.blinking_timer = self.BLINKING_SPEED
            
    ## TREAT JUMPING
    def treatJumping(self):
        if self.cur_state == STATE.JUMP:
            self.addVelocityY(self.GRAVITY)             # Jumping is basically a velocity spike with a gravity based decay. This is basically calculating the decay at each frame.
            if self.velocity_y == self.MAX_SPEED_Y:
                self.setCurrentState(STATE.FALL)
                self.velocity_x = self.MAX_SPEED_X #when falling, velocity increases to the max

    ## TREAT SOLID COLLISION IN Y AXIS
    def treatSolidCollisionY(self, current_y, target_y):
        # landed
        if self.cur_state in [STATE.JUMP, STATE.FALL] and target_y > current_y:
            self.setCurrentState(STATE.WALK)
            self.velocity_x = self.MAX_SPEED_X * self.X_SPEED_FACTOR
            self.velocity_y = 0
            self.direction_x = DIRECTION.IDLE
            self.updateAnimation()
        # was jumping and hit ceiling
        elif self.cur_state == STATE.JUMP:
            self.setCurrentState(STATE.FALL)
            self.velocity_x = self.MAX_SPEED_X  #when falling, velocity increases to the max
            self.velocity_y = self.MAX_SPEED_Y

    ## COLLECT AN ITEM OR EQUIPMENT AND SAVE SCORE
    def collectItem(self, item_pos, level):
        x = item_pos[0]
        y = item_pos[1]

        item = level.getNode(x, y).getTile()
        if isinstance(item, Equipment):
            self.inventory[item.getId()] = 1
        self.score += item.getScore()

        if isinstance(self.score/5000, int):
            self.give_life()

        level.setNodeTile(x, y, Scenery())

    ## PROCESS SCENERY THAT'S INTERACTIVE
    def processScenerySpecial(self, element_pos, level):
        x = element_pos[0]
        y = element_pos[1]

        element = level.getNode(x, y).getTile()
        if element.getType() == INTSCENERYTYPE.GOAL and self.inventory["trophy"] == 1:
            self.setCurrentState(STATE.ENDMAP)
        elif element.getType() == INTSCENERYTYPE.HAZARD:
            self.setCurrentState(STATE.DESTROY)
            self.takeLife()
        elif element.getType() == INTSCENERYTYPE.TREE:
            self.inventory["tree"] = 1

    ## TREAT ENEMY COLLISION
    def treatEnemyCollisionY(self, current_y, target_y):
        pass

    ## UPDATES THE PLAYER POSITION BASED ON THE STATE HE'S IN
    def updatePosition(self, player_x, player_y, level):    
        self.inventory["tree"] = 0
        ''' TODO : PLAYER SIZE '''
        collision = level.checkPlayerCollision(player_x, player_y, 20, 16)
        collision_type = collision[0]

        collider_pos = collision[1]

        # Collect an item if there is one
        if collision_type == COLLISION.ITEM:
            self.collectItem(collider_pos, level)
        # Interact with scenery if one
        elif collision_type == COLLISION.INTSCEN:
            self.processScenerySpecial(collider_pos, level)
        # Collision with an enemy
        elif collision_type == COLLISION.ENEMY:
            ''' TODO: KILL BOTH ENEMY AND PLAYER '''
            pass

        # Checks if the player walked into a pit
        if self.cur_state == STATE.WALK:
            if not level.isPlayerCollidingWithSolid(player_x, player_y + 1):
                self.setCurrentState(STATE.FALL)
                self.velocity_x = self.MAX_SPEED_X
                self.velocity_y = self.MAX_SPEED_Y

        ## Move X: START
        player_newx = player_x + self.velocity_x * self.direction_x.value                   # Tries to walk to the direction the player's going
        solid_collision = level.isPlayerCollidingWithSolid(player_newx, player_y)

        if solid_collision:                                                                 # If a collision occurs,
            player_newx = player_x                                                          # undo the movement
            if self.cur_state == STATE.FALL:                                           # If player's falling and released movement keys,
                self.direction_x = DIRECTION.IDLE                                           # stop the uncontrolled fall
                self.velocity_x = 0
        ## Move X: END

        ## Move Y: START
        player_newy = player_y + self.velocity_y

        # Check for solid collisions
        solid_collision = level.isPlayerCollidingWithSolid(player_newx, player_newy)

        if self.cur_state != STATE.DESTROY:
            if solid_collision:
                self.treatSolidCollisionY(player_y, player_newy)
                player_newy = player_y

        # If jumping, gravity is acting upon the player
        self.treatJumping()
        ## Move Y: END

        ## Jetpack gas: START
        if (self.cur_state == STATE.FLY) and self.inventory["jetpack"] > 0:
            self.inventory["jetpack"] -= 0.005
        elif (self.cur_state == STATE.FLY):
            self.inventory["jetpack"] = 0
            self.setCurrentState(STATE.FALL)
            self.velocity_x = self.MAX_SPEED_X #when falling, velocity increases to the max
            self.velocity_y = self.MAX_SPEED_Y    
        ## Jetpack gas: END       
        
        ## Animation: START
        self.blinking_timer -= 1
        if (player_x != player_newx or player_y != player_newy) and self.cur_state != STATE.ENDMAP:          # If the player moved, updates the animation
            self.updateAnimation()
        elif self.cur_state == STATE.BLINK and self.blinking_timer == 0:
            self.updateAnimation()
            self.blinking_timer = self.BLINKING_SPEED
        ## Animation: END
        
        return (player_newx, player_newy)

    ## UPDATE ANIMATION
    def updateAnimation(self):
        # Rotate the animation counter and set the new gfx index
        if self.animation_counter < self.ANIMATION_COUNTER_MAX:       # Only updates if it's time to update (the counter reached its maximum)
            self.animation_counter = self.animation_counter + 1
        else:
            self.animation_counter = 0
            if self.animation_index < len(self.animation_index_list[self.cur_state]):           # Rotates the number that indexes the list of frames of that STATE.
                self.animation_index = self.animation_index + 1                                         # Basically means that the animation frames will alternate in the list's order.
            if self.animation_index == len(self.animation_index_list[self.cur_state]):
                self.animation_index = 0

        self.gfx_id = self.animation_index_list[self.cur_state][self.animation_index]          # Did not use setter here because we are not sending integer indexes.

    ## ADD A GIVEN INCREMENT TO THE VELOCITY ATTRIBUTE
    def addVelocityY(self, inc):
        self.velocity_y = self.velocity_y + inc
        #test limits
        if (self.velocity_y > self.MAX_SPEED_Y):
            self.velocity_y = self.MAX_SPEED_Y

    def clearXMovement(self):
        self.velocity_x = 0

    '''
    Getters and setters
    '''

    def setVelocityX(self, vel):
        '''TODO: TEST INSTANCE'''
        self.velocity_x = vel

    def setDirectionX(self, direction):
        '''TODO: TEST INSTANCE'''
        self.direction_x = direction

    def setVelocityY(self, vel):
        '''TODO: TEST INSTANCE'''
        self.velocity_y = vel

    def setCurrentState(self, newstate):
        '''TODO: TEST INSTANCE?'''
        self.cur_state = newstate
        self.animation_index = 0
        self.animation_counter = 0

    def getDirectionX(self):
        return self.direction_x

    def getVelocityY(self):
        return self.velocity_y

    def getVelocityX(self):
        return self.velocity_x

    def getGravity(self):
        return self.GRAVITY

    def getMaxSpeedX(self):
        return self.MAX_SPEED_X

    def getMaxSpeedY(self):
        return self.MAX_SPEED_Y

    def getXSpeedFactor(self):
        return self.X_SPEED_FACTOR


class AnimatedSprite(Dynamic):
    '''
    AnimatedSprite represents an animated sprite in the game.
    It has the following arguments:
        anim_timer: integer represents the animation timer of the sprite
    '''

    '''
    Constants
    '''    
    
    ANIM_TIMER_MAX = 30    
    
    '''
    Constructors
    '''

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "undefined"
            self.gfx_id = -1
            self.anim_timer = self.ANIM_TIMER_MAX
        #alternative constructor (id, gfx_id)
        elif len(args) == 2:
            '''TODO: CHECK INSTANCES '''
            self.id = args[0]
            self.gfx_id = args[1]
            self.anim_timer = self.ANIM_TIMER_MAX
        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''

    def getGraphic(self, tileset):
        self.anim_timer -= ANIMATION_VELOCITY
        
        if (self.anim_timer == 0):
            self.anim_timer = self.ANIM_TIMER_MAX
            
            if (self.id == "explosion"):
                if self.gfx_id == 3:
                    self.gfx_id = 0 
                else: self.gfx_id += 1

        #call superclass method
        return super(AnimatedSprite, self).getGraphic(tileset)
        

class Shot(Dynamic):
    '''
    Shot represents a shot in the game (going straight)
    It has the following arguments:
        direction: enumeration represents the direction of the shot
    '''
    
    '''
    Constants
    '''
    
    MAX_SPEED_X = 0.4 * TILE_SCALE_FACTOR
    
    '''
    Constructors
    '''

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "bullet"
            self.gfx_id = 0
            self.direction = DIRECTION.RIGHT
        #alternative constructor (id, gfx_id, direction)
        elif len(args) == 3:
            '''TODO: CHECK INSTANCES '''
            self.id = args[0]
            self.gfx_id = args[1]
            self.direction = args[2]
        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''
    
    def updatePosition(self, current_x, current_y, level):
        new_x = current_x + self.direction.value * self.MAX_SPEED_X
        
        collision = level.checkShotCollision(current_x, current_y)
        
        if (collision[0] == COLLISION.ENEMY):
            ''' TODO: KILL ENEMY '''
            return -1
        elif (collision[0] == COLLISION.SOLID):
            return -1
            
        return new_x
    
    '''
    Getters and setters
    '''   
    
    def setDirection(self, dir):
        ''' TODO: CHECK INSTANCE '''
        self.dir = dir
        
    def getDirection(self):
        return self.dir

        
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

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "spider"
            self.gfx_id = 0
            self.state = "normal"
            self.state_list = ["normal", "die"]
            self.shot_frequency = 2
            self.shot_chance = 0.3
            self.speed = 1
            self.movement_type = 1
        #alternative constructor (id, gfx_id, state, state_list, shot_freq, shot_chance, speed, mov_type)
        elif len(args) == 8:
            id, gfx_id, state, state_list, shot_freq, shot_chance, speed, mov_type = args
            '''TODO: IMPLEMENT THIS (I'M TOO LAZY NOW)'''
        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''

    '''
    Getters and setters
    '''

    '''TODO: IMPLEMENT THIS (I'M TOO LAZY NOW)'''
