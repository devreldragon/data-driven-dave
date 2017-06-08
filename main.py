from classes import *

def buildMapBorder(map, tile):
    bottom = map.getHeight() - 1
    right = map.getWidth() - 1
    
    for x in range(right + 1):
        map.setNodeTile(x, 1, tile)
        map.setNodeTile(x, bottom, tile)
    
    for y in range(2, bottom):
        map.setNodeTile(0, y, tile)
        map.setNodeTile(right, y, tile)

def buildWall(map, x, tile):
    for y in range(1, map.getHeight()):
        map.setNodeTile(x, y, tile)
        
def main():
    LevelOne = Map()
    
    buildMapBorder(LevelOne, Solid())
    
    buildWall(LevelOne, 19, Solid())
    buildWall(LevelOne, 20, Solid())
    
    orb = TILESET.index("ITEM_ORB")
    red_d = TILESET.index("ITEM_RED_DIAMOND")
    door = TILESET.index("GOAL_DOOR")
    trophy = TILESET.index("EQUIP_TROPHY")
    
    a = Item()
    b = Equipment()
    c = InteractiveScenery()
    d = Item()
    
    LevelOne.setNodeTile(1, 2, a.Construct(orb, orb, 50))
    
    #???
    print(LevelOne.getNode(1, 2).pos_x)
    input()
    
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
    LevelOne.setNodeTile(11, 3, b.Construct(trophy, trophy, 1000, "trophy"))
    LevelOne.setNodeTile(11, 4, Solid())
    LevelOne.setNodeTile(11, 8, Solid())
    LevelOne.setNodeTile(11, 9, Solid())
    LevelOne.setNodeTile(12, 8, Solid())
    LevelOne.setNodeTile(12, 9, c.Construct(door, door, "endmap", 1, ("endmap")))
    LevelOne.setNodeTile(13, 5, Item())
    LevelOne.setNodeTile(13, 6, Solid())
    LevelOne.setNodeTile(13, 8, Solid())
    LevelOne.setNodeTile(14, 8, Solid())
    LevelOne.setNodeTile(15, 3, Item())
    LevelOne.setNodeTile(15, 4, Solid())
    LevelOne.setNodeTile(15, 8, Solid())
    LevelOne.setNodeTile(16, 8, Solid())
    LevelOne.setNodeTile(17, 2, d.Construct(red_d, red_d, 150))
    LevelOne.setNodeTile(17, 5, Item())
    LevelOne.setNodeTile(17, 6, Solid())
    
    
    LevelOne.setNodeTile(0,1,Solid())
    LevelOne.printMap()

if __name__ == "__main__":
    main()