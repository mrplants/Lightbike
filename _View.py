import pygame

def pointInRect(position, rect):
    if position[0] < rect[0] or position[0] > rect[0] + rect[2]:
        return False
    if position[1] < rect[1] or position[1] > rect[1] + rect[3]:
        return False
    return True

class View:
    def __init__(self, size = (100, 100)):
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((0,255,255))
        pass
    
    def layoutBike(self, name, path, color):
#         print "layout path for bike with name: " + name
        pygame.draw.lines(self.screen, color, False, path, 1)
        
    def showReadyButton(self):
        self.readyButtonRect = (200, 200, 100, 100)
        pygame.draw.rect(self.screen, (0, 255, 0), self.readyButtonRect)
        self.font = pygame.font.Font(None, 30)
        self.text = 'Ready?'
        self.image = self.font.render( self.text, 1, (255,0,0))
        self.screen.blit(self.image, (230, 230, 100, 100))
    
    def pointOnReadyButton(self, position):
        return pointInRect(position, self.readyButtonRect)
