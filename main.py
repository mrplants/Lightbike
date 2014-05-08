import pygame, sys
from Board import Board
from View import View
from Bike import Bike
from PlayerConnector import PlayerConnector

pygame.init()

board = Board()
connection = PlayerConnector(board)
bike = Bike(board, connection.ID)
view = View(board.size)

while 1:
    
    #check the events queue
    for event in pygame.event.get():
        #quit game on quit
        if event.type == pygame.QUIT:
            #maybe alert the PlayerConnection that a client has quit?
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                bike.turnLeft()
            if event.key == pygame.K_RIGHT:
                bike.turnRight()
    
    #TODO: lay out the paths for the bikes
    for bikeName in board.bikes:
        view.layoutBike(bikeName, board.bikePaths[bikeName], board.bikeColors[bikeName])
    
    #TODO: tell your own bike to tick, it returns a BikeEvent
    event = bike.tick()
    board.tick()
    
    #TODO: tell the PlayerConnection what the event was
    connection.newEvent(event)