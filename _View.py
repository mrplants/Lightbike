import pygame

class View:
    def __init__(self, size = (100, 100)):
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((255,255,255))
        pass
    
    def layoutBike(self, name, path, color):
#         print "layout path for bike with name: " + name
        pygame.draw.lines(self.screen, color, False, path, 1)