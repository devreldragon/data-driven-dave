import newrelic.agent
import math
import logging

newrelic.agent.initialize('newrelic.ini') #This is required! [RLF]

from classes import *
from functional import *

'''
Interpic
'''

@newrelic.agent.background_task()
def showTitleScreen(screen, tileset, ui_tiles):
    clock = pygame.time.Clock()
    
    # init graphics
    started_game = False
    titlepic_level = Map(1)
    dave_logo = AnimatedTile("davelogo", 0)
    overlay = Scenery("blacktile", 0)
    
    # clear screen on entering
    screen.clearScreen()
    
    # messages
    creator_text = "RECREATED BY ARTHUR, CATTANI AND MURILO"
    professor_text = "PROFESSOR LEANDRO K. WIVES"
    instr1_text = "PRESS SPACE TO START"
    instr2_text = "PRESSING ESC AT ANY MOMENT EXITS"
    
    while not started_game:
        pygame.display.update()
        
        # print level and tiles
        screen.setXPosition(14, titlepic_level.getWidth())
        screen.printMap(titlepic_level, tileset)
        screen.printTitlepicBorder(tileset)
        screen.printTile(104, 0, dave_logo.getGraphic(ui_tiles))   
        screen.printTile(0, BOTTOM_OVERLAY_POS, overlay.getGraphic(ui_tiles))
        
        # print text in center
        screen.printTextAlignedInCenter(creator_text, 47)
        screen.printTextAlignedInCenter(professor_text, 55)
        screen.printTextAlignedInCenter(instr1_text, BOTTOM_OVERLAY_POS + 2)
        screen.printTextAlignedInCenter(instr2_text, BOTTOM_OVERLAY_POS + 11)
        
        # if player pressed escape, exit game; space, start game
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                started_game = True  
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True    # return 0 so we know player pressed escape

        pygame.display.flip()
        clock.tick(200)
        
    # clear screen on exiting
    screen.clearScreen()
        
    return False

@newrelic.agent.background_task()
def showInterpic(completed_levels, screen, GamePlayer, tileset, ui_tileset):
    clock = pygame.time.Clock()
    
    # init graphics
    interpic_level = Map("interpic")
    screen.setXPosition(0, interpic_level.getWidth())    
    screen.printMap(interpic_level, tileset)
    screen.clearBottomUi(ui_tileset)
    
    # init player
    (player_absolute_x, player_absolute_y) = interpic_level.initPlayerPositions(0, GamePlayer)
    GamePlayer.setCurrentState(STATE.WALK)
    GamePlayer.setDirectionX(DIRECTION.RIGHT)
    GamePlayer.setSpriteDirection(DIRECTION.RIGHT)

    # init messages
    intertext = "GOOD WORK! ONLY " + str(NUM_OF_LEVELS - completed_levels + 1) + " MORE TO GO!"
    last_level_text = "THIS IS THE LAST LEVEL!!!"
    finish_text = "YES! YOU FINISHED THE GAME!!"
    
    # keep moving the player right, until it reaches the screen boundary
    player_reached_boundary = (player_absolute_x >= screen.getUnscaledWidth())

    while not player_reached_boundary:
        # if player pressed escape, quit game
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True # return so we treat exiting externally
                
        # update player pos and animation
        player_absolute_x = GamePlayer.movePlayerRight(player_absolute_x)
        GamePlayer.updateAnimator()
        
        # update screen
        screen.printMap(interpic_level, tileset)
        screen.printOverlays(ui_tileset)
        screen.printUi(ui_tileset, GamePlayer, completed_levels-1)
        screen.printPlayer(GamePlayer, player_absolute_x, player_absolute_y, tileset)
        
        # print text accordingly to the number of completed levels
        if completed_levels == NUM_OF_LEVELS + 1:
            screen.printTextAlignedInCenter(finish_text, 54)
        elif completed_levels == NUM_OF_LEVELS:
            screen.printTextAlignedInCenter(last_level_text, 54)
        else:
            screen.printTextAlignedInCenter(intertext, 54)

        player_reached_boundary = (player_absolute_x >= screen.getUnscaledWidth())
        
        pygame.display.flip()
        clock.tick(200)
        
    return False

@newrelic.agent.background_task()
def showWarpZone(completed_levels, screen, GamePlayer, tileset, ui_tileset):
    clock = pygame.time.Clock()
    
    # init graphics
    warp_level = Map("warp")
    screen.setXPosition(0, warp_level.getWidth())    
    screen.printMap(warp_level, tileset)
    screen.clearBottomUi(ui_tileset)
    
    # init player
    (player_absolute_x, player_absolute_y) = warp_level.initPlayerPositions(0, GamePlayer)
    GamePlayer.resetPosAndState()
    GamePlayer.setFallingState()
    GamePlayer.setGfxId(0)
    
    # keep moving the player right, until it reaches the screen boundary
    player_reached_bottom = (player_absolute_y >= screen.getUnscaledHeight())

    while not player_reached_bottom:
        # if player pressed escape, quit game
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True # return so we treat exiting externally
        
        player_absolute_y += 0.5
        
        # update screen
        screen.printMap(warp_level, tileset)        
        screen.printPlayer(GamePlayer, player_absolute_x, player_absolute_y, tileset)
        screen.printOverlays(ui_tileset)
        screen.printUi(ui_tileset, GamePlayer, completed_levels-1)

        player_reached_bottom = (player_absolute_y >= screen.getUnscaledHeight())
        
        pygame.display.flip()
        clock.tick(200)
        
    return False
    
    
