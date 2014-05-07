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
#bikenames = []

#size = (10, 10)
ROWS = 0
COLUMNS = 1

class Board:
    def __init__(self, width = 100, height = 100, bike):
        self.size = (width, height)
        self.bikes = []
        self.bikeColors = {}
        self.bikePaths = {}
        pass