from os import listdir
from os.path import isfile, join
import pygame

##################################
## LIST AND STRING MANIPULATION ##
##################################

def head(list):
    return list[0]
    
def tail(list):
    return list[1:]
    
def second(list):
    return head(tail(list))
    
def fourth(list):
    return head(tail(tail(tail(list))))

def isListEmpty(list):
	return (tail(list) == list)
    
def popListLast(list):
	return [] if isListEmpty(tail(list)) else [head(list)] + popListLast(tail(list))
	
def lastFromNonEmpty(list):
	return head(list) if isListEmpty(tail(list)) else last(tail(list))
	
def last(list):
	return "" if isListEmpty(list) else lastFromNonEmpty(list)
    
def appendInLastAux(list_of_strings, new_list_of_strings, element):
	return popListLast(new_list_of_strings) + [last(new_list_of_strings) + element] if isListEmpty(list_of_strings) else appendInLastAux(tail(list_of_strings), new_list_of_strings + [head(list_of_strings)], element)

def appendInLastEntry(list_of_strings, element):
	return appendInLastAux(list_of_strings, [], element)
	
###########################
## FILENAME MANIPULATION ##
##       FOR TILES       ##
###########################
    
def separateString(string, resulting_strings):
	return resulting_strings if isListEmpty(string) else (separateString(tail(string), appendInLastEntry(resulting_strings, head(string))) if (head(string).isdigit() and last(last(resulting_strings)).isdigit()) or (head(string).isalpha() and last(last(resulting_strings)).isalpha()) else separateString(tail(string), resulting_strings + [head(string)]))

def splitStringIntoLettersAndNumbers(string):
	return separateString(string, [])

def graphicPropertiesFromFilename(filename):
	return (head(splitStringIntoLettersAndNumbers(filename)), int(fourth(splitStringIntoLettersAndNumbers(filename))), int(second(splitStringIntoLettersAndNumbers(filename))))

################
## LOAD TILES ##
################

def pygame_image_load(tilepath):
	return pygame.image.load(tilepath).convert_alpha()
	
def convert_tuples_to_dict(list_of_tuples):
    return {tuple[0] : tuple[1:] for tuple in list_of_tuples}
	
def list_tiles(folder):
    return listdir(folder)
    
def save_tile(tile, folder):
    return (graphicPropertiesFromFilename(tile)[0], pygame_image_load(folder + tile), graphicPropertiesFromFilename(tile)[1:][0], graphicPropertiesFromFilename(tile)[1:][1:][0])
	
def save_all_tiles(folder):
	return map(lambda tile: save_tile(tile, folder), list_tiles(folder))

def load_all_tiles():
    return convert_tuples_to_dict(save_all_tiles("tiles/game/")), convert_tuples_to_dict(save_all_tiles("tiles/ui/"))

    