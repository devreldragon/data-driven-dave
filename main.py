from classes import *
from os import listdir
from os.path import isfile, join
import pygame

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
    



#returns dictionary TODO UNIFY FUNCTIONS
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
    LevelOne = buildLevelOne()

    ##pygame inits: START
    pygame.init()
    game_display = pygame.display.set_mode((320*SCALEFACTOR, 192*SCALEFACTOR))
    game_display.fill((0, 0, 0))

    tileset = load_game_tiles()
    ui_tileset = load_ui_tiles()

    GamePlayer = LevelOne.getPlayer()
    playerPosition = LevelOne.getPlayerPosition()
    player_position_x = 16 * playerPosition[0]
    player_position_y = 16 * playerPosition[1]
    LevelOne.setNodeTile(playerPosition[0], playerPosition[1], Tile())            ## Cleans the Player's original position, so the map can print it correct

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
        
        (player_position_x, player_position_y) = GamePlayer.updatePosition(player_position_x, player_position_y, LevelOne)
        
        if GamePlayer.getCurrentState() == GamePlayer.state.ENDMAP:
            '''TODO: interpic and next level'''
            ended = True
        
        MapToDisplay(LevelOne, game_display, tileset)
        game_display.blit(getBlockInImage(tileset["player"], GamePlayer.getGfxId()), (player_position_x*SCALEFACTOR, player_position_y*SCALEFACTOR))
        print_ui(ui_tileset,game_display,GamePlayer.score,1,3)
        pygame.display.flip()

        pygame.event.pump()
        
        clock.tick(200)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
