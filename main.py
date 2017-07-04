from classes import *
from os import listdir
from os.path import isfile, join


'''
Level construction
'''

def BuildLevel(level_number):
    #open the level in the txt
    textmap = open("levels/" + str(level_number) + ".txt", 'r')

    #get height (must reset offset)
    height = len(textmap.readlines())
    textmap.seek(0)

    #get width (must reset offset)
    width = int(len(textmap.readline()) / 3)
    textmap.seek(0)

    #init class
    Level = Map(height, width)

    #for each node, set it accordingly
    for y, line in enumerate(textmap.readlines()):
        x = 0
        while (x < width):
            text_tile = line[(3*x):(3*x + 2)]
            tile_type = tileFromText(text_tile)
            Level.setNodeTile(x, y, tile_type)
            x += 1

    return Level

def initLevel(level_number):
    #build the level
    Level = BuildLevel(level_number)

    #init player and his positions
    GamePlayer = Player()
    playerPosition = Level.getPlayerSpawnerPosition(0)
    player_position_x = WIDTH_OF_MAP_NODE * playerPosition[0]
    player_position_y = HEIGHT_OF_MAP_NODE * playerPosition[1]

    return (Level, GamePlayer, player_position_x, player_position_y)

def tileFromText(text_tile):
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
        return Tile("scenery", gfx_id)
    elif text_tile[0] == 'M':
        return Tile("moonstars", gfx_id)
    elif text_tile[0] == 'E':
        return InteractiveScenery("tree", gfx_id, INTSCENERYTYPE.TREE)
    elif text_tile[0] == 'I':
        scores = [50, 100, 150, 200, 300, 500]
        return Item("items", gfx_id, scores[1])
    elif text_tile[0] == 'P':
        return Solid("pinkpipe", gfx_id)
    else:
        return Tile("scenery", 0)


'''
User interface (invetory, scores, etc)
'''

def print_ui_initial(ui_tileset,game_display,player,level_number):
    #print("Printing initial UI")

    #score text
    game_display.blit(cropBlockFromGraphic(ui_tileset["scoretext"], 0, 54,11), (0,0))
    leadingzeroes_score = str(player.score).zfill(5)
    for index in range(5):
        current_number = int(leadingzeroes_score[index] )
        game_display.blit(cropBlockFromGraphic(ui_tileset["numbers"], current_number, 8,11, 10), (60*TILE_SCALE_FACTOR+8*index*TILE_SCALE_FACTOR,0))

    #level text
    game_display.blit(cropBlockFromGraphic(ui_tileset["leveltext"], 0, 45,11), (120*TILE_SCALE_FACTOR,0))
    leadingzeroes_level = str(level_number).zfill(2)
    for index in range(2):
        current_level = int(leadingzeroes_level[index] )
        game_display.blit(cropBlockFromGraphic(ui_tileset["numbers"], current_level, 8,11, 10), (170*TILE_SCALE_FACTOR+8*index*TILE_SCALE_FACTOR,0))

    #daves text
    game_display.blit(cropBlockFromGraphic(ui_tileset["davestext"], 0, 50,11), (210*TILE_SCALE_FACTOR,0))
    for index in range(player.lifes):
        game_display.blit(cropBlockFromGraphic(ui_tileset["daveicon"], 0, 14,12), (270*TILE_SCALE_FACTOR+index*14*TILE_SCALE_FACTOR,0))

def update_ui_score(ui_tileset,game_display,score):
    #print("Updating UI")
    #score text
    game_display.blit(cropBlockFromGraphic(ui_tileset["scoretext"], 0, 54,11), (0,0))
    leadingzeroes_score = str(score).zfill(5)
    for index in range(5):
        current_number = int(leadingzeroes_score[index] )
        game_display.blit(cropBlockFromGraphic(ui_tileset["numbers"], current_number, 8,11,10), (60*TILE_SCALE_FACTOR+8*index*TILE_SCALE_FACTOR,0)) #X offset+each number offset

