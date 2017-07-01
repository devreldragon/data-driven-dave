from classes import *
from os import listdir
from os.path import isfile, join
import pygame

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
    GamePlayer = Level.getPlayer()
    playerPosition = Level.getPlayerPosition()
    player_position_x = WIDTH_OF_MAP_NODE * playerPosition[0]
    player_position_y = HEIGHT_OF_MAP_NODE * playerPosition[1]

    #clear the residue left by player spawner
    ''' TODO: INVESTIGATE THIS '''
    Level.clearPlayerPosition()

    #the X position, in the map, where the screen starts
    ''' TODO: PLAYER MIGHT START IN THE MIDDLE OF THE MAP (Bonus rooms) '''
    screen_x_position = 0

    return (Level, GamePlayer, player_position_x, player_position_y, screen_x_position)

def tileFromText(text_tile):
    #if the tile has an index, store it
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
    if (index >= num_of_blocks):
        ErrorInvalidValue()

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

        tile_table[tile_name] = (image, tile_height, tile_width)

    return tile_table

'''
Screen
'''

## print a tile in the display screen
def printTileInDisplay(tile, x, y, display, tileset, printing_sprite=False):
    graphic_set = tileset[tile.getId()]

    set_width = graphic_set[2]
    set_height = graphic_set[1]
    set_image = graphic_set[0]
    set_image_width = set_image.get_rect().size[0]
    number_of_tiles_in_image = int(set_image_width / set_width)

    tile_graphic = cropBlockFromGraphic(set_image, tile.getGfxId(), set_width, set_height, number_of_tiles_in_image)

    if printing_sprite:
        display_x = x * TILE_SCALE_FACTOR
        display_y = y * TILE_SCALE_FACTOR
    else:
        display_x = WIDTH_OF_MAP_NODE * x * TILE_SCALE_FACTOR
        display_y = HEIGHT_OF_MAP_NODE * y * TILE_SCALE_FACTOR

    display.blit(tile_graphic, (display_x, display_y))

def printPlayerInDisplay(player, x, y, display, tileset, printing_sprite=False):
    graphic_set = tileset[player.getId()]

    set_width = graphic_set[2]
    set_height = graphic_set[1]
    set_image = graphic_set[0]
    set_image_width = set_image.get_rect().size[0]
    number_of_tiles_in_image = int(set_image_width / set_width)

    tile_graphic = cropBlockFromGraphic(set_image, player.getGfxId(), set_width, set_height, number_of_tiles_in_image)
    if (player.direction_x == direction.RIGHT):
        player.flip_sprite = True
    elif (player.direction_x == direction.LEFT):
        player.flip_sprite = False


    if (player.flip_sprite):
        tile_graphic = pygame.transform.flip(tile_graphic,1,0);

    if printing_sprite:
        display_x = x * TILE_SCALE_FACTOR
        display_y = y * TILE_SCALE_FACTOR
    else:
        display_x = WIDTH_OF_MAP_NODE * x * TILE_SCALE_FACTOR
        display_y = HEIGHT_OF_MAP_NODE * y * TILE_SCALE_FACTOR

    display.blit(tile_graphic, (display_x, display_y))

## display map in pygame
def printMapInDisplay(map, display, tileset, screen_x_position):
    for y, row in enumerate(map.getNodeMatrix()):
        for x, col in enumerate(row):
            tile = map.getNode(x,y).getTile()
            # won't print player nor the first line, neither other tiles that aren't in the screen
            if (tile.getId() != "player") and isInScreen(x, screen_x_position) and (y > 0):
                adjusted_x = x - screen_x_position
                printTileInDisplay(tile, adjusted_x, y, display, tileset)

#function used for scrolling the screen
def moveScreenX(map, display, tileset, old_screen_x, scroll_increment):
    screen_shift = 0
    reached_level_left_boundary = (old_screen_x + screen_shift <= 0)
    reached_level_right_boundary = (old_screen_x + screen_shift + SCREEN_WIDTH_TILES >= map.getWidth())

    #going left
    while (screen_shift > scroll_increment) and not reached_level_left_boundary:
        printMapInDisplay(map, display, tileset, old_screen_x + screen_shift)
        pygame.display.flip()

        screen_shift -= SCREEN_SHIFTING_VELOCITY
        reached_level_left_boundary = (old_screen_x + screen_shift <= 0)

    #going right
    while (screen_shift < scroll_increment) and not reached_level_right_boundary:
        printMapInDisplay(map, display, tileset, old_screen_x + screen_shift)
        pygame.display.flip()

        screen_shift += SCREEN_SHIFTING_VELOCITY
        reached_level_right_boundary = (old_screen_x + screen_shift + SCREEN_WIDTH_TILES >= map.getWidth())

    return old_screen_x + screen_shift

#check if a given point x is in screen
def isInScreen(x, screen_x):
    return (x >= screen_x) and (x < screen_x + SCREEN_WIDTH_TILES)

