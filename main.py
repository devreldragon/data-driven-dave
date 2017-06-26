from classes import *
from os import listdir
from os.path import isfile, join
import pygame

'''
Levels
'''

def buildLevelOne():
    LevelOne = Map()

    LevelOne.buildMapBorder(Solid())

    LevelOne.buildWall(18, Solid())
    LevelOne.buildWall(19, Solid())

    orb = "items"
    red_d = "items"
    trophy = "trophy"

    LevelOne.setNodeTile(1, 2, Item(orb, 0, 50))
    LevelOne.setNodeTile(1, 5, Item())
    LevelOne.setNodeTile(1, 6, Solid())
    LevelOne.setNodeTile(1, 7, Item())
    LevelOne.setNodeTile(1,9, Solid("tunnel", 1))
    LevelOne.setNodeTile(3, 3, Item())
    LevelOne.setNodeTile(3, 4, Solid())
    LevelOne.setNodeTile(4, 8, Solid())
    LevelOne.setNodeTile(5, 5, Item())
    LevelOne.setNodeTile(5, 6, Solid())
    LevelOne.setNodeTile(5, 8, Solid())
    LevelOne.setNodeTile(6, 8, Solid())
    LevelOne.setNodeTile(7, 3, Item())
    LevelOne.setNodeTile(7, 4, Solid())
    LevelOne.setNodeTile(7, 7, Item())
    LevelOne.setNodeTile(7, 8, Solid())
    LevelOne.setNodeTile(9, 5, Item())
    LevelOne.setNodeTile(9, 6, Solid())
    LevelOne.setNodeTile(11, 3, Equipment(trophy, 0, 1000, "trophy"))
    LevelOne.setNodeTile(11, 4, Solid())
    LevelOne.setNodeTile(11, 8, Solid())
    LevelOne.setNodeTile(11, 9, Solid())
    LevelOne.setNodeTile(12, 8, Solid())
    LevelOne.setNodeTile(12, 9, InteractiveScenery())
    LevelOne.setNodeTile(13, 5, Item())
    LevelOne.setNodeTile(13, 6, Solid())
    LevelOne.setNodeTile(13, 8, Solid())
    LevelOne.setNodeTile(14, 8, Solid())
    LevelOne.setNodeTile(15, 3, Item())
    LevelOne.setNodeTile(15, 4, Solid())
    LevelOne.setNodeTile(15, 8, Solid())
    LevelOne.setNodeTile(16, 8, Solid())
    LevelOne.setNodeTile(17, 2, Item(red_d, 2, 150))
    LevelOne.setNodeTile(17, 5, Item())
    LevelOne.setNodeTile(17, 6, Solid())
    LevelOne.setNodeTile(2, 9, Player())
    return LevelOne

