from os import listdir
from os.path import isfile, join
import pygame

'''
Tile and gfxs
'''

## separate a string into letters and numbers
def listEmpty(list):
	return (list == [] or list == "")

def popLast(list):
	return [] if listEmpty(list[1:]) else [list[0]] + popLast(list[1:])
	
def getLastFromNonEmptyList(list):
	return list[0] if listEmpty(list[1:]) else getLastFromNonEmptyList(list[1:])
	
def getLastFromList(list):
	return "" if listEmpty(list) else getLastFromNonEmptyList(list)
	
def appendInLastAux(list_of_strings, new_list_of_strings, element):
	return popLast(new_list_of_strings) + [getLastFromList(new_list_of_strings) + element] if listEmpty(list_of_strings) else appendInLastAux(list_of_strings[1:], new_list_of_strings + [list_of_strings[0]], element)

def appendInLast(list_of_strings, element):
	return appendInLastAux(list_of_strings, [], element)
	
def separateString(string, resulting_strings):
	return resulting_strings if listEmpty(string) else (separateString(string[1:], appendInLast(resulting_strings, string[0])) if ((string[0].isdigit() and getLastFromList(getLastFromList(resulting_strings)).isdigit()) or (string[0].isalpha() and getLastFromList(getLastFromList(resulting_strings)).isalpha())) else separateString(string[1:], resulting_strings + [string[0]]))

def splitStringIntoLettersAndNumbers(string):
	return separateString(string, [])

## get name and size properties from filename
def graphicPropertiesFromFilename(filename):
	return (splitStringIntoLettersAndNumbers(filename)[0], int(splitStringIntoLettersAndNumbers(filename)[3]), int(splitStringIntoLettersAndNumbers(filename)[1]))

## load all game tiles
def pygame_image_load(tilepath):
	return pygame.image.load(tilepath).convert_alpha()
	
# must be procedural
''' TODO: TRY TO CONVERT THIS TO FUNCTIONAL '''
def convert_tuples_to_dict(list_of_tuples):
	dict = {}
	for tuple in list_of_tuples:
		dict[tuple[0]] = tuple[1:]
	return dict
	
''' TODO: REFACTOR CONSIDERING THE STRING OF THE PATH '''
	
def list_game_tiles():
	return listdir("tiles/game/")
	
def save_game_tile(tile):
	return (graphicPropertiesFromFilename(tile)[0], pygame_image_load("tiles/game/" + tile), graphicPropertiesFromFilename(tile)[1], graphicPropertiesFromFilename(tile)[2])
	
def save_all_game_tiles():
	return map(save_game_tile, list_game_tiles())
	
def list_ui_tiles():
	return listdir("tiles/ui/")
	
def save_ui_tile(tile):
	return (graphicPropertiesFromFilename(tile)[0], pygame_image_load("tiles/ui/" + tile), graphicPropertiesFromFilename(tile)[1], graphicPropertiesFromFilename(tile)[2])
	
def save_all_ui_tiles():
	return map(save_ui_tile, list_ui_tiles())
	
def load_all_tiles():
	return convert_tuples_to_dict(save_all_game_tiles()), convert_tuples_to_dict(save_all_ui_tiles())