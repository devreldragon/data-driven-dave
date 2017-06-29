
import sys
from math import floor
from enum import Enum #WE SO FUCKING NEED THIS AAAAAA

'''
Constants and enumerations
'''

TILE_SCALE_FACTOR = 2
WIDTH_OF_MAP_NODE = 16
HEIGHT_OF_MAP_NODE = 16
SCREEN_SHIFTING_VELOCITY = 0.5

BOUNDARY_DISTANCE_TRIGGER = 25
SCREEN_WIDTH_TILES = 20
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 208

class direction(Enum):
    LEFT = -1
    IDLE = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

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

class Map(object):
    '''
    Map represents a logic map of the level
    It has the following arguments:
        height: height of the map
        width: width of the map
        node_matrix: a matrix of MapNodes representing the map
    '''

    '''
    Constants
    '''
    
    COLLISION = Enum('COLLISION', 'NONE SOLID ENEMY ITEM EQUIP INTSCEN')
    
    '''
    Methods
    '''
    
    def __init__(self, *args):
        #default constructor
        if(len(args) == 0):
            self.height = 11
            self.width = 150
            self.node_matrix = [[MapNode() for i in range(self.width)] for j in range(self.height)]
        elif(len(args) == 2):
            ''' TODO: TEST INSTANCES '''
            self.height = args[0]
            self.width = args[1]
            self.node_matrix = [[MapNode() for i in range(self.width)] for j in range(self.height)]        
        else: ErrorInvalidConstructor()

    def addMapLine(self):
        self.height += 1
        self.node_matrix.append([MapNode() for i in range(self.width)])

    def addMapColumn(self):
        self.width += 1
        for map_line in self.node_matrix:
            map_line.append(MapNode())

    def buildMapBorder(self, tile):
        bottom = self.height - 1
        right = self.width - 1

        for x in range(right + 1):
            self.setNodeTile(x, 1, tile)
            self.setNodeTile(x, bottom, tile)

        for y in range(2, bottom):
            self.setNodeTile(0, y, tile)
            self.setNodeTile(right, y, tile)

    def buildWall(self, x, tile):
        for y in range(1, self.height):
            self.setNodeTile(x, y, tile)

    def setNodeTile(self, x, y, tile):
        if (x < self.width) and (y < self.height):
            self.node_matrix[y][x].setTile(tile)
        else: ErrorInvalidValue()

    def clearPlayerPosition(self):
        playerPosition = self.getPlayerPosition()
        self.setNodeTile(playerPosition[0], playerPosition[1], Tile())
        
    def getNode(self, x, y):
        return self.node_matrix[y][x]

    def getPlayerPosition(self):
        for y, line in enumerate(self.node_matrix):
            for x, col in enumerate(line):
                if self.node_matrix[y][x].getTile().getId() == "player":
                    return (x, y)

    def getPlayer(self):
        playerPos = self.getPlayerPosition()
        y = playerPos[1]
        x = playerPos[0]
        return self.node_matrix[y][x].getTile()

    def getCollisionType(self, x, y):
        solid = isinstance(self.node_matrix[y][x].getTile(), Solid)
        item = isinstance(self.node_matrix[y][x].getTile(), Item)
        intscen = isinstance(self.node_matrix[y][x].getTile(), InteractiveScenery)
        enemy = isinstance(self.node_matrix[y][x].getTile(), Enemy)
        
        if solid:
            return self.COLLISION.SOLID
        elif item:
            return self.COLLISION.ITEM
        elif intscen:
            return self.COLLISION.INTSCEN
        elif enemy:
            return self.COLLISION.ENEMY
        else:
            return False
        
    def checkCollision(self, player_pos, solid_only=False):
        TOLERANCE_VALUE = 1 #the dave can walk a little bit "into" the blocks
    
        x_left = floor((player_pos[0] + TOLERANCE_VALUE)/16)
        y_top = floor((player_pos[1])/16)
        x_right = floor((player_pos[0] + 15 - TOLERANCE_VALUE) / 16)
        y_bottom = floor((player_pos[1] + 15) / 16)

        collision_topleft = self.getCollisionType(x_left, y_top)
        collision_topright = self.getCollisionType(x_right, y_top)
        collision_bottomleft = self.getCollisionType(x_left, y_bottom)
        collision_bottomright = self.getCollisionType(x_right, y_bottom)

        ## GAMBIARRA: collision priority (won't check others if solid_only = true):
        priority = [self.COLLISION.SOLID, self.COLLISION.ITEM, self.COLLISION.ENEMY, self.COLLISION.INTSCEN]
        
        for col in priority:
            if collision_topleft == col:
                return (collision_topleft, (x_left, y_top))
            elif collision_topright == col:
                return (collision_topright, (x_right, y_top))
            elif collision_bottomleft == col:
                return (collision_bottomleft, (x_left, y_bottom))
            elif collision_bottomright == col:
                return (collision_bottomright, (x_right, y_bottom))
            if solid_only: break
        
        return (self.COLLISION.NONE, (-1,-1))

    def checkSolidCollision(self, player_pos):
        return (self.checkCollision(player_pos, True)[0] == self.COLLISION.SOLID)
        
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
            pos_x = args[0]
            pos_y = args[1]
            tile = args[2]

            if not(isinstance(pos_x, int)) or not(isinstance(pos_y, int)): #or not(Tile.isTileValid(tile)):
                ErrorInvalidValue()
            else:
                self.pos_x = pos_x
                self.pos_y = pos_y
                self.tile = tile
        else: ErrorInvalidConstructor()

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

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "scenery"
            self.gfx_id = 0
        #alternative constructor (self, id, gfx_id)
        elif len(args) == 2:
            id = args[0]
            gfx_id = args[1]

            if not(isinstance(id, str)) or not(isinstance(gfx_id, int)):
                ErrorInvalidValue()
            else:
                self.id = id
                self.gfx_id = gfx_id
        else: ErrorInvalidConstructor()

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


