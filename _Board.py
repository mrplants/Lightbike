import math
from _BikeEvent import BikeEvent
import _BikeEvent

# the game board is the logic that remembers where the paths from each bike.

#main data structure. key = bike_name, value = array of bike previous locations (tuple with first value Row, second value Column)
#bikePaths = {}
ROW = 0
COLUMN = 1

#data structure to store bike path colors. key = bike_name, value = tuple with three values(R, G, B)
#pathColors = {}
RED = 0
GREEN = 1
BLUE = 2

#bike names, for iterating through the other dictionaries
#bikeNames = []

#size = (10, 10)
ROWS = 0
COLUMNS = 1

#bike Directions. dictionary with key = bike name and value = direction
NORTH = "north"
SOUTH = "south"
EAST = "east"
WEST = "west"

class Board:
    def __init__(self, width = 100, height = 100):
        self.size = (width, height)
        self.bikes = []
        self.bikeColors = {}
        self.bikePaths = {}
        self.bikeDirections = {}
        
        self.countD = 0
        self.countN = 1
        self.start = False
        
    def addBike(self, bikeName, color):
        print "new bike: " + bikeName
        self.countN = self.countN + 2
        if self.countN >= self.countD:
            self.countN = 1
            self.countD = self.countD + 1
        ratio = float(self.countN) / math.pow(2, self.countD)
        print "bike ratio" + str(ratio)
        self.bikes.append(bikeName)
        self.bikeDirections[bikeName] = NORTH
        self.bikePaths[bikeName] = [(self.size[ROW]/2, self.size[COLUMN] * float(ratio)), (self.size[ROW]/2, self.size[COLUMN] * float(ratio))]
        self.bikeColors[bikeName] = color
    
    def newEvent(self, event):
        if event.reason == _BikeEvent.RIGHT_TURN:
            self.turnBikeRight(event.id)
        elif event.reason == _BikeEvent.LEFT_TURN:
            self.turnBikeLeft(event.id)
        elif event.reason == _BikeEvent.CRASH:
            print "CRASH: " + event.id
            self.bikes.remove(event.id)
    
    def turnBikeRight(self, bikeName):
        if self.bikeDirections[bikeName] == NORTH:
            self.bikeDirections[bikeName] = EAST
        elif self.bikeDirections[bikeName] == SOUTH:
            self.bikeDirections[bikeName] = WEST
        elif self.bikeDirections[bikeName] == EAST:
            self.bikeDirections[bikeName] = SOUTH
        elif self.bikeDirections[bikeName] == WEST:
            self.bikeDirections[bikeName] = NORTH
    
    def turnBikeLeft(self, bikeName):
        if self.bikeDirections[bikeName] == NORTH:
            self.bikeDirections[bikeName] = WEST
        elif self.bikeDirections[bikeName] == SOUTH:
            self.bikeDirections[bikeName] = EAST
        elif self.bikeDirections[bikeName] == EAST:
            self.bikeDirections[bikeName] = NORTH
        elif self.bikeDirections[bikeName] == WEST:
            self.bikeDirections[bikeName] = SOUTH
    
    def tick(self):
        for bikeName in self.bikes:
            self.bikePaths[bikeName].append(self.nextPosition(self.bikePaths[bikeName][-1], self.bikeDirections[bikeName]))

        
    def checkStraight(self, bikeName):
        nextPosition = self.nextPosition(self.bikePaths[bikeName][-1], self.bikeDirections[bikeName])
        for bikeName in self.bikes:
            for position in self.bikePaths[bikeName]:
                if nextPosition == position:
                    return False
        
        if not self.positionOnBoard(nextPosition):
            return False
        
        return True
    
    def positionOnBoard(self, position):
        if position[ROW] >= self.size[ROW] or position[ROW] < 0:
            return False
        if position[COLUMN] >= self.size[COLUMN] or position[COLUMN] < 0:
            return False
        return True
    
    def nextPosition(self, position, direction):
        if direction == NORTH:
            return(position[ROW] - 1, position[COLUMN])
        elif direction == SOUTH:
            return (position[ROW] + 1, position[COLUMN])
        elif direction == EAST:
            return (position[ROW], position[COLUMN] + 1)
        elif direction == WEST:
            return (position[ROW], position[COLUMN] - 1)

    def bikePosition(self, name): #returns the position of the bike with the name passed in
        return self.bikePaths[name][-1]
    
    def startGame(self):
        self.start = True