from classes import *
from os import listdir
from os.path import isfile, join
import pygame

'''
Constants
'''

BOUNDARY = 25
SCREEN_WIDTH_TILES = 20
SCREEN_WIDTH = 320

'''
Levels
'''

def BuildLevel(level_number):
    textmap = open("levels/" + str(level_number) + ".txt", 'r')
    
    height = len(textmap.readlines())
    textmap.seek(0)
    width = int(len(textmap.readline()) / 3)
    textmap.seek(0)
    Level = Map(height, width)
    
    for y, line in enumerate(textmap.readlines()):
        x = 0
        while (x < width):
            text_tile = line[(3*x):(3*x + 2)]
            tile_type = tileFromText(text_tile)
            Level.setNodeTile(x, y, tile_type)
            x += 1
            
    return Level       
    
    
def tileFromText(text_tile):
    try:
        gfx_id = int(text_tile[1])
    except:
        gfx_id = 0

    if text_tile == "DO":
        return InteractiveScenery()
    elif text_tile == "FR":
        return InteractiveScenery("fire", 0, InteractiveScenery.TYPE.HAZARD, 1)
    elif text_tile == "WA":
        return InteractiveScenery("water", 0, InteractiveScenery.TYPE.HAZARD, 1)
    elif text_tile == "TN":
        return InteractiveScenery("tentacles", 0, InteractiveScenery.TYPE.HAZARD, 1)
    elif text_tile == "TR":
        return Equipment("trophy", 0, 1000, "trophy") 
    elif text_tile == "GU":
        return Equipment("gun", 0, 0, "gun")
    elif text_tile == "JE":
        return Equipment("jetpack", 0, 0, "jetpack")
    elif text_tile == "LO":
        return InteractiveScenery("treelog", 0, InteractiveScenery.TYPE.TREE, 0)
    elif text_tile == "pl":
        return Player()
    elif text_tile[0] == 'B':
        return Solid("solid", gfx_id)
    elif text_tile[0] == 'T':
        return Solid("tunnel", gfx_id)
    elif text_tile[0] == 'S':
        return Tile("scenery", gfx_id)
    elif text_tile[0] == 'M':
        return Tile("moonstars", gfx_id)
    elif text_tile[0] == 'E':
        return Tile("tree", gfx_id)
    elif text_tile[0] == 'I':
        scores = [50, 100, 150, 200, 300, 500]
        return Item("items", gfx_id, scores[1])
    elif text_tile[0] == 'P':
        return Solid("pinkpipe", gfx_id)
    else:
        return Tile("scenery", 0)
    
    
'''
Engine
'''
    
''' TODO: REORGANIZE/REORDER FUNCTIONS '''

#crop an image, looking for the right gfx within the set
def getBlockInImage(image, index):
    '''TODO: NOT ALL IMAGES ARE 16X16'''
    SIZE = 16
    NUML = 8 # 8 sprites per line
    indexw = index % NUML # modulus operator
    indexh = index // NUML
    rect = (indexw*SIZE, indexh*SIZE, SIZE, SIZE)
    block_image =  pygame.transform.scale(image.subsurface(rect),(SIZE*SCALEFACTOR,SIZE*SCALEFACTOR))
    return block_image

def getBlockInImageDiffSize(image,index,sizex,sizey):
    '''TODO: NOT ALL IMAGES ARE 16X16'''
    NUML = 10 # 8 sprites per line
    indexw = index % NUML # modulus operator
    indexh = index // NUML
    rect = (indexw*sizex, indexh*sizey, sizex, sizey)
    block_image =  pygame.transform.scale(image.subsurface(rect),(sizex*SCALEFACTOR,sizey*SCALEFACTOR))
    return block_image    
    
#truncate filename removing its size description
def fileNameTruncate(name):
    newname = ""
    for ch in name:
        if ch.isalpha():
            newname += ch
        else:
            return newname

#returns dictionary
def load_game_tiles():
    tilefiles = [file for file in listdir("tiles/game/") if isfile(join("tiles/game/", file))] #load all the image files within the directory

    tile_table = {} #init dictionary

    for savedfile in tilefiles:
        image = pygame.image.load("tiles/game/" + savedfile).convert_alpha()
        ''' TODO: CHECK IF THESE PARAMETERS HAVE ANY USE '''
        image_width, image_height = image.get_size()

        tile_table[fileNameTruncate(savedfile)] = image

    return tile_table

