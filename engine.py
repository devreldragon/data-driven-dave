import sys
import pygame
import pygame.locals
from random import randint

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
    pygame.init()
    listSurfaces = []
    screen = pygame.display.set_mode((160, 160))
    screen.fill((0, 0, 0))
    table = load_tile_table("ground.png", 16, 16)
    for x, row in enumerate(table):
        for y, tile in enumerate(row):
            listSurfaces.append(tile)
            
    #for x in range(len(listSurfaces)):
        #print(listSurfaces[x])
           
    for x, row in enumerate(table):
        for y, tile in enumerate(row):
            screen.blit(listSurfaces[randint(0,len(listSurfaces)-1)], (x*16, y*16) )         
     
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass
   