def InterpicScreen(completed_levels, display, tileset):
    Interpic = BuildLevel("interpic")

    clock = pygame.time.Clock()

    printMapInDisplay(Interpic, display, tileset, 0)

    #init player
    player = Interpic.getPlayer()
    playerPosition = Interpic.getPlayerPosition()
    player_position_x = WIDTH_OF_MAP_NODE * playerPosition[0]
    player_position_y = HEIGHT_OF_MAP_NODE * playerPosition[1]

    Interpic.clearPlayerPosition()

    #keep moving the player right, until it reaches the screen boundary
    player_reached_boundary = (player_position_x >= Interpic.getWidth() * WIDTH_OF_MAP_NODE)

    ''' TODO: ANIMATION '''
    while not player_reached_boundary:
        player_position_x += player.getMaxSpeedX() * player.getXSpeedFactor()

        #print map
        printMapInDisplay(Interpic, display, tileset, 0)
        #print player
        printTileInDisplay(player, player_position_x, player_position_y, display, tileset, True)

        player_reached_boundary = (player_position_x >= Interpic.getWidth() * WIDTH_OF_MAP_NODE)

        pygame.display.flip()
        clock.tick(200)

'''
Pygame inits
'''

def init_display():
    display = pygame.display.set_mode((SCREEN_WIDTH * TILE_SCALE_FACTOR, SCREEN_HEIGHT * TILE_SCALE_FACTOR))
    display.fill((0, 0, 0))

    return display


def main():
    ##Init pygame
    pygame.init()
    game_display = init_display()

    ##Init tiles
    ''' TODO: UNIFY '''
    tileset = load_game_tiles()
    ui_tileset = load_ui_tiles()

    ##Init game
    ended_game = False

    ''' TODO: TITLE SCREEN '''
    current_level_number = 5

    ##Available Keys
    movement_keys = [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]
    inv_keys = [pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT]

    ##Game processing
    while not ended_game:
        # init stuff
        clock = pygame.time.Clock()
        pygame.display.update()

        # build the level
        (Level, GamePlayer, player_position_x, player_position_y, screen_x_position) = initLevel(current_level_number)

        # UI Inits
        print_ui_initial(ui_tileset, game_display, GamePlayer, 1)
        score_ui = 0 #initial score, everytime it changes, we update the ui
        trophy_ui = False #initial score, everytime it changes, we update the ui

        ''' TODO: THIS SHOULD BE INSIDE THE NEXT LOOP? '''
        update_ui_gun(ui_tileset, game_display)
        update_ui_jetpack(ui_tileset, game_display)

        # level processing controller
        ended_level = False

        ## Level processing
        while not ended_level:
            # get keys (invetory)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ended_level = True
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT] and GamePlayer.getCurrentState() in [GamePlayer.state.WALK, GamePlayer.state.FLY, GamePlayer.state.JUMP]:
                        GamePlayer.clearXMovement()
                    elif event.key in [pygame.K_UP, pygame.K_DOWN] and GamePlayer.getCurrentState() in [GamePlayer.state.FLY, GamePlayer.state.CLIMB]:
                        GamePlayer.setVelocityY(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key in inv_keys:
                        GamePlayer.inventoryInput(inv_keys.index(event.key))

            # get keys (movement)
            pressed_keys = pygame.key.get_pressed()
            key_map = [0,0,0,0]
            for i, key in enumerate(movement_keys):
                if pressed_keys[key]:
                    key_map[i] = 1
            GamePlayer.movementInput(key_map)

            # update the player position in the level and treat collisions
            (player_position_x, player_position_y) = GamePlayer.updatePosition(player_position_x, player_position_y, Level)

            # if the player ended the level, go on to the next
            if GamePlayer.getCurrentState() == GamePlayer.state.ENDMAP:
                ended_level = True
                break;

            # if the player is close enough to one of the screen boundaries, move the screen.
            player_close_to_left_boundary = (player_position_x <= WIDTH_OF_MAP_NODE * screen_x_position + BOUNDARY_DISTANCE_TRIGGER)
            player_close_to_right_boundary = (player_position_x >= WIDTH_OF_MAP_NODE * screen_x_position + SCREEN_WIDTH - BOUNDARY_DISTANCE_TRIGGER)
            reached_level_left_boundary = (screen_x_position <= 0)
            reached_level_right_boundary = (screen_x_position + SCREEN_WIDTH_TILES > Level.getWidth())

            # move screen left
            if player_close_to_left_boundary and not reached_level_left_boundary:
                screen_x_position = moveScreenX(Level, game_display, tileset, screen_x_position, -15)
            # move screen right
            elif player_close_to_right_boundary and not reached_level_right_boundary:
                screen_x_position = moveScreenX(Level, game_display, tileset, screen_x_position, 15)
            # not moving (just update the screen)
            else:
                printMapInDisplay(Level, game_display, tileset, screen_x_position)
                # print player accordingly to screen shift
                ''' TODO: REFACTOR? '''
                printPlayerInDisplay(GamePlayer, player_position_x - WIDTH_OF_MAP_NODE * screen_x_position, player_position_y, game_display, tileset, True)

            # update UI
            ''' TODO: PUT THIS INSIDE A HELPER FUNCTION? '''
            if score_ui != GamePlayer.score:
                update_ui_score(ui_tileset,game_display,GamePlayer.score)
                score_ui = GamePlayer.score
            if not trophy_ui and GamePlayer.inventory["trophy"] == 1:
                update_ui_trophy(ui_tileset,game_display)
                trophy_ui = True

            pygame.display.flip()
            pygame.event.pump()
            clock.tick(200)

        # Onto the next level
        current_level_number += 1

        if current_level_number > 10:
            ''' TODO: CREDITS SCREEN '''
            ended_game = True
        else:
            InterpicScreen(current_level_number, game_display, tileset)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