def update_ui_trophy(ui_tileset,game_display):
    game_display.blit(cropBlockFromGraphic(ui_tileset["gothrudoortext"], 0, 172,14), (70*TILE_SCALE_FACTOR,192*TILE_SCALE_FACTOR))

def update_ui_gun(ui_tileset,game_display):
    game_display.blit(cropBlockFromGraphic(ui_tileset["gunicon"], 0, 16,11), (285*TILE_SCALE_FACTOR,176*TILE_SCALE_FACTOR))
    game_display.blit(cropBlockFromGraphic(ui_tileset["guntext"], 0, 27,11), (240*TILE_SCALE_FACTOR,176*TILE_SCALE_FACTOR))

def update_ui_jetpack(ui_tileset,game_display):
    game_display.blit(cropBlockFromGraphic(ui_tileset["jetpacktext"], 0, 62,11), (0,176*TILE_SCALE_FACTOR))
    game_display.blit(cropBlockFromGraphic(ui_tileset["jetpackmeter"], 0, 128,12), (70*TILE_SCALE_FACTOR,176*TILE_SCALE_FACTOR))

'''TODO: UNIFY THIS FUNCTION WITH load_tiles'''
## returns dictionary
def load_ui_tiles():
    tilefiles = [file for file in listdir("tiles/ui/") if isfile(join("tiles/ui/", file))] #load all the image files within the directory

    tile_table = {} #init dictionary

    for savedfile in tilefiles:
        image = pygame.image.load("tiles/ui/" + savedfile).convert_alpha()
        ''' TODO: CHECK IF THESE PARAMETERS HAVE ANY USE '''
        image_width, image_height = image.get_size()

        ''' TODO: REVIEW THIS '''
        tile_table[graphicPropertiesFromFilename(savedfile)[0]] = image
    #print(tile_table)
    return tile_table

'''
Tile and gfxs
'''

## split a string separating numbers from letters
def splitStringIntoLettersAndNumbers(string):
    split_string = []
    sub_string = ""
    index = 0

    ''' TODO: REFACTOR? '''
    while index < len(string):
        if string[index].isalpha():
            while index < len(string) and string[index].isalpha():
                sub_string += string[index]
                index += 1
        elif string[index].isdigit():
             while index < len(string) and string[index].isdigit():
                sub_string += string[index]
                index += 1
        else:
            index += 1
        split_string.append(sub_string)
        sub_string = ""

    return split_string

## crop a set of tiles, getting the block in index X
def cropBlockFromGraphic(image, index, size_x, size_y, num_of_blocks=1):
    x_index = index % num_of_blocks
    x_index_pixel = x_index * size_x

    #select the tile to crop (y is always 0)
    rectangle = (x_index_pixel, 0, size_x, size_y)
    size_of_rectangle = (size_x * TILE_SCALE_FACTOR, size_y * TILE_SCALE_FACTOR)
    cropped_tile = pygame.transform.scale(image.subsurface(rectangle), size_of_rectangle)
    return cropped_tile

## get name and size properties from filename
def graphicPropertiesFromFilename(filename):
    split_filename = splitStringIntoLettersAndNumbers(filename)

    name = split_filename[0]
    height = int(split_filename[3])
    width = int(split_filename[1])

    return (name, height, width)

''' TODO: UNIFY THIS FUNCTION WITH load_ui_tiles '''
## returns dictionary
def load_game_tiles():
    tilefiles = [file for file in listdir("tiles/game/") if isfile(join("tiles/game/", file))] #load all the image files within the directory

    tile_table = {} #init dictionary

    for savedfile in tilefiles:
        image = pygame.image.load("tiles/game/" + savedfile).convert_alpha()

        tile_name, tile_height, tile_width = graphicPropertiesFromFilename(savedfile)

        TILE_IDS.append(tile_name)
        
        tile_table[tile_name] = (image, tile_height, tile_width)

    return tile_table

'''
Interpic
'''

