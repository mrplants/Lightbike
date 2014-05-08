import pygame

class View:
    def __init__(self, size = (100, 100)):
        screen = pygame.display.set_mode(size)
        pass
    
    def layoutBike(self, name, path, color):
        print "layout path for bike"