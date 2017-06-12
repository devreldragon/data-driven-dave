import sys
import pygame
import pygame.locals
from random import randint
from classes import *

def buildLevelOne():
    LevelOne = Map()
    
    LevelOne.buildMapBorder(Solid())
    
    LevelOne.buildWall(18, Solid())
    LevelOne.buildWall(19, Solid())
    
    orb = TILESET.index("ITEM_ORB")
    red_d = TILESET.index("ITEM_RED_DIAMOND")
    trophy = TILESET.index("EQUIP_TROPHY")

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
    LevelOne.setNodeTile(2, 9, Player())
    
    LevelOne.setNodeTile(0,1,Solid())
    return LevelOne

#Given a Map object, print it in the pygame display
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

if __name__=='__main__':
    LevelOne = buildLevelOne()

    pygame.init()
    listSurfaces = []
    screen = pygame.display.set_mode((320, 192))
    screen.fill((0, 0, 0))
    table = load_tile_table("ground.png", 16, 16)
    
    for x, row in enumerate(table):
        for y, tile in enumerate(row):
            listSurfaces.append(tile)

    '''
    for x, row in enumerate(table):
        for y, tile in enumerate(row):
            screen.blit(listSurfaces[randint(0,len(listSurfaces)-1)], (x*16, y*16) )         
    '''
    
    MapToDisplay(LevelOne, screen, listSurfaces)
    
    pygame.display.flip()

    #game processing
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass
   