def showInterpic(completed_levels, screen, tileset):
    Interpic = BuildLevel("interpic")

    clock = pygame.time.Clock()

    screen.setXPosition(0)    
    screen.printMap(Interpic, tileset)

    #init player
    player = Player()
    playerPosition = Interpic.getPlayerSpawnerPosition(0)
    player_position_x = WIDTH_OF_MAP_NODE * playerPosition[0]
    player_position_y = HEIGHT_OF_MAP_NODE * playerPosition[1]

    player.setCurrentState(STATE.WALK)
    player.flip_sprite = True

    #keep moving the player right, until it reaches the screen boundary
    player_reached_boundary = (player_position_x >= screen.getUnscaledWidth())

    while not player_reached_boundary:
        player_position_x += player.getMaxSpeedX() * player.getXSpeedFactor()

        #print map
        screen.printMap(Interpic, tileset)
        #print player
        screen.printPlayer(player, player_position_x, player_position_y, tileset)

        player_reached_boundary = (player_position_x >= screen.getUnscaledWidth())

        player.updateAnimation()
        pygame.display.flip()
        clock.tick(200)

'''
Pygame inits
'''

def main():
    ##Init pygame
    pygame.init()
    game_screen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    ##Init tiles
    ''' TODO: UNIFY '''
    tileset = load_game_tiles()
    ui_tileset = load_ui_tiles()

    ##Init game
    ended_game = False
    game_over = False

    ''' TODO: TITLE SCREEN '''
    current_level_number = 5

    ##Available Keys
    movement_keys = [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]
    inv_keys = [pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT]

    ##Game processing
    while not ended_game and not game_over:
        # init stuff
        clock = pygame.time.Clock()
        pygame.display.update()

        # build the level
        (Level, GamePlayer, player_position_x, player_position_y) = initLevel(current_level_number)
        DeathPuff = AnimatedSprite("explosion", 0)
        death_timer = -1
        friendly_shot = 0

        # UI Inits
        print_ui_initial(ui_tileset, game_screen.display, GamePlayer, 1)
        score_ui = 0 #initial score, everytime it changes, we update the ui
        trophy_ui = False #initial score, everytime it changes, we update the ui

        ''' TODO: THIS SHOULD BE INSIDE THE NEXT LOOP? '''
        update_ui_gun(ui_tileset, game_screen.display)
        update_ui_jetpack(ui_tileset, game_screen.display)

        # level processing controller
        ended_level = False

        ## Level processing
        while not ended_level:
            # get keys (invetory)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ended_level = True
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT] and GamePlayer.getCurrentState() in [STATE.WALK, STATE.FLY, STATE.JUMP, STATE.CLIMB]:
                        GamePlayer.clearXMovement()
                    elif event.key in [pygame.K_UP, pygame.K_DOWN] and GamePlayer.getCurrentState() in [STATE.FLY, STATE.CLIMB]:
                        GamePlayer.setVelocityY(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key in inv_keys:
                        if GamePlayer.inventoryInput(inv_keys.index(event.key)) and not friendly_shot:
                            friendly_shot = Level.spawnFriendlyFire(GamePlayer.getDirectionX())
                            friendly_shot_x, friendly_shot_y = player_position_x + GamePlayer.getDirectionX().value * WIDTH_OF_MAP_NODE, player_position_y

            # get keys (movement)
            pressed_keys = pygame.key.get_pressed()
            key_map = [0,0,0,0]
            for i, key in enumerate(movement_keys):
                if pressed_keys[key]:
                    key_map[i] = 1
            GamePlayer.movementInput(key_map)

            # update the player position in the level and treat collisions
            if GamePlayer.getCurrentState() != STATE.DESTROY:
                (player_position_x, player_position_y) = GamePlayer.updatePosition(player_position_x, player_position_y, Level)
                
            # update friendly shot position, if there is one
            if friendly_shot:
                friendly_shot_x = friendly_shot.updatePosition(friendly_shot_x, friendly_shot_y, Level)
                if (friendly_shot_x == -1):
                    del friendly_shot
                    friendly_shot = 0

            # if the player ended the level, go on to the next
            if GamePlayer.getCurrentState() == STATE.ENDMAP:
                ended_level = True
                break;
            elif GamePlayer.getCurrentState() == STATE.DESTROY:
                ''' TODO: REFACTOR '''
                if death_timer == -1:
                    DeathPuff.setGfxId(0)
                    GamePlayer.takeLife()
                    death_timer = 120
                
                player_position_y += 0.25
                death_timer -= 1
                
                if death_timer == 0:
                    death_timer = -1
                    game_screen.setXPosition(0)
                    DeathPuff.setGfxId(-1)
                    
                    if (GamePlayer.resetPosAndState() != -1):
                        (player_position_x, player_position_y) = Level.getPlayerSpawnerPosition(0)
                        player_position_x *= WIDTH_OF_MAP_NODE
                        player_position_y *= HEIGHT_OF_MAP_NODE
                    else:
                        ended_level = True
                        game_over = True
                
            # if the player is close enough to one of the screen boundaries, move the screen.
            player_close_to_left_boundary = (player_position_x <= game_screen.getXPositionInPixelsUnscaled() + BOUNDARY_DISTANCE_TRIGGER)
            player_close_to_right_boundary = (player_position_x >= game_screen.getXPositionInPixelsUnscaled() + game_screen.getUnscaledWidth() - BOUNDARY_DISTANCE_TRIGGER)
            reached_level_left_boundary = (game_screen.getXPosition() <= 0)
            reached_level_right_boundary = (game_screen.getXPosition() + game_screen.getWidthInTiles() > Level.getWidth())         

            # move screen left
            if player_close_to_left_boundary and not reached_level_left_boundary:
                game_screen.moveScreenX(Level, -15, tileset)
            # move screen right
            elif player_close_to_right_boundary and not reached_level_right_boundary:
                game_screen.moveScreenX(Level, 15, tileset)
            # not moving (just update the screen)
            else:
                game_screen.printMap(Level, tileset)
                
                if friendly_shot:
                    game_screen.printTile(friendly_shot_x - game_screen.getXPositionInPixelsUnscaled(), friendly_shot_y, friendly_shot.getGraphic(tileset))
                    
                    bullet_bypassed_screen_right_boundary = (friendly_shot_x >= game_screen.getXPositionInPixelsUnscaled() + game_screen.getUnscaledWidth())
                    bullet_bypassed_screen_left_boundary = (friendly_shot_x <= game_screen.getXPositionInPixelsUnscaled())
                    
                    if bullet_bypassed_screen_right_boundary or bullet_bypassed_screen_left_boundary:
                        del friendly_shot
                        friendly_shot = 0
                
                if GamePlayer.getCurrentState() != STATE.DESTROY:
                    # print player accordingly to screen shift
                    game_screen.printPlayer(GamePlayer, player_position_x - game_screen.getXPositionInPixelsUnscaled(), player_position_y, tileset)
                else:
                    # print death puff accordingly to screen shift
                    game_screen.printTile(player_position_x - game_screen.getXPositionInPixelsUnscaled(), player_position_y, DeathPuff.getGraphic(tileset))

            # update UI
            ''' TODO: PUT THIS INSIDE A HELPER FUNCTION? '''
            if score_ui != GamePlayer.score:
                update_ui_score(ui_tileset,game_screen.display,GamePlayer.score)
                score_ui = GamePlayer.score
            if not trophy_ui and GamePlayer.inventory["trophy"] == 1:
                update_ui_trophy(ui_tileset,game_screen.display)
                trophy_ui = True
                
            pygame.display.flip()
            pygame.event.pump()
            clock.tick(200)

        # Onto the next level
        current_level_number += 1

        if current_level_number > 10 and ended_level:
            ''' TODO: CREDITS SCREEN '''
            ended_game = True
        elif ended_level and not game_over:
            showInterpic(current_level_number, game_screen, tileset)
        elif game_over:
            ''' TODO: GAME OVER SCREEN '''
            ended_game = True
            pass
            
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
