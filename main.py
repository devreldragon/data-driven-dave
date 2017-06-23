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
    rect = (index*SIZE, 0, SIZE, SIZE)
    block_image = image.subsurface(rect)
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
        image = pygame.image.load("tiles/game/" + savedfile).convert()
        ''' TODO: CHECK IF THESE PARAMETERS HAVE ANY USE '''
        image_width, image_height = image.get_size()
        
        tile_table[fileNameTruncate(savedfile)] = image
    
    return tile_table

#display map in pygame    
def MapToDisplay(map, display, gfx_map):
    for y, row in enumerate(map.getNodeMatrix()):
        for x, col in enumerate(row):
            tile = map.getNode(x,y).getTile()
            if tile.getId() != "player":              #won't print player
                display.blit(getBlockInImage(gfx_map[tile.getId()], tile.getGfxId()), (16*x, 16*y))    
        
#this function returns 1 if given number is positive, -1 if it's negative
def checkNumberSign(number):
    if number < 0: return -1
    else: return 1
 

 
def main():
    LevelOne = buildLevelOne()

    ##pygame inits: START
    pygame.init()
    game_display = pygame.display.set_mode((320, 192))
    game_display.fill((0, 0, 0))
    
    tileset = load_game_tiles()
    
    GamePlayer = LevelOne.getPlayer()
    playerPosition = LevelOne.getPlayerPosition()
    playerPositionX = 16 * playerPosition[0]
    playerPositionY = 16 * playerPosition[1]

    clock = pygame.time.Clock()
    pygame.display.update()
    ended = False
    ##pygame inits: END
    
    keys = [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT]
    
    jumpfalling = 0
    
    while not ended:
    
        ##get pressed keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ended = True
            elif event.type == pygame.KEYUP:
                GamePlayer.input(keys.index(event.key), 1)
            elif event.type == pygame.KEYDOWN:
                output = GamePlayer.input(keys.index(event.key), 0)
                if output == 1:
                    '''TODO: GUNFIRE'''
                    pass            
               
        if GamePlayer.getXUpdateTimer() <= 0:
            playerPositionX = playerPositionX + checkNumberSign(GamePlayer.getAccelerationX())
            if LevelOne.checkPlayerCollision((playerPositionX, playerPositionY)) == "BLOCK_COLLISION":
                playerPositionX = playerPositionX - checkNumberSign(GamePlayer.getAccelerationX())
            GamePlayer.resetPosTimer('x')
            
            #no block underneath (walking)
            if LevelOne.checkPlayerCollision((playerPositionX, playerPositionY+1)) != "BLOCK_COLLISION" and GamePlayer.getState() == "walk":
                GamePlayer.setState("fall")
                ''' TODO: RENAME/REFACTOR THIS 5 (other places too) '''
                GamePlayer.setAccelerationY(5)

        player_state = GamePlayer.getState()    
        
        if GamePlayer.getYUpdateTimer() <= 0:
            playerPositionY = playerPositionY + checkNumberSign(GamePlayer.getAccelerationY())
            if LevelOne.checkPlayerCollision((playerPositionX, playerPositionY)) == "BLOCK_COLLISION" and player_state != "die":
                ''' TODO: THERE'S AN ERROR IN HERE. I'M OUT OF TIME RIGHT NOW. GONNA FIX IT LATER. LEAVE IT FOR ME '''
                if player_state == "fall":
                    GamePlayer.setState("walk")
                    GamePlayer.setAccelerationY(0)
                elif player_state == "jump":
                    GamePlayer.setState("fall")
                    ''' TODO: RENAME/REFACTOR THIS 5 '''
                    GamePlayer.setAccelerationY(5) 
                elif player_state == "climb" and GamePlayer.getAccelerationY() > 0:
                    GamePlayer.setState("walk")
                    GamePlayer.setAccelerationY(0)
                playerPositionY = playerPositionY - checkNumberSign(GamePlayer.getAccelerationY())
            GamePlayer.resetPosTimer('y')

        if GamePlayer.getState() == "jump" or jumpfalling:
            GamePlayer.incAccelerationY(0.05)
            if GamePlayer.getAccelerationY() == 0:
                GamePlayer.setState("fall")
                jumpfalling = 1
            elif GamePlayer.getAccelerationY() == 5:
                jumpfalling = 0
        
        MapToDisplay(LevelOne, game_display, tileset)
        game_display.blit(getBlockInImage(tileset["player"], GamePlayer.getGfxId()), (playerPositionX, playerPositionY))
                
        pygame.display.flip()
        
        clock.tick(200)
        
        GamePlayer.decPosTimer('x')
        GamePlayer.decPosTimer('y')
        
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()