def print_ui_initial(ui_tileset,game_display,player,level_number):
    #print("Printing initial UI")

    #score text
    game_display.blit(getBlockInImageDiffSize(ui_tileset["scoretext"], 0, 54,11), (0,0))
    leadingzeroes_score = str(player.score).zfill(5)
    for index in range(5):
        current_number = int(leadingzeroes_score[index] )
        game_display.blit(getBlockInImageDiffSize(ui_tileset["numbers"], current_number, 8,11), (60*SCALEFACTOR+8*index*SCALEFACTOR,0))
    
    #level text
    game_display.blit(getBlockInImageDiffSize(ui_tileset["leveltext"], 0, 45,11), (120*SCALEFACTOR,0))
    leadingzeroes_level = str(level_number).zfill(2)
    for index in range(2):
        current_level = int(leadingzeroes_level[index] )
        game_display.blit(getBlockInImageDiffSize(ui_tileset["numbers"], current_level, 8,11), (170*SCALEFACTOR+8*index*SCALEFACTOR,0))
    
    #daves text
    game_display.blit(getBlockInImageDiffSize(ui_tileset["davestext"], 0, 50,11), (210*SCALEFACTOR,0))
    for index in range(player.lifes):
        game_display.blit(getBlockInImageDiffSize(ui_tileset["daveicon"], 0, 14,12), (270*SCALEFACTOR+index*14*SCALEFACTOR,0))
        
def update_ui_score(ui_tileset,game_display,score):
    #print("Updating UI")
    #score text
    game_display.blit(getBlockInImageDiffSize(ui_tileset["scoretext"], 0, 54,11), (0,0))
    leadingzeroes_score = str(score).zfill(5)
    for index in range(5):
        current_number = int(leadingzeroes_score[index] )
        game_display.blit(getBlockInImageDiffSize(ui_tileset["numbers"], current_number, 8,11), (60*SCALEFACTOR+8*index*SCALEFACTOR,0)) #X offset+each number offset
        
def update_ui_trophy(ui_tileset,game_display): 
    game_display.blit(getBlockInImageDiffSize(ui_tileset["gothrudoortext"], 0, 172,14), (70*SCALEFACTOR,192*SCALEFACTOR))

def update_ui_gun(ui_tileset,game_display): 
    game_display.blit(getBlockInImageDiffSize(ui_tileset["gunicon"], 0, 16,11), (285*SCALEFACTOR,176*SCALEFACTOR))
    game_display.blit(getBlockInImageDiffSize(ui_tileset["guntext"], 0, 27,11), (240*SCALEFACTOR,176*SCALEFACTOR))
    
def update_ui_jetpack(ui_tileset,game_display): 
    game_display.blit(getBlockInImageDiffSize(ui_tileset["jetpacktext"], 0, 62,11), (0,176*SCALEFACTOR))
    game_display.blit(getBlockInImageDiffSize(ui_tileset["jetpackmeter"], 0, 128,12), (70*SCALEFACTOR,176*SCALEFACTOR))

#returns dictionary 
'''TODO: UNIFY FUNCTIONS'''
def load_ui_tiles():
    tilefiles = [file for file in listdir("tiles/ui/") if isfile(join("tiles/ui/", file))] #load all the image files within the directory

    tile_table = {} #init dictionary

    for savedfile in tilefiles:
        image = pygame.image.load("tiles/ui/" + savedfile).convert_alpha()
        ''' TODO: CHECK IF THESE PARAMETERS HAVE ANY USE '''
        image_width, image_height = image.get_size()

        tile_table[fileNameTruncate(savedfile)] = image
    #print(tile_table)
    return tile_table

#display map in pygame
def MapToDisplay(map, display, gfx_map, starting_x):
    for y, row in enumerate(map.getNodeMatrix()):
        for x, col in enumerate(row):
            tile = map.getNode(x,y).getTile()
            if (tile.getId() != "player") and inScreen(x, starting_x) and y > 0:
                display.blit(getBlockInImage(gfx_map[tile.getId()], tile.getGfxId()), (16*(x - starting_x)*SCALEFACTOR, 16*SCALEFACTOR*y))

#function used for scrolling the screen
def moveScreenX(map, display, gfx_map, old_x, increment):
    shift = 0
    #going left
    while(shift > increment) and (old_x + shift > 0):
        MapToDisplay(map, display, gfx_map, old_x + shift)
        pygame.display.flip()
        shift -= 0.5
    #going right
    ''' TODO: FIX THIS '''
    while(shift < increment) and (old_x + shift < map.getWidth()):
        MapToDisplay(map, display, gfx_map, old_x + shift)
        pygame.display.flip()
        shift += 0.5

