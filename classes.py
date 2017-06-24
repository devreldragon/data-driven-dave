
import sys

from math import floor

'''
Constants
'''

##TODO: Review id() field in classes

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

        '''
    def printMap(self):
        for map_line in self.node_matrix:
            for node in map_line:
                print(TILETERMINAL[node.tile.id], end='', flush=True)
            print()
            '''

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

    def checkPlayerCollision(self, player_pos):
        x_left = floor(player_pos[0]/16)
        y_top = floor(player_pos[1]/16)
        x_right = floor((player_pos[0]+15) / 16)
        y_bottom = floor((player_pos[1]+15) / 16)

        ''' TODO: CHANGE THIS '''
        VALUE = "solid"

        collision_topleft = (self.node_matrix[y_top][x_left].getTile().getId() == VALUE)
        collision_topright = (self.node_matrix[y_top][x_right].getTile().getId() == VALUE)
        collision_bottomleft = (self.node_matrix[y_bottom][x_left].getTile().getId() == VALUE)
        collision_bottomright = (self.node_matrix[y_bottom][x_right].getTile().getId() == VALUE)

        if collision_topleft or collision_topright or collision_bottomleft or collision_bottomright:
            return "BLOCK_COLLISION"

        ''' TODO: TREAT OTHER COLLISIONS '''

        return "NO_COLLISION"


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

    '''
    Constructors
    '''

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "door"
            self.gfx_id = 0
            self.target_state = "endmap"
            self.auto = 1
        #alternative constructor (id, gfx_id, target_state, auto, possible_states)
        elif len(args) == 5:
            id = args[0]
            gfx_id = args[1]
            target_state = args[2]
            auto = args[3]
            possible_states = args[4]

            if not(isinstance(id, str)) or not(isinstance(gfx_id, int)) or not(self.isStateValid(target_state, possible_states)) or (auto not in [0, 1]):
                ErrorInvalidValue()
            else:
                self.id = id
                self.gfx_id = gfx_id
                self.target_state = target_state
                self.auto = auto
        else: ErrorInvalidConstructor()

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

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "undefined"
            self.gfx_id = -1
            self.state = -1
            self.state_list = []
        #alternative constructor (id, gfx_id, state, state_list)
        elif len(args) == 4:
            '''TODO: CHECK INSTANCES '''
            id = args[0]
            gfx_id = args[1]
            state = args[2]
            state_list = args[3]
        else: ErrorInvalidConstructor()

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
            ''' TODO: GFX TREATMENT '''
            #self.gfx_id = 100 + self.state_list.index(state)
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
    It has the following arguments:
        acceleration_y: acceleration in the y axis
        acceleration_x: acceleration in the x axis
    '''

    MAX_SPEED_X = 1
    MAX_SPEED_Y = 1
    INCREMENT = 0.05

    '''
    Constructors
    '''

    def __init__(self, *args):
        #default constructor
        if len(args) == 0:
            self.id = "player"
            self.gfx_id = 0
            self.state = "blink"
            '''TODO : STATE MUST BE AN ENUMERATION '''
            self.state_list = ["endmap", "walk", "fall", "jump", "fly", "climb", "die", "blink"]
            self.acceleration_x = 0
            self.velocity_x = 0.5
            self.acceleration_y = 0.01
            self.velocity_y = 0
            self.inventory = {"jetpack": 0, "gun": 0, "trophy": 0}
        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''

    ## Keys, in order: K_UP, K_LEFT, K_RIGHT, K_DOWN, K_LCTRL, K_RCTRL, K_LALT, K_RALT

    def input(self, key, action):
        if self.state in ["endmap", "die"]:
            return 0

        keydown = (action == 0)
        keyup = (action == 1)

        k_uparrow = (key == 0)
        k_leftarrow = (key == 1)
        k_rightarrow = (key == 2)
        k_downarrow = (key== 3)
        k_ctrl = (key == 4) or (key == 5)
        k_alt = (key == 6) or (key == 7)

        ''' TODO: ANIMATION (might need more ifs) '''
        ''' TODO: REFACTOR? '''

        if keyup:
            if (k_leftarrow):
                self.acceleration_x = 0

            if (k_rightarrow):
                self.acceleration_x = 0

        elif keydown:
            if k_leftarrow:
                self.acceleration_x = -1
                if (self.state == "climb"):
                    self.state = "fall"
                elif (self.state == "blink"):
                    self.state = "walk"
            if k_rightarrow:
                self.acceleration_x = 1
                if (self.state == "climb"):
                    self.state = "fall"
                elif (self.state == "blink"):
                    self.state = "walk"
            if k_uparrow and self.state in ["walk", "blink", "fly", "climb"]:
                self.changeVelocityY(- self.MAX_SPEED_Y)
                if self.state in ["walk", "blink"]:
                    self.state = "jump"
            if k_downarrow:
                print("velocidade Y: ", self.velocity_y)
                print("Aceleração Y: ", self.acceleration_y)
                print("velocidade X: ", self.velocity_x)
                print("Aceleração X: ", self.acceleration_x)
                print("Estado: ", self.state)
    #        if k_downarrow and self.state in ["fly", "climb"]:            // TIREI PORQUE ACHO QUE NÃO FAZ SENTIDO
    #            self.acceleration_y = self.MAX_SPEED_Y
            if k_ctrl and self.inventory["jetpack"]:
                if self.state == "fly":
                    self.state = "fall"
                else:
                    self.state = "fly"
            if k_alt and self.inventory["gun"]:
                return 1    #treat gunfire externally (because we need the map)
        return 0

    def updatePosition(self, player_x, player_y, level):

        if self.state == "walk":
            if level.checkPlayerCollision((player_x, player_y + 1)) != "BLOCK_COLLISION":
                self.state = "fall"

        player_newx = player_x + self.getVelocityX() * self.getAccelerationX()
        player_newy = player_y

        if (self.state == "jump" or self.state == "fall"):
            self.changeVelocityY(self.acceleration_y)
            player_newy = player_newy + self.getVelocityY()

        if level.checkPlayerCollision((player_newx, player_newy)) == "BLOCK_COLLISION":
            if level.checkPlayerCollision((player_newx, player_y)) != "BLOCK_COLLISION":
                if player_newy > player_y:  ## BATEU EM BAIXO
                    self.state = "walk"
                    self.setVelocityY(0)
                    player_newy = (player_newy//16) * 16
                else:  ## BATEU A CABEÇA
                    self.setVelocityY(0)
                    player_newy = player_y

            elif level.checkPlayerCollision((player_x, player_newy)) != "BLOCK_COLLISION":
                player_newx = player_x
            else:
                player_newx = player_x
                player_newy = player_y
                self.setVelocityY(0)
                self.state = "walk"

        return (player_newx, player_newy)




#    def resetPosTimer(self, timer):
        #if timer == 'x':
            #self.x_update_timer = self.MAX_SPEED_X
        #elif timer == 'y':
            #self.y_update_timer = self.MAX_SPEED_X

    #def decPosTimer(self, timer):
        #if timer == 'x':
            #self.x_update_timer -= abs(self.acceleration_x)
        #elif timer == 'y':
            #self.y_update_timer -= abs(self.acceleration_y)

    def setAccelerationX(self, acc):
        '''TODO: TEST INSTANCE'''
        self.acceleration_x = acc

    def setAccelerationY(self, acc):
        '''TODO: TEST INSTANCE'''
        self.acceleration_y = acc

    def setVelocityX(self, acc):
        '''TODO: TEST INSTANCE'''
        self.velocity_x = acc

    def setVelocityY(self, acc):
        '''TODO: TEST INSTANCE'''
        self.velocity_y = acc

    def changeVelocityX(self, inc):
        if inc == 0:
            self.decayVelocityX()
        else:
            self.velocity_x = self.velocity_x + inc
            if (self.velocity_x > self.MAX_SPEED_X):
                self.velocity_x = self.MAX_SPEED_X
            elif (self.velocity_x < - self.MAX_SPEED_X):
                self.velocity_x = - self.MAX_SPEED_X


    def changeVelocityY(self, inc):
        self.velocity_y = self.velocity_y + inc
        if (self.velocity_y > self.MAX_SPEED_Y):
            self.velocity_y = self.MAX_SPEED_Y
        elif (self.velocity_y < - self.MAX_SPEED_Y):
            self.velocity_y = - self.MAX_SPEED_Y

    def decayVelocityX(self): # SIMULA ATRITO
        if self.velocity_x > 0:
            self.velocity_x = self.velocity_x - 0.1
            if self.velocity_x < 0:
                self.velocity_x = 0

        elif self.velocity_x < 0:
            self.velocity_x = self.velocity_x + 0.1
            if self.velocity_x > 0:
                self.velocity_x = 0

    def incAccelerationY(self, acc):
        '''TODO: TEST INSTANCE'''
        self.acceleration_y += acc
        self.acceleration_y = round(self.acceleration_y, 2) #fix that fucking floating point problem

    def getAccelerationX(self):
        return self.acceleration_x

    def getAccelerationY(self):
        return self.acceleration_y

    #def getXUpdateTimer(self):
        #return self.x_update_timer

    #def getYUpdateTimer(self):
        #return self.y_update_timer

    def getVelocityX(self):
        return self.velocity_x

    def getVelocityY(self):
        return self.velocity_y

    def getMaxSpeedX(self):
        return self.MAX_SPEED_X

    def getMaxSpeedY(self):
        return self.MAX_SPEED_Y


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
