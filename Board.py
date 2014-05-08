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
        self.countN = self.countN + 2
        if self.countN >= self.countD:
            self.countN = 1
            self.countD = self.countD + 1
        ratio = float(self.countN) / math.pow(2, self.countD)
        print "bike ratio" + str(ratio)
        self.bikes.append(bikeName)
        self.bikeDirections[bikeName] = NORTH
        self.bikePaths[bikeName] = [(self.size[ROW]/2, self.size[COLUMN] * float(ratio))]
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
            position = self.bikePaths[bikeName][-1]
            if self.bikeDirections[bikeName] == NORTH:
                self.bikePaths[bikeName].append((position[ROW] - 1, position[COLUMN]))
            elif self.bikeDirections[bikeName] == SOUTH:
                self.bikePaths[bikeName].append((position[ROW] + 1, position[COLUMN]))
            elif self.bikeDirections[bikeName] == EAST:
                self.bikePaths[bikeName].append((position[ROW], position[COLUMN] + 1))
            elif self.bikeDirections[bikeName] == WEST:
                self.bikePaths[bikeName].append((position[ROW], position[COLUMN] - 1))
