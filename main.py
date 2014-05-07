import pygame, sys
import Board
import View
import BikeEvent, Bike
# import PlayerConnection

pygame.init()

board = Board()

view = View(board.size)

while 1:
    
    #check the events queue
    for event in pygame.event.get():
        #quit game on quit
        if event.type == pygame.QUIT:
            #TODO: alert the PlayerConnection that a client has quit
            sys.exit()
    
    #TODO: lay out the paths for the bikes
    
    #TODO: lay out the current bikes
    
    #TODO: tell your own bike to increment, it returns a BikeEvent
    
    #TODO: tell the PlayerConnection what the event was