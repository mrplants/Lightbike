import pygame, sys
from _Board import Board
from _View import View
from _Bike import Bike
from PlayerConnector import PlayerConnector
# import time

pygame.init()

board = Board(500, 500)
connection = PlayerConnector(board)
bike = Bike(board, connection.id)
view = View(board.size)

while 1:
    
    if not board.start:
        view.showReadyButton()
        #check the events queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #maybe alert the PlayerConnection that a client has quit?
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if view.pointOnReadyButton(pos):
                    print "ready"
                    connection.ready()
    else:        
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
        
        #lay out the paths for the bikes
        for bikeName in board.bikes:
            view.layoutBike(bikeName, board.bikePaths[bikeName], board.bikeColors[bikeName])
        
        #tell your own bike to tick, it returns a BikeEvent
        event = bike.tick()
        board.newEvent(event)
        board.tick()
        
        #tell the PlayerConnection what the event was
        connection.newEvent(event)
    #     time.sleep(0.1)
    pygame.display.flip()