#check if a given point x is in screen
def inScreen(x, screen_x):
    return (x >= screen_x) and (x < screen_x + SCREEN_WIDTH_TILES)
        
def main():
    ##pygame inits: START
    pygame.init()
    game_display = pygame.display.set_mode((320*SCALEFACTOR, 208*SCALEFACTOR))
    game_display.fill((0, 0, 0))
    
    tileset = load_game_tiles()
    ui_tileset = load_ui_tiles()
    
    current_level_number = 4
    
    ended_game = False
    ##pygame inits: END
    
    ##Keys
    movement_keys = [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]
    inv_keys = [pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT]
    
    ##Engine
    while not ended_game:
        Level = BuildLevel(current_level_number)
        
        GamePlayer = Level.getPlayer()
        playerPosition = Level.getPlayerPosition()
        player_position_x = 16 * playerPosition[0]
        player_position_y = 16 * playerPosition[1]
        Level.setNodeTile(playerPosition[0], playerPosition[1], Tile())            ## Cleans the Player's original position, so the map can print it correct

        screen_current_x = 0   ## The X position where the screen starts
        
        clock = pygame.time.Clock()
        pygame.display.update()      
   
        ##UI inits: START
        print_ui_initial(ui_tileset,game_display,GamePlayer,1)
        score_ui = 0 #initial score, everytime it changes, we update the ui
        trophy_ui = False #initial score, everytime it changes, we update the ui
        
        update_ui_gun(ui_tileset,game_display)
        update_ui_jetpack(ui_tileset,game_display)
        ##UI inits: END

        ended_level = False
        
        while not ended_level:
            #get keys (invetory)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ended_level = True
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT] and GamePlayer.getCurrentState() in [GamePlayer.state.WALK, GamePlayer.state.FLY, GamePlayer.state.JUMP]:
                        pass
                        GamePlayer.setVelocityX(0)
                        GamePlayer.setDirectionX(direction.IDLE)
                    elif event.key in [pygame.K_UP, pygame.K_DOWN] and GamePlayer.getCurrentState() in [GamePlayer.state.FLY, GamePlayer.state.CLIMB]:
                        GamePlayer.setVelocityY(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key in inv_keys:
                        GamePlayer.inventoryInput(inv_keys.index(event.key))    
        
            #get keys (movement)
            pressed_keys = pygame.key.get_pressed()
            key_map = [0,0,0,0]
            for i, key in enumerate(movement_keys):
                if pressed_keys[key]:
                    key_map[i] = 1
            
            GamePlayer.movementInput(key_map)
            
            #update the player position in the level
            (player_position_x, player_position_y) = GamePlayer.updatePosition(player_position_x, player_position_y, Level)
            
            #nextmap
            if GamePlayer.getCurrentState() == GamePlayer.state.ENDMAP:
                ended_level = True      
                break;
            
            ##print tiles
            #moving screen left
            if (screen_current_x > 0) and (player_position_x <= 16*screen_current_x + BOUNDARY):
                moveScreenX(Level, game_display, tileset, screen_current_x, -15)
                screen_current_x -= 15
            #moving screen right
            elif (screen_current_x + SCREEN_WIDTH_TILES < Level.getWidth()) and (player_position_x >= 16*screen_current_x + SCREEN_WIDTH - BOUNDARY):
                moveScreenX(Level, game_display, tileset, screen_current_x, 15)
                screen_current_x += 15
            #not moving
            else:
                MapToDisplay(Level, game_display, tileset, screen_current_x)
                game_display.blit(getBlockInImage(tileset["player"], GamePlayer.getGfxId()), ((player_position_x - 16 * screen_current_x)*SCALEFACTOR, player_position_y*SCALEFACTOR))
                
            if score_ui != GamePlayer.score:
                update_ui_score(ui_tileset,game_display,GamePlayer.score)
                score_ui = GamePlayer.score   
                
            if not trophy_ui and GamePlayer.inventory["trophy"] == 1:
                update_ui_trophy(ui_tileset,game_display)
                trophy_ui = True

            pygame.display.flip()

            pygame.event.pump()
            
            clock.tick(200)
        
        current_level_number += 1        
        
        if current_level_number > 10:
            ended_game = True
        else:
            InterpicScreen(current_level_number)        

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