class Scenery(Tile):
    '''
    Scenery represents a scenery tile in the game
    It has no new arguments
    '''

    '''
    Constructors
    '''

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "scenery"
            self.gfx_id = 0
        #alternative constructor (self, id, gfx_id)
        elif len(args) == 2:
            id = args[0]
            gfx_id = args[1]

            if not(isinstance(id, str)) or not(isinstance(gfx_id, int)):
                ErrorInvalidValue()
            else:
                self.id = id
                self.gfx_id = gfx_id
        else: ErrorInvalidConstructor()
 
 
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
        #alternative constructor (self, id, gfx_id)
        elif len(args) == 2:
            id = args[0]
            gfx_id = args[1]

            if not(isinstance(id, str)) or not(isinstance(gfx_id, int)):
                ErrorInvalidValue()
            else:
                self.id = id
                self.gfx_id = gfx_id
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
            id = args[0]
            gfx_id = args[1]
            score = args[2]

            if not(isinstance(id, str)) or not(isinstance(gfx_id, int)) or not(isinstance(score, int) or score < 0):
                ErrorInvalidValue()
            else:
                self.id = id
                self.gfx_id = gfx_id
                self.score = score
        else: ErrorInvalidConstructor()

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

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "trophy"
            self.gfx_id = 0
            self.score = 1000
            self.type = "trophy"
        #alternative constructor (id, gfx_id, score, type)
        elif len(args) == 4:
            id = args[0]
            gfx_id = args[1]
            score = args[2]
            type = args[3]

            if not(isinstance(id, str)) or not(isinstance(gfx_id, int)) or not(isinstance(score, int)) or not(self.validType(type)) or score < 0:
                ErrorInvalidValue()
            else:
                self.id = id
                self.gfx_id = gfx_id
                self.score = score
                self.type = type
        else: ErrorInvalidConstructor()

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
        target_state: string indicating the state the player can go when interacting with this object
        auto: boolean indicating if the state above is called automatically when having contact with the object
    '''

    TYPE = Enum('TYPE', 'GOAL HAZARD TREE')
    
    '''
    Constructors
    '''

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "door"
            self.gfx_id = 0
            self.type = self.TYPE.GOAL
            self.auto = 1
        #alternative constructor (id, gfx_id, type, auto)
        elif len(args) == 4:
            id = args[0]
            gfx_id = args[1]
            type = args[2]
            auto = args[3]

            ''' TODO: TEST INSTANCES '''
            
            '''
            if not(isinstance(id, str)) or not(isinstance(gfx_id, int)) or not(self.isStateValid(target_state, possible_states)) or (auto not in [0, 1]):
                ErrorInvalidValue()
            else:
            '''
            self.id = id
            self.gfx_id = gfx_id
            self.type = type
            self.auto = auto
        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''

    '''
    Getters and setters
    '''

    def setType(self, type):
        ''' TODO: CHECK INSTANCE '''
        self.type = type
    
    def setAuto(self, auto):
        if auto in [0,1]:
            self.auto = auto
        else: ErrorInvalidValue()

    def getType(self):
        return self.type
        
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

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "undefined"
            self.gfx_id = -1
            self.state = Enum('state', 'UNDEFINED')
            self.cur_state = self.state.UNDEFINED
        #alternative constructor (id, gfx_id, states, cur_state)
        elif len(args) == 4:
            '''TODO: CHECK INSTANCES '''
            self.id = args[0]
            self.gfx_id = args[1]
            self.state = args[2]
            self.cur_state = args[3]
        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''

    '''
    def isStateValid(self, state):
        if state in self.state_list:
            return 1
        else: return 0
    '''
        
    '''
    Getters and setters
    '''

    def setCurrentState(self, state):
        ''' TODO: CHECK INSTANCE '''
        self.cur_state = state

    '''
    def setStateList(self, state_list):
        for state in state_list:
            if not(isinstance(state, str)):
                ErrorInvalidValue()
                return;
        self.state_list = state_list
        '''

    def getCurrentState(self):
        return self.cur_state

    '''
    def getStateList(self):
        return self.state_list
        '''

        
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
    
    '''
    Constructors
    '''

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "player"
            self.gfx_id = 0
            self.state = Enum('state', 'ENDMAP WALK FALL JUMP FLY CLIMB BLINK DIE')
            self.cur_state = self.state.BLINK
            self.velocity_y = 0                                             # The velocity and direction in the y axis (module + value)
            self.velocity_x = self.MAX_SPEED_X * self.X_SPEED_FACTOR        # The velocity in the x axis (only value)
            self.direction_x = direction.IDLE                               # Shows the current direction of movement (-1 = left, 1 = right, 0 = none)
            self.inventory = {"jetpack": 0, "gun": 0, "trophy": 0, "tree": 0}
            self.score = 0
            self.lifes = 3
       
            ##animation stuff
            self.animation_index = 0               # Number used to index the animation list of the corresponding state
            self.animation_counter = 0             # Counter that ticks until the next frame of animation should be displayed
            self.animation_index_list = {self.state.WALK : [1, 2, 3, 2], 
                                            self.state.BLINK : [0, -1], 
                                            self.state.FALL : [12], 
                                            self.state.JUMP : [12],
                                            self.state.CLIMB : [15, 16, 17],
                                            self.state.FLY : [24, 25, 26]}     # Dict of lists that specifies the index (displacement) of each animation frame based on the player tile. Indexed by the name of the self.state. (indexes are not integer because the tiles are not exactly the same size, apparently?)

        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''

    ## INPUT/KEYS TREATMENT
    def movementInput(self, pressed_keys):
        if self.cur_state in [self.state.ENDMAP, self.state.DIE]:
            return 0

        k_uparrow = (pressed_keys[0])
        k_leftarrow = (pressed_keys[1])
        k_rightarrow = (pressed_keys[2])
        k_downarrow = (pressed_keys[3])
        
        if k_uparrow:
            if self.cur_state in [self.state.BLINK, self.state.WALK] and self.inventory["tree"] == 1:
                self.setCurrentState(self.state.CLIMB)
                self.velocity_y = - self.MAX_SPEED_Y
                self.updateAnimation()
            elif self.cur_state in [self.state.BLINK, self.state.WALK]:
                self.setCurrentState(self.state.JUMP)
                self.velocity_y = - self.JUMP_SPEED
            elif self.cur_state in [self.state.FLY, self.state.CLIMB]:
                self.velocity_y = - self.MAX_SPEED_Y
        if k_leftarrow:
            self.direction_x = direction.LEFT

            if self.cur_state in [self.state.BLINK, self.state.WALK, self.state.JUMP, self.state.CLIMB, self.state.FLY]:
                self.velocity_x = self.MAX_SPEED_X * self.X_SPEED_FACTOR
            elif self.cur_state == self.state.FALL:
                self.velocity_x = self.MAX_SPEED_X #when falling, velocity increases to the max  
            if self.cur_state == self.state.BLINK:
                self.setCurrentState(self.state.WALK)
            elif self.cur_state == self.state.CLIMB and self.inventory["tree"] == 0:
                self.setCurrentState(self.state.FALL)
                self.velocity_y = self.MAX_SPEED_Y
        if k_rightarrow:
            self.direction_x = direction.RIGHT
            
            if self.cur_state in [self.state.BLINK, self.state.WALK, self.state.JUMP, self.state.CLIMB, self.state.FLY]:
                self.velocity_x = self.MAX_SPEED_X * self.X_SPEED_FACTOR
            elif self.cur_state == self.state.FALL:
                self.velocity_x = self.MAX_SPEED_X #when falling, velocity increases to the max
                
            if self.cur_state == self.state.BLINK:
                self.setCurrentState(self.state.WALK)
            elif self.cur_state == self.state.CLIMB and self.inventory["tree"] == 0:
                self.setCurrentState(self.state.FALL)
                self.velocity_y = self.MAX_SPEED_Y
        if k_downarrow:
            if self.cur_state in [self.state.CLIMB, self.state.FLY]:
                self.velocity_y = self.MAX_SPEED_Y

    def inventoryInput(self, key):
        if self.cur_state in [self.state.ENDMAP, self.state.DIE]:
            return -1
        
        k_ctrl = (key == 0) or (key == 1)
        k_alt = (key == 2) or (key == 3)
        
        if k_ctrl and self.inventory["jetpack"]:
            if self.cur_state == self.state.FLY:
                self.setCurrentState(self.state.FALL)
                self.velocity_x = self.MAX_SPEED_X #when falling, velocity increases to the max
                self.velocity_y = self.MAX_SPEED_Y 
            else:
                self.setCurrentState(self.state.FLY)
                self.velocity_x = 0
                self.velocity_y = 0
                self.updateAnimation()
        if k_alt and self.inventory["gun"]:
            return 1    #treat gunfire externally (because we need the map)
        return 0
                
    ## LIFES
    def takeLife(self):
        if self.lifes > 0:
            self.lifes -= 1
        else: 
            ''' TODO: GAME OVER '''
                    
    def giveLife(self):
        if self.lifes < self.MAX_LIFES:
            self.lifes += 1
        
    ## TREAT JUMPING
    def treatJumping(self):
        if self.cur_state == self.state.JUMP:
            self.addVelocityY(self.GRAVITY)             # Jumping is basically a velocity spike with a gravity based decay. This is basically calculating the decay at each frame.                   
            if self.velocity_y == self.MAX_SPEED_Y:
                self.setCurrentState(self.state.FALL)
                self.velocity_x = self.MAX_SPEED_X #when falling, velocity increases to the max
     
    ## TREAT SOLID COLLISION IN Y AXIS
    def treatSolidCollisionY(self, current_y, target_y):    
        # landed
        if self.cur_state in [self.state.JUMP, self.state.FALL] and target_y > current_y:
            self.setCurrentState(self.state.WALK)
            self.velocity_x = self.MAX_SPEED_X * self.X_SPEED_FACTOR
            self.velocity_y = 0
            self.direction_x = direction.IDLE
            self.updateAnimation()
        # was jumping and hit ceiling
        elif self.cur_state == self.state.JUMP:
            self.setCurrentState(self.state.FALL)
            self.velocity_x = self.MAX_SPEED_X  #when falling, velocity increases to the max
            self.velocity_y = self.MAX_SPEED_Y

    ## COLLECT AN ITEM OR EQUIPMENT AND SAVE SCORE
    def collectItem(self, item_pos, level):
        x = item_pos[0]
        y = item_pos[1]
        
        item = level.getNode(x, y).getTile()
        if isinstance(item, Equipment):
            self.inventory[item.getType()] = 1            
        self.score += item.getScore()
        
        if isinstance(self.score/5000, int):
            self.give_life()
        
        level.setNodeTile(x, y, Scenery())
        print(self.score)
    
    ## PROCESS SCENERY THAT'S INTERACTIVE
    def processScenerySpecial(self, element_pos, level):
        x = element_pos[0]
        y = element_pos[1]
    
        element = level.getNode(x, y).getTile()
        if element.getType() == element.TYPE.GOAL and self.inventory["trophy"] == 1:
            self.setCurrentState(self.state.ENDMAP)
        elif element.getType() == element.TYPE.HAZARD:
            self.setCurrentState(self.state.DIE)
            self.takeLife()
        elif element.getType() == element.TYPE.TREE:
            self.inventory["tree"] = 1
        
    ## TREAT ENEMY COLLISION
    def treatEnemyCollisionY(self, current_y, target_y):
        pass
            
    ## UPDATES THE PLAYER POSITION BASED ON THE STATE HE'S IN
    def updatePosition(self, player_x, player_y, level):        

        self.inventory["tree"] = 0    
        collision = level.checkCollision((player_x, player_y))
        collision_type = collision[0]
        collider_pos = collision[1]

        # Collect an item if there is one
        if collision_type == level.COLLISION.ITEM:
            self.collectItem(collider_pos, level)
        # Interact with scenery if one
        elif collision_type == level.COLLISION.INTSCEN:
            self.processScenerySpecial(collider_pos, level)
        # Collision with an enemy
        elif collision_type == level.COLLISION.ENEMY:
            ''' TODO: KILL BOTH ENEMY AND PLAYER '''
            pass
   
        # Checks if the player walked into a pit
        if self.cur_state == self.state.WALK:
            if not level.checkSolidCollision((player_x, player_y + 1)):       
                self.setCurrentState(self.state.FALL)
                self.velocity_x = self.MAX_SPEED_X
                self.velocity_y = self.MAX_SPEED_Y  

        ## Move X: START
        player_newx = player_x + self.velocity_x * self.direction_x.value                   # Tries to walk to the direction the player's going
        solid_collision = level.checkSolidCollision((player_newx, player_y))
                
        if solid_collision:                                                                 # If a collision occurs,
            player_newx = player_x                                                          # undo the movement
            if self.cur_state == self.state.FALL:                                           # If player's falling and released movement keys,
                self.direction_x = direction.IDLE                                           # stop the uncontrolled fall 
                self.velocity_x = 0
        ## Move X: END
            
        ## Move Y: START
        player_newy = player_y + self.velocity_y
   
        # Check for solid collisions
        solid_collision = level.checkSolidCollision((player_newx, player_newy))
        
        if self.cur_state != self.state.DIE:
            if solid_collision:
                self.treatSolidCollisionY(player_y, player_newy)
                player_newy = player_y
        
        # If jumping, gravity is acting upon the player
        self.treatJumping()
        ## Move Y: END
        
        ## Animation: START
        if (player_x != player_newx or player_y != player_newy) and self.cur_state != self.state.ENDMAP:          # If the player moved, updates the animation
            self.updateAnimation()
        ## Animation: END
        
        return (player_newx, player_newy)

    ## UPDATE ANIMATION
    def updateAnimation(self):
        # Rotate the animation counter and set the new gfx index
        if self.animation_counter < self.ANIMATION_COUNTER_MAX:       # Only updates if it's time to update (the counter reached its maximum)
            self.animation_counter = self.animation_counter + 1
        else:
            self.animation_counter = 0
            if self.animation_index < len(self.animation_index_list[self.cur_state]):           # Rotates the number that indexes the list of frames of that self.state.
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
        self.direction_x = direction.IDLE
            
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