@newrelic.agent.background_task()
def getBonusMapping(current_level):
    if current_level == 2: return 6
    elif current_level == 5: return 2
    elif current_level == 6: return 9
    elif current_level == 7: return 10
    elif current_level == 8: return 6
    elif current_level == 9: return 7
    elif current_level == 10: return 1
    elif current_level == 1: return 11
    else: return 1
    
@newrelic.agent.background_task()
def showScores(screen, tileset):
    pass
    
@newrelic.agent.background_task()
def savePlayerScore(player_score, screen, tileset):
    pass
        
@newrelic.agent.background_task()
def showCreditsScreen(screen, tileset):
    pass
   
'''
Game processing stuff
'''
       
'''
Main
'''

def main():
    ##Init pygame
    pygame.init()
    game_screen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    ##Init tiles
    tileset, ui_tileset = load_all_tiles()
    game_open = True
    
    ##Logging test [RLF]
    logging.basicConfig(level=logging.INFO)
    logging.info('This is a sample info message')
    logging.warning('This is a sample warning message')
    logging.error('This is a sample error message')

    ##Game start log message [RLF]
    logging.info('Game started')

    while game_open:
        ##Show title screen
        option = showTitleScreen(game_screen, tileset, ui_tileset)
     
        #if player presses escape, close game
        game_open = not option
        
        ##Init a player
        GamePlayer = Player()
      
        ##Init level and spawner
        current_level_number = 1
        current_spawner_id = 0

        ##Available Keys
        movement_keys = [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]
        inv_keys = [pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT]

        ##Game processing
        ended_game = False

        while not ended_game:
            # init clock and display
            clock = pygame.time.Clock()
            pygame.display.update()

            # build the level and init screen and player positions
            Level = Map(current_level_number)
            (player_position_x, player_position_y) = Level.initPlayerPositions(current_spawner_id, GamePlayer)
            
            spawner_pos_x = Level.getPlayerSpawnerPosition(current_spawner_id)[0]
            game_screen.setXPosition(spawner_pos_x - 10, Level.getWidth())

            # UI Inits
            score_ui = 0 #initial score. Everytime it changes, we update the ui
            jetpack_ui = False
            
            # init other sprites
            death_timer = -1
            friendly_shot = 0

            # level processing controller
            ended_level = False

            ## Level processing
            while not ended_level:
            
                # get keys (inventory)
                for event in pygame.event.get():
                    # stop moving
                    if event.type == pygame.KEYUP:
                        # horizontally
                        if event.key in [pygame.K_LEFT, pygame.K_RIGHT] and GamePlayer.getCurrentState() in [STATE.WALK, STATE.FLY, STATE.JUMP, STATE.CLIMB]:
                            GamePlayer.clearXMovement()
                        # vertically
                        elif event.key in [pygame.K_UP, pygame.K_DOWN] and GamePlayer.getCurrentState() in [STATE.FLY, STATE.CLIMB]:
                            GamePlayer.setVelocityY(0)
                    # hit a key
                    elif event.type == pygame.KEYDOWN:
                        # quit game
                        if event.key == pygame.K_ESCAPE:
                            game_open = False
                            ended_level = True
                            ended_game = True

                            # Write game stats to log [RLF]
                            logging.info('Game ended with score %s', GamePlayer.score)

                            # Record custom New Relic event [RLF]
                            event_type = "GameComplete" 
                            params = {'current_level': current_level_number, 'player_score': GamePlayer.score} 
                            newrelic.agent.record_custom_event(event_type, params, application=application)

                        # use something from the inventory
                        elif event.key in inv_keys:
                            if GamePlayer.inventoryInput(inv_keys.index(event.key)) and not friendly_shot:
                                friendly_shot = Level.spawnFriendlyFire(GamePlayer.getSpriteDirection())
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
                    (player_position_x, player_position_y) = GamePlayer.updatePosition(player_position_x, player_position_y, Level, game_screen.getUnscaledHeight())
                    
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
                # if the player died, spawn death puff and respawn player (if he has enough lives)
                elif GamePlayer.getCurrentState() == STATE.DESTROY:
                    if death_timer == -1:
                        GamePlayer.takeLife()
                        DeathPuff = AnimatedTile("explosion", 0)
                        death_timer = 120
                    
                    player_position_y += 0.25
                    death_timer -= 1
                    
                    if death_timer == 0:
                        death_timer = -1
                        game_screen.setXPosition(Level.getPlayerSpawnerPosition(current_spawner_id)[0] - 10, Level.getWidth())
                        del DeathPuff
                        
                        if (GamePlayer.resetPosAndState() != -1):
                            (player_position_x, player_position_y) = Level.getPlayerSpawnerPosition(current_spawner_id)
                            player_position_x *= WIDTH_OF_MAP_NODE
                            player_position_y *= HEIGHT_OF_MAP_NODE
                        else:
                            ended_level = True
                            ended_game = True

                            # Write game stats to log [RLF]
                            logging.info('Game ended with score %s', GamePlayer.score)

                            # Record custom New Relic event [RLF]
                            event_type = "GameComplete" 
                            params = {'current_level': current_level_number, 'player_score': GamePlayer.score} 
                            newrelic.agent.record_custom_event(event_type, params, application=application)
                    
                # if the player is close enough to one of the screen boundaries, move the screen.
                player_close_to_left_boundary = (player_position_x <= game_screen.getXPositionInPixelsUnscaled() + BOUNDARY_DISTANCE_TRIGGER)
                player_close_to_right_boundary = (player_position_x >= game_screen.getXPositionInPixelsUnscaled() + game_screen.getUnscaledWidth() - BOUNDARY_DISTANCE_TRIGGER)
                reached_level_left_boundary = (game_screen.getXPosition() <= 0)
                reached_level_right_boundary = (game_screen.getXPosition() + game_screen.getWidthInTiles() > Level.getWidth())         

                # move screen left
                if player_close_to_left_boundary and not reached_level_left_boundary:
                    game_screen.moveScreenX(Level, -15, tileset, ui_tileset, GamePlayer, current_level_number)
                # move screen right
                elif player_close_to_right_boundary and not reached_level_right_boundary:
                    game_screen.moveScreenX(Level, 15, tileset, ui_tileset, GamePlayer, current_level_number)
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
                    elif not ended_game:
                        # print death puff accordingly to screen shift
                        game_screen.printTile(player_position_x - game_screen.getXPositionInPixelsUnscaled(), player_position_y, DeathPuff.getGraphic(tileset))

                # update UI
                game_screen.printOverlays(ui_tileset)
                game_screen.printUi(ui_tileset, GamePlayer, current_level_number)
                
                if not ended_level:
                    if GamePlayer.inventory["gun"] == 1:
                        game_screen.updateUiGun(ui_tileset)
                    if GamePlayer.inventory["jetpack"] == 1 or jetpack_ui :
                        game_screen.updateUiJetpack(ui_tileset, GamePlayer.inventory["jetpack"])
                        jetpack_ui = True
                    if GamePlayer.inventory["trophy"] == 1:
                        game_screen.updateUiTrophy(ui_tileset)
                        
                
                if score_ui != GamePlayer.score:
                    game_screen.updateUiScore(GamePlayer.score, ui_tileset)
                    score_ui = GamePlayer.score                
                    
                pygame.display.flip()
                pygame.event.pump() 
                clock.tick(200)

            # Record custom New Relic event [RLF]
            event_type = "LevelUp" 
            params = {'current_level': current_level_number, 'player_score': GamePlayer.score} 
            newrelic.agent.record_custom_event(event_type, params, application=application)

            # Onto the next level
            GamePlayer.clearInventory()
            if (player_position_x == -2):
                current_level_number = getBonusMapping(current_level_number)
                current_spawner_id = 1
            elif (current_spawner_id == 1):
                current_level_number = getBonusMapping(current_level_number)
                current_spawner_id = 0
            else:
                current_level_number += 1

            GamePlayer.setCurrentLevelNumber(current_level_number)
                
            if current_level_number > NUM_OF_LEVELS and ended_level and not ended_game:
                showCreditsScreen(game_screen, tileset)
                ended_game = True

                # Write game stats to log [RLF]
                logging.info('Game ended with score %s', GamePlayer.score)

                # Record custom New Relic event [RLF]
                event_type = "GameComplete" 
                current_level_number -= 1
                params = {'current_level': current_level_number, 'player_score': GamePlayer.score} 
                newrelic.agent.record_custom_event(event_type, params, application=application)

            elif ended_level and current_spawner_id == 1:
                option = showWarpZone(current_level_number, game_screen, GamePlayer, tileset, ui_tileset)
                ended_game = option
                game_open = not option
            elif ended_level and not ended_game:
                option = showInterpic(current_level_number, game_screen, GamePlayer, tileset, ui_tileset)
                ended_game = option
                game_open = not option
                
        savePlayerScore(GamePlayer.getScore(), game_screen, tileset)
        showScores(game_screen, tileset)
                
    pygame.quit()
    quit()

application = newrelic.agent.register_application(timeout=5) # force New Relic agent registration [RLF]

if __name__ == "__main__":
    main()

newrelic.agent.shutdown_agent(timeout=2.5) # shutdown New Relic agent [RLF]
