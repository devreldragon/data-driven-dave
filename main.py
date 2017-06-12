from classes import *
import pygame

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

def main():
    LevelOne = buildLevelOne()

    pygame.init()
    game_display = pygame.display.set_mode((320, 192))
    game_display.fill((0, 0, 0))

    playerSprite = pygame.Surface([15, 15])
    playerSprite.fill((255, 255, 255))
    playerPositionX = 120
    playerPositionY = 50
    playerAccelerationX = 0
    playerAccelerationY = 0

    clock = pygame.time.Clock()
    pygame.display.update()
    ended = False
    
    while not ended:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                ended = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    playerAccelerationY = playerAccelerationY - 1
                elif event.key == pygame.K_DOWN:
                    playerAccelerationY = playerAccelerationY + 1
                elif event.key == pygame.K_LEFT:
                    playerAccelerationX = playerAccelerationX - 1
                elif event.key == pygame.K_RIGHT:
                    playerAccelerationX = playerAccelerationX + 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    playerAccelerationY = playerAccelerationY + 1
                elif event.key == pygame.K_DOWN:
                    playerAccelerationY = playerAccelerationY - 1
                elif event.key == pygame.K_LEFT:
                    playerAccelerationX = playerAccelerationX + 1
                elif event.key == pygame.K_RIGHT:
                    playerAccelerationX = playerAccelerationX - 1

        playerPositionX = playerPositionX + playerAccelerationX
        playerPositionY = playerPositionY + playerAccelerationY
        game_display.fill((0,0,0))
        game_display.blit(playerSprite, (playerPositionX, playerPositionY))

        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()