import math

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
        print "bike location: " + str(self.bikePaths[bikeName][-1])
        self.bikeColors[bikeName] = color
    
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
            print "added to bike path"
            for node in self.bikePaths[bikeName]:
                print "bike location: " + str(node)
            self.bikePaths[bikeName].append(self.nextPosition(self.bikePaths[bikeName][-1], self.bikeDirections[bikeName]))

        
    def checkStraight(self, bikeName):
        nextPosition = self.nextPosition(self.bikePaths[bikeName][-1], self.bikeDirections[bikeName])
        for bikeName in self.bikes:
            for position in self.bikePaths[bikeName]:
                if nextPosition == position:
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