def buildLevelTwo():
    LevelTwo = Map()

    LevelTwo.buildMapBorder(Solid())

    ORB = Item("items", 0, 50)
    BLUE_DIAMOND = Item("items", 1, 100)
    RED_DIAMOND = Item("items", 2, 150)
    TROPHY = Equipment("trophy", 0, 1000, "trophy") 
    PINKPIPE = Solid("pinkpipe", 1)
    FIRE = InteractiveScenery("fire", 0, InteractiveScenery.TYPE.HAZARD, 1)
    WATER = InteractiveScenery("water", 0, InteractiveScenery.TYPE.HAZARD, 1)
    TENTACLE = InteractiveScenery("tentacles", 0, InteractiveScenery.TYPE.HAZARD, 1)
    DOOR = InteractiveScenery()
    REDBRICK = Solid()
    
    LevelTwo.setNodeTile(1, 9, Player())
    
    LevelTwo.setNodeTile(1, 2, RED_DIAMOND)
    LevelTwo.setNodeTile(1, 4, PINKPIPE)
    LevelTwo.setNodeTile(2, 6, PINKPIPE)
    LevelTwo.setNodeTile(3, 6, PINKPIPE)
    LevelTwo.setNodeTile(3, 10, FIRE)
    LevelTwo.setNodeTile(4, 4, PINKPIPE)
    LevelTwo.setNodeTile(4, 8, PINKPIPE)
    LevelTwo.setNodeTile(4, 10, FIRE)
    LevelTwo.setNodeTile(5, 8, PINKPIPE)
    LevelTwo.setNodeTile(5, 10, FIRE)
    LevelTwo.setNodeTile(6, 8, PINKPIPE)
    LevelTwo.setNodeTile(6, 10, FIRE)
    LevelTwo.setNodeTile(7, 2, BLUE_DIAMOND)
    LevelTwo.setNodeTile(7, 10, FIRE)
    LevelTwo.setNodeTile(8, 5, PINKPIPE)
    LevelTwo.setNodeTile(8, 8, RED_DIAMOND)
    LevelTwo.setNodeTile(8, 10, FIRE)
    LevelTwo.setNodeTile(9, 5, PINKPIPE)
    LevelTwo.setNodeTile(9, 6, REDBRICK)
    LevelTwo.setNodeTile(9, 7, REDBRICK)
    LevelTwo.setNodeTile(9, 8, REDBRICK)
    LevelTwo.setNodeTile(9, 9, REDBRICK)
    LevelTwo.setNodeTile(10, 5, PINKPIPE)
    LevelTwo.setNodeTile(10, 9, BLUE_DIAMOND)
    LevelTwo.setNodeTile(10, 10, FIRE)
    LevelTwo.setNodeTile(11, 7, PINKPIPE)
    LevelTwo.setNodeTile(11, 10, FIRE)
    LevelTwo.setNodeTile(12, 10, FIRE)
    LevelTwo.setNodeTile(13, 4, PINKPIPE)
    LevelTwo.setNodeTile(13, 6, TROPHY)
    LevelTwo.setNodeTile(13, 9, PINKPIPE)
    LevelTwo.setNodeTile(13, 10, FIRE)
    LevelTwo.setNodeTile(14, 5, REDBRICK)
    LevelTwo.setNodeTile(14, 6, REDBRICK)
    LevelTwo.setNodeTile(14, 7, REDBRICK)
    LevelTwo.setNodeTile(14, 8, REDBRICK)
    LevelTwo.setNodeTile(14, 9, REDBRICK)
    LevelTwo.setNodeTile(15, 10, WATER)
    LevelTwo.setNodeTile(16, 6, PINKPIPE)
    LevelTwo.setNodeTile(16, 8, BLUE_DIAMOND)
    LevelTwo.setNodeTile(16, 10, WATER)
    LevelTwo.setNodeTile(17, 6, PINKPIPE)
    LevelTwo.setNodeTile(17, 8, BLUE_DIAMOND)
    LevelTwo.setNodeTile(17, 10, WATER)
    LevelTwo.setNodeTile(18, 6, PINKPIPE)
    LevelTwo.setNodeTile(18, 8, BLUE_DIAMOND)
    LevelTwo.setNodeTile(18, 10, WATER)
    LevelTwo.setNodeTile(19, 6, PINKPIPE)
    LevelTwo.setNodeTile(19, 8, BLUE_DIAMOND)
    LevelTwo.setNodeTile(19, 10, WATER)
    LevelTwo.setNodeTile(20, 2, ORB)
    LevelTwo.setNodeTile(20, 6, PINKPIPE)
    LevelTwo.setNodeTile(20, 8, BLUE_DIAMOND)
    LevelTwo.setNodeTile(20, 10, WATER)
    LevelTwo.setNodeTile(21, 10, WATER)
    for i in range(5, 10):
        LevelTwo.setNodeTile(22, i, REDBRICK)
    LevelTwo.setNodeTile(23, 4, REDBRICK)
    LevelTwo.setNodeTile(23, 5, REDBRICK) 
    LevelTwo.setNodeTile(24, 3, REDBRICK)
    LevelTwo.setNodeTile(24, 4, REDBRICK)
    LevelTwo.setNodeTile(24, 7, REDBRICK)
    LevelTwo.setNodeTile(24, 8, REDBRICK)
    LevelTwo.setNodeTile(25, 3, REDBRICK)
    LevelTwo.setNodeTile(25, 6, REDBRICK)
    LevelTwo.setNodeTile(26, 3, REDBRICK)
    LevelTwo.setNodeTile(26, 5, REDBRICK)
    LevelTwo.setNodeTile(26, 6, REDBRICK)
    LevelTwo.setNodeTile(26, 8, REDBRICK)
    LevelTwo.setNodeTile(26, 9, REDBRICK)
    LevelTwo.setNodeTile(27, 3, REDBRICK)
    LevelTwo.setNodeTile(27, 5, REDBRICK)
    LevelTwo.setNodeTile(27, 8, REDBRICK)
    LevelTwo.setNodeTile(27, 9, ORB)
    LevelTwo.setNodeTile(28, 3, REDBRICK)
    LevelTwo.setNodeTile(28, 5, REDBRICK)
    LevelTwo.setNodeTile(28, 6, ORB)
    for i in range(5, 9):
        LevelTwo.setNodeTile(29, i, REDBRICK)    
    for i in range(2, 6):
        LevelTwo.setNodeTile(30, i, REDBRICK)
    for i in range(2, 6):
        LevelTwo.setNodeTile(31, i, REDBRICK)
    LevelTwo.setNodeTile(31, 8, REDBRICK)
    LevelTwo.setNodeTile(31, 9, ORB)
    LevelTwo.setNodeTile(32, 5, REDBRICK)
    for i in range(7, 10):
        LevelTwo.setNodeTile(32, i, REDBRICK)    
    LevelTwo.setNodeTile(33, 3, REDBRICK)
    LevelTwo.setNodeTile(33, 5, REDBRICK)
    LevelTwo.setNodeTile(34, 3, REDBRICK)
    LevelTwo.setNodeTile(34, 5, REDBRICK)
    LevelTwo.setNodeTile(34, 6, REDBRICK)
    LevelTwo.setNodeTile(34, 7, REDBRICK)
    LevelTwo.setNodeTile(35, 3, REDBRICK)
    LevelTwo.setNodeTile(35, 9, REDBRICK)
    LevelTwo.setNodeTile(36, 3, REDBRICK)
    LevelTwo.setNodeTile(36, 7, REDBRICK)
    LevelTwo.setNodeTile(36, 9, ORB)
    for i in range(3, 10):
        LevelTwo.setNodeTile(37, i, REDBRICK)
    for i in range(38, 48):
        LevelTwo.setNodeTile(i, 3, REDBRICK)
        LevelTwo.setNodeTile(i, 10, FIRE)
    for i in range(48, 50):
        LevelTwo.setNodeTile(i, 2, REDBRICK)
        LevelTwo.setNodeTile(i, 3, REDBRICK)
        LevelTwo.setNodeTile(i, 10, FIRE) 
    LevelTwo.setNodeTile(47, 2, DOOR)
    
    #write the letters
    ##C
    LevelTwo.setNodeTile(38, 5, TENTACLE)
    LevelTwo.setNodeTile(38, 6, TENTACLE)
    LevelTwo.setNodeTile(38, 7, TENTACLE)
    LevelTwo.setNodeTile(39, 4, TENTACLE)
    LevelTwo.setNodeTile(39, 8, TENTACLE)
    LevelTwo.setNodeTile(40, 4, TENTACLE)
    LevelTwo.setNodeTile(40, 8, TENTACLE)
    
    ##I
    LevelTwo.setNodeTile(42, 4, TENTACLE)
    LevelTwo.setNodeTile(42, 8, TENTACLE)
    LevelTwo.setNodeTile(43, 4, TENTACLE)
    LevelTwo.setNodeTile(43, 5, TENTACLE)
    LevelTwo.setNodeTile(43, 6, TENTACLE)
    LevelTwo.setNodeTile(43, 7, TENTACLE)
    LevelTwo.setNodeTile(43, 8, TENTACLE)
    LevelTwo.setNodeTile(44, 4, TENTACLE)
    LevelTwo.setNodeTile(44, 8, TENTACLE)
    
    ##C
    LevelTwo.setNodeTile(46, 5, TENTACLE)
    LevelTwo.setNodeTile(46, 6, TENTACLE)
    LevelTwo.setNodeTile(46, 7, TENTACLE)
    LevelTwo.setNodeTile(47, 4, TENTACLE)
    LevelTwo.setNodeTile(47, 8, TENTACLE)
    LevelTwo.setNodeTile(48, 4, TENTACLE)
    LevelTwo.setNodeTile(48, 8, TENTACLE) 

    return LevelTwo
    
    
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

