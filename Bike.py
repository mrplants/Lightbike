import Board

RIGHT = "right"
LEFT = "left"
STRAIGHT = "straight"

class Bike:
    def __init__(self,board , name):
        self.board = board
        self.nextMove = STRAIGHT
        self.name = name
        pass
    
    def turnRight(self):
        self.nextMove = RIGHT
        
    def turnLeft(self):
        self.nextMove = LEFT
        
    def tick(self):
        if self.nextMove == RIGHT:
            self.board.turnBikeRight(self.name)
        elif self.nextMove == LEFT:
            self.board.turnBikeLeft(self.name)