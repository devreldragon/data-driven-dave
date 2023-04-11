import newrelic.agent

import sys
from math import floor
from enum import Enum
from random import randint
import pygame

'''
Constants and enumerations
'''

TILE_SCALE_FACTOR = 3
WIDTH_OF_MAP_NODE = 16
HEIGHT_OF_MAP_NODE = 16
TOP_OVERLAY_POS = 12
BOTTOM_OVERLAY_POS = 166

ANIMATION_VELOCITY = 2

BOUNDARY_DISTANCE_TRIGGER = 32

SCREEN_WIDTH = 320 * TILE_SCALE_FACTOR
SCREEN_HEIGHT = 200 * TILE_SCALE_FACTOR

NUM_OF_LEVELS = 10

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
    
'''
Errors
'''

def ErrorInvalidValue():
    raise ValueError("Please enter a valid value.")

def ErrorInvalidConstructor():
    raise ValueError("The entered constructor is not valid.")
    
def ErrorMethodNotImplemented():
    raise ValueError("This method must be implemented by a child class.")
    
def ErrorSpawnerNotFound():
    raise ValueError("Specified spawner was not found.")

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
        font: pygame.font is the font used in the game
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
        self.font = pygame.font.SysFont("Consolas", 8 * TILE_SCALE_FACTOR)
        self.display = pygame.display.set_mode((width, height))
        self.display.fill((0, 0, 0))  
        
    '''
    Other methods
    '''
        
    def clearScreen(self):
        self.display.fill((0,0,0))
        
    def isXInScreen(self, x):
        return (x >= self.x_pos) and (x < self.x_pos + self.getWidthInTiles())

    @newrelic.agent.background_task()
    def printTile(self, x, y, tile_graphic):
        scaled_x = x * TILE_SCALE_FACTOR
        scaled_y = y * TILE_SCALE_FACTOR    

        self.display.blit(tile_graphic, (scaled_x, scaled_y))
 
    @newrelic.agent.background_task()
    def printMap(self, map, tileset):
        for y, row in enumerate(map.getNodeMatrix()):
            for x, col in enumerate(row):
                tile = map.getNode(x,y)
                absolute_y = y * HEIGHT_OF_MAP_NODE
                
                # won't print other tiles that aren't in the game screen (considering the current x position)
                if self.isXInScreen(x):
                    adjusted_x = x - self.x_pos                                     #print the tile accordingly to the screen shift
                    absolute_x = adjusted_x * WIDTH_OF_MAP_NODE                     #store the x pos in pixels
                    tile_graphic = tile.getGraphic(tileset)                         #get the tile graphic
                    self.printTile(absolute_x, absolute_y, tile_graphic)

    @newrelic.agent.background_task()
    def printPlayer(self, player, player_x, player_y, tileset):
        player_graphic = player.getGraphic(tileset) 
        player.copyDirectionToSprite()
            
        if (player.isSpriteFlipped()):
            player_graphic = pygame.transform.flip(player_graphic,1,0)
                
        self.printTile(player_x, player_y, player_graphic)
                    
    @newrelic.agent.background_task()
    def printTitlepicBorder(self, tileset):
        for x in range(0, 20):
            for y in range(0, 11):
                if (y < 4) or (x < 5) or (x > 14):
                    absolute_x = x * WIDTH_OF_MAP_NODE
                    absolute_y = y * HEIGHT_OF_MAP_NODE
                    self.printTile(absolute_x, absolute_y, Scenery().getGraphic(tileset))
                    
    @newrelic.agent.background_task()
    def moveScreenX(self, map, amount, tileset, ui_tileset, player, level_number):
        screen_shift = 0
        reached_level_left_boundary = (self.x_pos <= 0)
        reached_level_right_boundary = (self.x_pos + self.getWidthInTiles() >= map.getWidth())
        
        #going left
        while (screen_shift > amount) and not reached_level_left_boundary:
            self.printMap(map, tileset)
            self.printOverlays(ui_tileset)
            self.printUi(ui_tileset, player, level_number)
            
            pygame.display.flip()

            screen_shift -= self.SCREEN_SHIFTING_VELOCITY
            self.x_pos -= self.SCREEN_SHIFTING_VELOCITY 
            reached_level_left_boundary = (self.x_pos <= 0)

        #going right
        while (screen_shift < amount) and not reached_level_right_boundary:
            self.printMap(map, tileset)
            self.printOverlays(ui_tileset)
            self.printUi(ui_tileset, player, level_number)
            
            pygame.display.flip()
            
            screen_shift += self.SCREEN_SHIFTING_VELOCITY
            self.x_pos += self.SCREEN_SHIFTING_VELOCITY 
            reached_level_right_boundary = (self.x_pos + self.getWidthInTiles() >= map.getWidth())      
          
    '''
    UI Methods
    '''
        
    @newrelic.agent.background_task()
    def printOverlays(self, ui_tileset):
        top_overlay = Scenery("topoverlay", 0)
        bottom_overlay = Scenery("bottomoverlay", 0)
        self.printTile(0, 0, top_overlay.getGraphic(ui_tileset))
        self.printTile(0, BOTTOM_OVERLAY_POS, bottom_overlay.getGraphic(ui_tileset))
                    
    @newrelic.agent.background_task()
    def printText(self, text, x, y):
        graphic_text = self.font.render(text, 1, (255, 255, 255))

        scaled_x = x * TILE_SCALE_FACTOR
        scaled_y = y * TILE_SCALE_FACTOR
        
        self.display.blit(graphic_text, (scaled_x, scaled_y))
        
    @newrelic.agent.background_task()
    def printTextAlignedInCenter(self, text, y):
        graphic_text = self.font.render(text, 1, (255, 255, 255))
        graphic_text_width = graphic_text.get_rect().width
        
        scaled_x = self.width/2 - graphic_text_width/2
        scaled_y = y * TILE_SCALE_FACTOR
        
        self.display.blit(graphic_text, (scaled_x, scaled_y))      
     
    @newrelic.agent.background_task()
    def printUi(self, ui_tileset, player, level_number):
        self.updateUiScore(player.getScore(), ui_tileset)
        self.updateUiLevel(level_number, ui_tileset)
        self.updateUiDaves(player.getLives(), ui_tileset)

    @newrelic.agent.background_task()
    def updateUiScore(self, score, ui_tileset):
        #score text
        score_text = Scenery("scoretext", 0)
        self.printTile(0, 0, score_text.getGraphic(ui_tileset))
        
        #score amount
        numbers = Scenery("numbers", 0)
        leadingzeroes_score = str(score).zfill(5)
        for digit in range(5):
            numbers.setGfxId(int(leadingzeroes_score[digit]))            
            self.printTile(60 + 8 * digit, 0, numbers.getGraphic(ui_tileset))

    @newrelic.agent.background_task()
    def updateUiLevel(self, level_number, ui_tileset):
        #level text
        level_text = Scenery("leveltext", 0)
        self.printTile(120, 0, level_text.getGraphic(ui_tileset))
        
        #level number
        numbers = Scenery("numbers", 0)
        leadingzeroes_level = str(level_number).zfill(2)
        for digit in range(2):
            numbers.setGfxId(int(leadingzeroes_level[digit]))
            self.printTile(170 + 8 * digit, 0, numbers.getGraphic(ui_tileset))
            
    @newrelic.agent.background_task()
    def updateUiDaves(self, life_amount, ui_tileset):
        #daves text
        daves_text = Scenery("davestext", 0)
        self.printTile(210, 0, daves_text.getGraphic(ui_tileset))
        
        #life amount
        dave_icon = Scenery("daveicon", 0)
        for index in range(life_amount):
            self.printTile(270 + 14 * index, 0, dave_icon.getGraphic(ui_tileset))
            
    @newrelic.agent.background_task()
    def updateUiTrophy(self, ui_tileset):
        text = Scenery("gothrudoortext", 0)
        self.printTile(70, 184, text.getGraphic(ui_tileset))

    @newrelic.agent.background_task()
    def updateUiGun(self, ui_tileset):
        gun_icon = Scenery("gunicon", 0)
        gun_text = Scenery("guntext", 0)
        self.printTile(285, 170, gun_icon.getGraphic(ui_tileset))
        self.printTile(240, 170, gun_text.getGraphic(ui_tileset))

    @newrelic.agent.background_task()
    def updateUiJetpack(self, ui_tileset, gas_amount):
        jetpack_text = Scenery("jetpacktext", 0)
        jetpack_meter = Scenery("jetpackmeter", 0)
        jetpack_bar = Scenery("jetpackbar", 0)
        
        self.printTile(0, 170, jetpack_text.getGraphic(ui_tileset))
        self.printTile(70, 170, jetpack_meter.getGraphic(ui_tileset))
        
        for index in range(floor(gas_amount * 61)):
            self.printTile(73 + 2 * index, 173, jetpack_bar.getGraphic(ui_tileset))
            
    @newrelic.agent.background_task()
    def clearBottomUi(self, ui_tileset):
        black_tile = Scenery("blacktile", 0)
        self.printTile(0, 170, black_tile.getGraphic(ui_tileset))            
        
            
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
            
    def setXPosition(self, x_position, level_width):
        if not isinstance(x_position, int):
            ErrorInvalidValue()
        elif x_position < 0:
            self.x_pos = 0;
        elif x_position > level_width - self.getWidthInTiles():
            self.x_pos = level_width - self.getWidthInTiles()
        else:
            self.x_pos = x_position

            
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
            self.buildMapMatrix()
        #alternative constructor 1 (level_number)
        elif(len(args) == 1):
            if not self.validConstructorArgs(*args):
                ErrorInvalidValue()
            
            self.buildLevel(args[0])            
        #alternative constructor 2 (height, width)
        elif(len(args) == 2):
            if not self.validConstructorArgs(*args):
                ErrorInvalidValue()
            
            self.height = args[0]
            self.width = args[1]
            self.buildMapMatrix()
        else: ErrorInvalidConstructor()

    def buildMapMatrix(self):
        self.node_matrix = [[Tile() for i in range(self.width)] for j in range(self.height)]

    def validConstructorArgs(self, *args):
        if len(args) == 1:
            level_number = args[0]
            
            return (isinstance(level_number, str)) or (isinstance(level_number, int) and level_number >= 1 and level_number <= NUM_OF_LEVELS)
        elif len(args) == 2:
            height = args[0]
            width = args[1]
            
            return (isinstance(height, int) and isinstance(width, int) and height >= 0 and width >= 0)            
        
    def validateCoordinates(self, x, y):
        return (isinstance(x, int) and isinstance(y, int) and x >= 0 and y >= 0 and x < self.width and y < self.height)
        
    def setNodeTile(self, x, y, tile):
        if self.validateCoordinates(x, y) and isinstance(tile, Tile):
            self.node_matrix[y][x] = tile
        else: ErrorInvalidValue()
        
    def clearNode(self, x, y):
        self.setNodeTile(x, y, Scenery())

    def getNode(self, x, y):
        if self.validateCoordinates(x, y):
            return self.node_matrix[y][x]
        else: ErrorInvalidValue()

    def getPlayerSpawnerPosition(self, spawner_id):
        for y, line in enumerate(self.node_matrix):
            for x, col in enumerate(line):
                if self.node_matrix[y][x].getId() == "player_spawner" and self.node_matrix[y][x].getSpawnerId() == spawner_id:
                    return (x, y)
        ErrorSpawnerNotFound()
                    
    def getCollisionType(self, x, y):
        #out of the map
        if not self.validateCoordinates(x, y):
            return COLLISION.NONE
    
        solid = isinstance(self.node_matrix[y][x], Solid)
        item = isinstance(self.node_matrix[y][x], Item)
        intscen = isinstance(self.node_matrix[y][x], InteractiveScenery)
        enemy = isinstance(self.node_matrix[y][x], Enemy)

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

    @newrelic.agent.background_task()
    def checkPlayerCollision(self, player_x, player_y, player_width, player_height, solid_only=False):
        TOLERANCE_VALUE = 3 #the dave can walk a little bit "into" the blocks
        
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

    def isPlayerCollidingWithSolid(self, player_x, player_y, player_width=20, player_height=16):
        return (self.checkPlayerCollision(player_x, player_y, player_width, player_height, True)[0] == COLLISION.SOLID)

    @newrelic.agent.background_task()
    def spawnFriendlyFire(self, direction):
        if (direction == DIRECTION.RIGHT) or (direction == DIRECTION.IDLE):
            shot = Shot()
        elif (direction == DIRECTION.LEFT): 
            shot = Shot("bullet", 1, DIRECTION.LEFT)
        else: ErrorInvalidValue()
        
        return shot
        
    @newrelic.agent.background_task()
    def checkShotCollision(self, shot_x, shot_y, shot_width=12, shot_height=3):    
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
    Level construction
    '''
    
    @newrelic.agent.background_task()
    def buildLevel(self, level_number):
        #open the level in the txt
        textmap = open("levels/" + str(level_number) + ".txt", 'r')

        #get height (must reset offset)
        self.height = len(textmap.readlines())
        textmap.seek(0)

        #get width (must reset offset)
        self.width = int(len(textmap.readline()) / 3)
        textmap.seek(0)
        
        #allocate matrix
        self.buildMapMatrix()

        #for each node, set it accordingly
        for y, line in enumerate(textmap.readlines()):
            x = 0
            while (x < self.width):
                text_tile = line[(3*x):(3*x + 2)]
                tile_type = self.tileFromText(text_tile)
                self.setNodeTile(x, y, tile_type)
                x += 1

    @newrelic.agent.background_task()
    def initPlayerPositions(self, spawner_id, player): 
        player.setCurrentState(STATE.BLINK)
        player.setDirectionX(DIRECTION.IDLE)
        playerPosition = self.getPlayerSpawnerPosition(spawner_id)
        
        #if the spawner isn't present, raise error
        if playerPosition == (-1, -1):
            ErrorSpawnerNotFound()
        
        player_position_x = WIDTH_OF_MAP_NODE * playerPosition[0]
        player_position_y = HEIGHT_OF_MAP_NODE * playerPosition[1]
        
        return (player_position_x, player_position_y)
        
    @newrelic.agent.background_task()
    def tileFromText(self, text_tile):
        #if the tile has an index, store it
        try:
            gfx_id = int(text_tile[1])
        except:
            gfx_id = 0

        if text_tile == "DO":
            return InteractiveScenery()
        elif text_tile == "FR":
            return InteractiveScenery("fire", randint(0,3), INTSCENERYTYPE.HAZARD)
        elif text_tile == "WA":
            return InteractiveScenery("water", randint(0,3), INTSCENERYTYPE.HAZARD)
        elif text_tile == "TN":
            return InteractiveScenery("tentacles", randint(0,3), INTSCENERYTYPE.HAZARD)
        elif text_tile == "TR":
            return Equipment("trophy", 0, 1000)
        elif text_tile == "GU":
            return Equipment("gun", 0, 0)
        elif text_tile == "JE":
            return Equipment("jetpack", 0, 0)
        elif text_tile[0] == "p":
            return PlayerSpawner("player_spawner", -1, gfx_id)
        elif text_tile[0] == 'B':
            return Solid("solid", gfx_id)
        elif text_tile[0] == 'T':
            return Solid("tunnel", gfx_id)
        elif text_tile[0] == 'S':
            return Scenery("scenery", gfx_id)
        elif text_tile[0] == 'M':
            return Scenery("moonstars", gfx_id)
        elif text_tile[0] == 'E':
            return InteractiveScenery("tree", gfx_id, INTSCENERYTYPE.TREE)
        elif text_tile[0] == 'I':
            scores = [50, 100, 150, 200, 300, 500]
            return Item("items", gfx_id, scores[1])
        elif text_tile[0] == 'P':
            return Solid("pinkpipe", gfx_id)
        else:
            return Scenery()

        
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
            self.id = "undefined"
            self.gfx_id = -1
        else: ErrorInvalidConstructor()
        
    '''
    Other methods
    '''
           
    def validConstructorArgs(self, *args):
        # This method must be implemented in the children classes
        ErrorMethodNotImplemented()
        
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
            return pygame.Surface((16 * TILE_SCALE_FACTOR, 16 * TILE_SCALE_FACTOR))

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
        ErrorMethodNotImplemented()

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
    Scenery represents a scenery tile in the game (just background)
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
        
        return (isinstance(id, str) and isinstance(gfx_id, int) and gfx_id >= -1)
        
    '''
    Getters and setters
    '''
    
    def setId(self, id):
        if isinstance(id, str):
            self.id = id
        else: ErrorInvalidValue()
           

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
        
        return (isinstance(id, str) and isinstance(gfx_id, int) and id in ["solid", "pinkpipe", "tunnel"] and gfx_id >= -1)   
        
    '''
    Getters and setters
    '''
    
    def setId(self, id):
        if isinstance(id, str) and id in ["solid", "pinkpipe", "tunnel"] :
            self.id = id
        else: ErrorInvalidValue()


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
        id = args[0]
        gfx_id = args[1]
        score = args[2]
        
        return (isinstance(score, int) and score >= 0 and isinstance(id, str) and isinstance(gfx_id, int) and id in ["items", "trophy", "jetpack", "gun"] and gfx_id >= -1)
    
    '''
    Getters and setters
    '''
    
    def setId(self, id):
        if isinstance(id, str) and id in ["items", "trophy", "jetpack", "gun"]:
            self.id = id
        else: ErrorInvalidValue()    
    
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
        id = args[0]
        gfx_id = args[1]
        type = args[2]
        
        return (isinstance(type, INTSCENERYTYPE) and isinstance(id, str) and isinstance(gfx_id, int) and id in ["tree", "door", "tentacles", "fire", "water"] and gfx_id >= -1)

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
    
    def setId(self, id):
        if isinstance(id, str) and id in ["tree", "door", "tentacles", "fire", "water"]:
            self.id = id
        else: ErrorInvalidValue()

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
    
    def setId(self, id):
        if isinstance(id, str) and id == "player_spawner":
            self.id = id
        else: ErrorInvalidValue()
       
    def getSpawnerId(self):
        return self.spawner_id
        
    def setSpawnerId(self, id):
        if not isinstance(id, int) or id < 0:
            ErrorInvalidValue()
        else:
            self.spawner_id = id

                
class AnimatedTile(Tile):
    '''
    AnimatedTile represents an animated tile in the game.
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
            self.id = "explosion"
            self.gfx_id = 0
            self.anim_timer = self.ANIM_TIMER_MAX
        #alternative constructor (id, gfx_id)
        elif len(args) == 2:
            if not self.validConstructorArgs(*args):
                ErrorInvalidValue()
                        
            self.id = args[0]
            self.gfx_id = args[1]
            self.anim_timer = self.ANIM_TIMER_MAX
        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''

    def validConstructorArgs(self, *args):
        id = args[0]
        gfx_id = args[1]
        
        return (isinstance(id, str) and isinstance(gfx_id, int) and gfx_id >= -1)
    
    def getGraphic(self, tileset):
        self.anim_timer -= ANIMATION_VELOCITY
        
        if (self.anim_timer == 0):
            self.anim_timer = self.ANIM_TIMER_MAX
            
            tile_frames = tileset[self.id]
            number_of_tile_frames = int(tile_frames[0].get_rect().size[0]/tile_frames[2])
            
            if self.gfx_id == number_of_tile_frames-1:
                self.gfx_id = 0 
            else: self.gfx_id += 1

        #call superclass method
        return super(AnimatedTile, self).getGraphic(tileset)

    '''
    Getters and setters
    '''
    
    def setId(self, id):
        if isinstance(id, str):
            self.id = id
        else: ErrorInvalidValue()        
        
        
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
        id = args[0]
        gfx_id = args[1]
        cur_state = args[2]
        
        return (isinstance(cur_state, STATE) and isinstance(id, str) and isinstance(gfx_id, int) and id in ["player", "ball", "cloud", "disc", "baton", "pinkenemy", "redenemy", "spider", "ufo"] and gfx_id >= -1) 
    
    '''
    Getters and setters
    '''
    
    def setId(self, id):
        if isinstance(id, str) and id in ["player", "ball", "cloud", "disc", "baton", "pinkenemy", "redenemy", "spider", "ufo"]:
            self.id = id
        else: ErrorInvalidValue()

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
        velocity_y : float represents the velocity and direction in y axis (module + value)
        velocity_x : float represents the velocity in the x axis
        direction_x : enumeration represents the direction in the x axis
        sprite_direction : enumeration represents the direction the sprite is facing (used for the gun)
        inventory : dictionary contains the inventory of the player
        score : integer represents the score of the player
        lives : integer represents the lives of the player
        animator : PlayerAnimator contains the class used to animate the player
    '''

    '''
    Constants
    '''

    MAX_SPEED_X = 0.6 
    MAX_SPEED_Y = 0.6
    X_SPEED_FACTOR = 0.75   #factor to be used when not falling (x speed only hits its maximum when falling)
    
    JUMP_SPEED = 0.8
    GRAVITY = 0.01          #gravity acceleration
    
    MAX_LIVES = 5

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
            self.sprite_direction = DIRECTION.IDLE
            self.inventory = {"jetpack": 0, "gun": 0, "trophy": 0, "tree": 0}
            self.score = 0
            self.lives = 3
            self.animator = PlayerAnimator()
        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''

    def getGraphic(self, tileset):
        return Tile.getGraphic(self, tileset)
    
    ## Input : START
    def movementInput(self, pressed_keys):
        #ignore states that don't interact with the level
        if self.cur_state in [STATE.ENDMAP, STATE.DESTROY]:
            return 0

        # readbility purposes
        k_uparrow = (pressed_keys[0])
        k_leftarrow = (pressed_keys[1])
        k_rightarrow = (pressed_keys[2])
        k_downarrow = (pressed_keys[3])

        if k_uparrow:
            # climb (not climbing yet)
            if self.cur_state in [STATE.BLINK, STATE.WALK] and self.inventory["tree"] == 1:
                self.setCurrentState(STATE.CLIMB)
                self.velocity_y = - self.MAX_SPEED_Y
                self.updateAnimator()
            # jump
            elif self.cur_state in [STATE.BLINK, STATE.WALK]:
                self.setCurrentState(STATE.JUMP)
                self.velocity_y = - self.JUMP_SPEED
            # climb (already climbing)
            elif self.cur_state in [STATE.FLY, STATE.CLIMB]:
                self.velocity_y = - self.MAX_SPEED_Y
                # jump off tree (by the top)
                if self.cur_state == STATE.CLIMB and self.inventory["tree"] == 0:
                    self.setCurrentState(STATE.JUMP)
                    
        if k_leftarrow or k_rightarrow:
            # set the direction accordingly
            self.direction_x = DIRECTION.LEFT if k_leftarrow else DIRECTION.RIGHT

            # move
            if self.cur_state in [STATE.BLINK, STATE.WALK, STATE.JUMP, STATE.CLIMB, STATE.FLY]:
                self.velocity_x = self.MAX_SPEED_X * self.X_SPEED_FACTOR
            # fall (can be uncontrolled)
            elif self.cur_state == STATE.FALL:
                self.velocity_x = self.MAX_SPEED_X #when falling, velocity increases to the max
                
            # set walking state if in initial state
            if self.cur_state == STATE.BLINK:
                self.setCurrentState(STATE.WALK)
            # fall off tree (by the sides)
            elif self.cur_state == STATE.CLIMB and self.inventory["tree"] == 0:
                self.setCurrentState(STATE.FALL)
                self.velocity_y = self.MAX_SPEED_Y
                
        if k_downarrow:
            # only works in flying and climbing state
            if self.cur_state in [STATE.CLIMB, STATE.FLY]:
                self.velocity_y = self.MAX_SPEED_Y
                
                # fall off tree (by the bottom)
                if self.cur_state == STATE.CLIMB and self.inventory["tree"] == 0:
                    self.setCurrentState(STATE.FALL)
                    self.velocity_y = self.MAX_SPEED_Y                    

    @newrelic.agent.background_task()
    def inventoryInput(self, key):
        # ignore states that don't interact with the level
        if self.cur_state in [STATE.ENDMAP, STATE.DESTROY]:
            return -1

        k_ctrl = (key == 0) or (key == 1)
        k_alt = (key == 2) or (key == 3)

        # start jetpack
        if k_ctrl and self.inventory["jetpack"]:
            if self.cur_state == STATE.FLY:
                self.setFallingState()
            else:
                self.setCurrentState(STATE.FLY)
                self.velocity_x = 0
                self.velocity_y = 0
                self.updateAnimator()
                
        # fire gun
        if k_alt and self.inventory["gun"]:
            return 1    # treat gunfire externally (because we need the map)
        return 0
    ## Input : END
    
    ## Motion : START
    def addVelocityY(self, inc):
        self.velocity_y = self.velocity_y + inc
        #test limits
        if (self.velocity_y > self.MAX_SPEED_Y):
            self.velocity_y = self.MAX_SPEED_Y

    def clearXMovement(self):
        self.velocity_x = 0
        self.direction_x = DIRECTION.IDLE
        
    def applyGravityOnJump(self):
        # Jumping is basically a velocity spike with a gravity based decay. This is basically calculating the decay at each frame.
        self.addVelocityY(self.GRAVITY) 
        
        if self.velocity_y == self.MAX_SPEED_Y:
            self.setFallingState()      
        
    def setFallingState(self):
        self.setCurrentState(STATE.FALL)
        self.velocity_x = self.MAX_SPEED_X #when falling, velocity increases to the max
        self.velocity_y = self.MAX_SPEED_Y    
        
    def setWalkingState(self):
        self.setCurrentState(STATE.WALK)
        self.velocity_x = self.MAX_SPEED_X * self.X_SPEED_FACTOR
        self.velocity_y = 0
        self.direction_x = DIRECTION.IDLE
        self.updateAnimator()
        
    def movePlayerRight(self, player_x):
        return player_x + self.MAX_SPEED_X * self.X_SPEED_FACTOR

    def resetPosAndState(self):
        if self.lives < 0:
            return -1
        
        self.setCurrentState(STATE.BLINK)
        self.gfxId = 0
        self.velocity_y = 0
        self.velocity_x = 0
        self.direction_x = DIRECTION.IDLE 
        self.animator.resetBlinker()    
    ## Motion : END

    ## Sprite : START
    def copyDirectionToSprite(self):
        if self.direction_x in [DIRECTION.LEFT, DIRECTION.RIGHT]:
            self.sprite_direction = self.direction_x
            
    def isSpriteFlipped(self):
        if self.sprite_direction == DIRECTION.RIGHT:
            return True
        else: return False
    ## Sprite : END
    
    ## Inventory : START
    def decJetpackGasoline(self):
        self.inventory["jetpack"] -= 0.001
        #fixes floating point problems
        if self.inventory["jetpack"] < 0:
            self.inventory["jetpack"] = 0  

    def takeLife(self):
        self.lives -= 1

    def giveLife(self):
        if self.lives < self.MAX_LIVES:
            self.lives += 1
            
    def clearInventory(self):
        self.inventory["trophy"] = 0
        self.inventory["gun"] = 0
        self.inventory["jetpack"] = 0
        
    ## Inventory : END
            
    ## Collision : START
    def processSolidCollisionY(self, current_y, target_y):
        # landed
        if self.cur_state in [STATE.JUMP, STATE.FALL] and target_y > current_y:
            self.setWalkingState()
        # was jumping and hit ceiling
        elif self.cur_state == STATE.JUMP:
            self.setFallingState()

    def collectItem(self, item_pos, level):
        x = item_pos[0]
        y = item_pos[1]

        item = level.getNode(x, y)
        
        #if the item is an equipment, add it to the inventory
        if isinstance(item, Equipment):
            self.inventory[item.getId()] = 1
            
        #increment score
        self.score += item.getScore()
        
        #if the player got to a certain score, give one life to him
        if self.score % 5000 == 0:
            self.giveLife()

        level.clearNode(x, y)

    def interactWithScenery(self, element_pos, level):
        x = element_pos[0]
        y = element_pos[1]

        element = level.getNode(x, y)
        #player has trophy and reached the door
        if element.getType() == INTSCENERYTYPE.GOAL and self.inventory["trophy"] == 1:
            self.setCurrentState(STATE.ENDMAP)
        #player collided with a hazard
        elif element.getType() == INTSCENERYTYPE.HAZARD:
            self.setCurrentState(STATE.DESTROY)
        #player has contact with a tree
        elif element.getType() == INTSCENERYTYPE.TREE:
            self.inventory["tree"] = 1

    def processEnemyCollision(self, enemy_pos, level):
        ''' TODO : ENEMY COLLISION '''
        pass
    
    def processCollisionsInCurrentPosition(self, player_x, player_y, level):
        #reset tree inventory in case player leaves tree object
        self.inventory["tree"] = 0
        
        collision = level.checkPlayerCollision(player_x, player_y, 20, 16)
        collision_type = collision[0]
        collider_pos = collision[1]

        # Collect an item if there is one
        if collision_type == COLLISION.ITEM:
            self.collectItem(collider_pos, level)
        # Interact with scenery if one
        elif collision_type == COLLISION.INTSCEN:
            self.interactWithScenery(collider_pos, level)
        # Collision with an enemy
        elif collision_type == COLLISION.ENEMY:
            self.processEnemyCollision(collider_pos, level)       
    ## Collision : END
    
    ## Update player position and process surroundings
    def updatePosition(self, player_x, player_y, level, screen_max_height):  
        # First, check collisions in the current position (without moving)
        self.processCollisionsInCurrentPosition(player_x, player_y, level)
        
        # Checks if player is getting to a bonus room
        if (player_x < 0 or player_x > level.getWidth() * 16) and (player_y > screen_max_height/4):
            self.setCurrentState(STATE.ENDMAP)
            return (-2, -2)
        
        # Checks if the player walked into a pit
        walked_into_pit = (not level.isPlayerCollidingWithSolid(player_x, player_y + 1))
        if self.cur_state == STATE.WALK and walked_into_pit:
            self.setFallingState()

        ## Move X: START
        player_newx = player_x + self.velocity_x * self.direction_x.value                   # Tries to walk to the direction the player's going
        solid_collision = level.isPlayerCollidingWithSolid(player_newx, player_y)

        if solid_collision:                                                                 # If a collision occurs,
            player_newx = player_x                                                          # undo the movement
            if self.cur_state == STATE.FALL:                                                # If player's falling and released movement keys,
                self.clearXMovement()                                                       # stop the uncontrolled fall
        ## Move X: END

        ## Move Y: START
        player_newy = player_y + self.velocity_y

        # Check for solid collisions
        solid_collision = level.isPlayerCollidingWithSolid(player_newx, player_newy)

        if self.cur_state != STATE.DESTROY and solid_collision:
            self.processSolidCollisionY(player_y, player_newy)
            player_newy = player_y

        # If jumping, gravity is acting upon the player
        if self.cur_state == STATE.JUMP:
            self.applyGravityOnJump()
            
        if player_newy >= screen_max_height:
            player_newy = 0
        ## Move Y: END

        ## Jetpack gas: START
        if (self.cur_state == STATE.FLY) and self.inventory["jetpack"] > 0:
            self.decJetpackGasoline()
        elif (self.cur_state == STATE.FLY) and self.inventory["jetpack"] == 0:
            self.setFallingState()
        ## Jetpack gas: END       
        
        ## Process animation: START
        if (player_x != player_newx or player_y != player_newy) and self.cur_state != STATE.ENDMAP:          # If the player moved, updates the animation
            self.updateAnimator()
        elif self.cur_state == STATE.BLINK:
            self.gfx_id = self.animator.blink()
        ## Process animation: END
        
        return (player_newx, player_newy)
        
    ## Animation : START
    def updateAnimator(self):
        self.gfx_id = self.animator.update(self.cur_state)
    ## Animation : END
    
    '''
    Getters and setters
    '''

    def setCurrentState(self, newstate):
        if isinstance(newstate, STATE):
            self.cur_state = newstate
            self.animator.resetAnimation()
        else: ErrorInvalidValue()
    
    def setVelocityY(self, vel):
        if isinstance(vel, float) or True:
            self.velocity_y = vel
        else: ErrorInvalidValue()
    
    def setVelocityX(self, vel):
        if isinstance(vel, float) or True:
            self.velocity_x = vel
        else: ErrorInvalidValue()

    def setDirectionX(self, direction):
        if isinstance(direction, DIRECTION):
            self.direction_x = direction
        else: ErrorInvalidValue()
        
    def setSpriteDirection(self, direction):
        if isinstance(direction, DIRECTION):
            self.sprite_direction = direction
        else: ErrorInvalidValue()

    def setScore(self, score):
        if isinstance(score, int) and score >= 0:
            self.score = score
        else: ErrorInvalidValue()
        
    def setLives(self, lives):
        if isinstance(lives, int) and lives >= 0 and lives <= self.MAX_LIVES:
            self.lives = lives
        else: ErrorInvalidValue()
        
    def getVelocityY(self):
        return self.velocity_y        

    def getVelocityX(self):
        return self.velocity_x
        
    def getDirectionX(self):
        return self.direction_x
        
    def getSpriteDirection(self):
        return self.sprite_direction

    def getScore(self):
        return self.score
        
    def getLives(self):
        return self.lives

        
class PlayerAnimator(object):
    '''
    PlayerAnimator is a class used to implement the animation of the player
    It has the following arguments:
        animation_index : integer used to index the animation list of the corresponding state
        animation_counter : integer counter that ticks until the next frame of animation should be displayed
        blinking_timer : integer counter that represents the frequency of the blinking of the player
        animation_index_list : Dict of lists that specifies the index (displacement) of each animation frame based on the player tile. Indexed by the name of the STATE.
    '''
    
    '''
    Constants
    '''
    
    ANIMATION_COUNTER_MAX = 20
    BLINKING_SPEED = 2
    
    '''
    Constructors
    '''
    
    def __init__(self, *args):
        if len(args) == 0:
            self.animation_index = 0
            self.animation_counter = 0
            self.blinking_timer = self.BLINKING_SPEED
            self.animation_index_list = {STATE.WALK : [1, 2, 3, 2],
                                            STATE.BLINK : [0, -1],
                                            STATE.FALL : [12],
                                            STATE.JUMP : [12],
                                            STATE.CLIMB : [15, 16, 17],
                                            STATE.FLY : [24, 25, 26],
                                            STATE.DESTROY : [-1]}
        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''
    
    def resetAnimation(self):
        self.animation_index = 0
        self.animation_counter = 0
    
    def update(self, current_state):
        # Rotate the animation counter and set the new gfx index
        if self.animation_counter < self.ANIMATION_COUNTER_MAX:       # Only updates if it's time to update (the counter reached its maximum)
            self.animation_counter = self.animation_counter + 1
        else:
            self.animation_counter = 0
            if self.animation_index < len(self.animation_index_list[current_state]):           # Rotates the number that indexes the list of frames of that STATE.
                self.animation_index = self.animation_index + 1                                         # Basically means that the animation frames will alternate in the list's order.
            if self.animation_index == len(self.animation_index_list[current_state]):
                self.animation_index = 0

        result_gfx = self.animation_index_list[current_state][self.animation_index]
        return result_gfx
        
    def blink(self):
        self.blinking_timer -= 1

        if self.blinking_timer == 0:
            self.resetBlinker()
            
        return self.update(STATE.BLINK)
    
    def resetBlinker(self):
        self.blinking_timer = self.BLINKING_SPEED
    
    '''
    Getters and setters
    
    No getters and setters are used as the class values are used only internally
    '''
            

class Shot(Tile):
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
            if not self.validConstructorArgs(*args):
                ErrorInvalidValue()           
            
            self.id = args[0]
            self.gfx_id = args[1]
            self.direction = args[2]
        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''
        
    def validConstructorArgs(self, *args):
        id = args[0]
        gfx_id = args[1]
        direction = args[2]
          
        return (isinstance(direction, DIRECTION) and direction in [DIRECTION.RIGHT, DIRECTION.LEFT] and isinstance(id, str) and isinstance(gfx_id, int) and gfx_id >= -1 and id in ["bullet", "enemybullet"])
    
    def updatePosition(self, current_x, current_y, level):
        new_x = current_x + self.direction.value * self.MAX_SPEED_X
        
        collision = level.checkShotCollision(current_x, current_y)
        collision_type = collision[0]
        collider_pos = collision[1]
        
        if (collision_type == COLLISION.ENEMY):
            ''' TODO: KILL ENEMY '''
            return -1
        elif (collision_type == COLLISION.SOLID):
            return -1
            
        return new_x
    
    '''
    Getters and setters
    '''
    
    def setId(self, id):
        if isinstance(id, str) and id in ["bullet", "enemybullet"]:
            self.id = id
        else: ErrorInvalidValue()
    
    def setDirection(self, dir):
        if isinstance(dir, DIRECTION) and dir in [DIRECTION.LEFT, DIRECTION.RIGHT]:
            self.dir = dir
        else: ErrorInvalidValue()
        
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
            self.cur_state = STATE.IDLE
            self.shot_frequency = 2
            self.shot_chance = 0.3
            self.speed = 1
            self.movement_type = 1
        #alternative constructor (id, gfx_id, cur_state, shot_freq, shot_chance, speed, mov_type)
        elif len(args) == 7:
            id, gfx_id, state, state_list, shot_freq, shot_chance, speed, mov_type = args
            ''' TODO : IMPLEMENT THIS '''
        else: ErrorInvalidConstructor()

    '''
    Other methods
    '''

    '''
    Getters and setters
    '''
