from classes import *
from math import floor
import pygame

def buildLevelOne():
    LevelOne = Map()
    
    LevelOne.buildMapBorder(Solid())
    
    LevelOne.buildWall(18, Solid())
    LevelOne.buildWall(19, Solid())
    
    orb = TILESET.index("ITEM_ORB")
    red_d = TILESET.index("ITEM_RED_DIAMOND")
    trophy = TILESET.index("EQUIP_TROPHY1")

    LevelOne.setNodeTile(1, 2, Item(orb, orb, 50))
    LevelOne.setNodeTile(1, 5, Item())
    LevelOne.setNodeTile(1, 6, Solid())
    LevelOne.setNodeTile(1, 7, Item())
    LevelOne.setNodeTile(1, 9, Solid())
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
    LevelOne.setNodeTile(11, 3, Equipment(trophy, trophy, 1000, "trophy"))
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
    LevelOne.setNodeTile(17, 2, Item(red_d, red_d, 150))
    LevelOne.setNodeTile(17, 5, Item())
    LevelOne.setNodeTile(17, 6, Solid())
    #LevelOne.setNodeTile(2, 9, Player())
    
    LevelOne.setNodeTile(0,1,Solid())
    return LevelOne

''' TODO: REORGANIZE/REORDER FUNCTIONS '''
    
def MapToDisplay(map, display, surface_list):
    for y, row in enumerate(map.getNodeMatrix()):
        for x, col in enumerate(row):
            tile_id = map.getNode(x,y).getTile().getId()
            display.blit(surface_list[tile_id], (16*x, 16*y))    
            
def load_tile_table(filename, width, height):
    image = pygame.image.load(filename).convert()
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_x in range(0, int (image_width/width) ):
        line = []
        tile_table.append(line)
        for tile_y in range(0, int(image_height/height) ):
            rect = (tile_x*width, tile_y*height, width, height)
            line.append(image.subsurface(rect))
    return tile_table

def playerCollision(player_pos, map):
    x_left = floor(player_pos[0]/16)
    y_top = floor(player_pos[1]/16)
    x_right = floor((player_pos[0]+15) / 16)
    y_bottom = floor((player_pos[1]+15) / 16)
    
    map_matrix = map.getNodeMatrix()
    
    ''' TODO: CHANGE THIS '''
    VALUE = TILESET.index("BLOCK_DIRT")
    
    collision_topleft = (map_matrix[y_top][x_left].getTile().getId() == VALUE)
    collision_topright = (map_matrix[y_top][x_right].getTile().getId() == VALUE)
    collision_bottomleft = (map_matrix[y_bottom][x_left].getTile().getId() == VALUE)
    collision_bottomright = (map_matrix[y_bottom][x_right].getTile().getId() == VALUE)

    if collision_topleft or collision_topright or collision_bottomleft or collision_bottomright:
        return "BLOCK_COLLISION"
        
    ''' TODO: TREAT OTHER COLLISIONS '''
        
    return "NO_COLLISION"
    
def main():
    LevelOne = buildLevelOne()
    print(LevelOne.printMap())
    NewPlayer = Player()
    LevelOne.setNodeTile(2, 9, NewPlayer) #set player inside the map

    ##pygame inits: START
    pygame.init()
    game_display = pygame.display.set_mode((320, 192))
    game_display.fill((0, 0, 0))
    
    listSurfaces = []   #build tiles and surfaces
    table = load_tile_table("ground.png", 16, 16)
    
    for x, row in enumerate(table):
        for y, tile in enumerate(row):
            listSurfaces.append(tile)
    
    playerSprite = pygame.Surface([15, 15])
    playerSprite.fill((255, 255, 255))
    playerPosition = LevelOne.getPlayerPosition()
    playerPositionX = 16 * playerPosition[0]
    playerPositionY = 16 * playerPosition[1]

    clock = pygame.time.Clock()
    pygame.display.update()
    ended = False
    ##pygame inits: END
    
    keys = [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT]
    
    while not ended:
        
        ##get pressed keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ended = True
            elif event.type == pygame.KEYDOWN:
                NewPlayer.setStatus(keys.index(event.key), 0)
            elif event.type == pygame.KEYUP:
                NewPlayer.setStatus(keys.index(event.key), 1)
                
        ''' TODO:
            We must review this. We are getting problems when the player jumps, because if the
            acceleration is equal to 5, it might occur that a gap with less than 5px is formed
            between the player and the ground.
            I think we might focus firstly on how the player will behave inside its class. It
            might help us while fixing the stuff here, in the outer.
            By the way, we might need to use the clock ticks to work with the new movement.
            '''
                
        playerPositionX = playerPositionX + NewPlayer.getAccelerationX()
        if playerCollision((playerPositionX, playerPositionY), LevelOne) == "BLOCK_COLLISION":
            playerPositionX = playerPositionX - NewPlayer.getAccelerationX()
        
        ##i've commented the Y axis movement functions because we need to rework this entirely.
        
        '''
        playerPositionY = playerPositionY + NewPlayer.getAccelerationY()
        if playerCollision((playerPositionX, playerPositionY), LevelOne) == "BLOCK_COLLISION":
            playerPositionY = playerPositionY - NewPlayer.getAccelerationY()
        
        if NewPlayer.getState() == "normal":
            if playerCollision((playerPositionX, playerPositionY+1), LevelOne) == "NO_COLLISION":
                NewPlayer.gravity()
            else: NewPlayer.setAccelerationY(0)
            '''
        
        MapToDisplay(LevelOne, game_display, listSurfaces)
        game_display.blit(playerSprite, (playerPositionX, playerPositionY))        
        
        pygame.display.flip()
        
        clock.tick(60)
        
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()