from _BikeEvent import BikeEvent
import _BikeEvent

RIGHT = "right"
LEFT = "left"
STRAIGHT = "straight"

class Bike:
    def __init__(self, board, name):
        self.board = board
        self.nextMove = STRAIGHT
        self.name = name
        pass
    
    def turnRight(self):
        self.nextMove = RIGHT
        
    def turnLeft(self):
        self.nextMove = LEFT
        
    def tick(self): #creates a new bike event and returns it to the main.
        if self.nextMove == RIGHT:
            bikeEvent = BikeEvent(_BikeEvent.RIGHT_TURN)
        elif self.nextMove == LEFT:
            bikeEvent = BikeEvent(_BikeEvent.LEFT_TURN)
        elif self.nextMove == STRAIGHT:
            check = self.board.checkStraight(self.name)
            if check:
                bikeEvent = BikeEvent(_BikeEvent.CRASH)
            else:
                bikeEvent = BikeEvent(_BikeEvent.STRAIGHT)   
        self.nextMove = STRAIGHT
        return bikeEvent