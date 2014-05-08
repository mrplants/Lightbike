STRAIGHT = "straight"
RIGHT_TURN = "right turn"
LEFT_TURN = "left turn"
CRASH = "crash"

class BikeEvent:
    def __init__(self, reason, id, position):
        self.reason = reason
        self.id = id
        self.position = position
        pass