def print_ui(ui_tileset,game_display,score,level_number,lives):
    #score text
    game_display.blit(getBlockInImageDiffSize(ui_tileset["scoretext"], 0, 54,11), (0,0))
    leadingzeroes_score = str(score).zfill(5)
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
    for index in range(lives):
        game_display.blit(getBlockInImageDiffSize(ui_tileset["daveicon"], 0, 14,12), (270*SCALEFACTOR+index*14*SCALEFACTOR,0))
    

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
    print(tile_table)
    return tile_table


    
#display map in pygame
def MapToDisplay(map, display, gfx_map):
    for y, row in enumerate(map.getNodeMatrix()):
        for x, col in enumerate(row):
            tile = map.getNode(x,y).getTile()
            if tile.getId() != "player":              #won't print player
                display.blit(getBlockInImage(gfx_map[tile.getId()], tile.getGfxId()), (16*SCALEFACTOR*x, 16*SCALEFACTOR*y))


def main():
    Level = buildLevelTwo()

    ##pygame inits: START
    pygame.init()
    game_display = pygame.display.set_mode((320*SCALEFACTOR, 192*SCALEFACTOR))
    game_display.fill((0, 0, 0))

    tileset = load_game_tiles()
    ui_tileset = load_ui_tiles()

    GamePlayer = Level.getPlayer()
    playerPosition = Level.getPlayerPosition()
    player_position_x = 16 * playerPosition[0]
    player_position_y = 16 * playerPosition[1]
    Level.setNodeTile(playerPosition[0], playerPosition[1], Tile())            ## Cleans the Player's original position, so the map can print it correct

    clock = pygame.time.Clock()
    pygame.display.update()
    ended = False
    ##pygame inits: END

    movement_keys = [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]
    inv_keys = [pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT]
    
    while not ended:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ended = True
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
    
        pressed_keys = pygame.key.get_pressed()
        key_map = [0,0,0,0]
        for i, key in enumerate(movement_keys):
            if pressed_keys[key]:
                key_map[i] = 1
        
        GamePlayer.movementInput(key_map)
        
        (player_position_x, player_position_y) = GamePlayer.updatePosition(player_position_x, player_position_y, Level)
        
        if GamePlayer.getCurrentState() == GamePlayer.state.ENDMAP:
            '''TODO: interpic and next level'''
            ended = True
        
        MapToDisplay(Level, game_display, tileset)
        game_display.blit(getBlockInImage(tileset["player"], GamePlayer.getGfxId()), (player_position_x*SCALEFACTOR, player_position_y*SCALEFACTOR))
        print_ui(ui_tileset,game_display,GamePlayer.score,1,3)
        pygame.display.flip()

        pygame.event.pump()
        
        clock.tick(200)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
