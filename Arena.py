# Arena.py

# Programming Paradigms
# Maribeth Rauh and Sean Fitzgerald
# 5/7/2014

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue


# Tell bikes what color they are

# Track connections and count
# Accept incoming connections from bikes
# Listen to when bikes turn and die

# Tell other bikes when these things happen

PLAYER_PORT = 9000

# The actual connection with the player that will send and receive data
class PlayerConnection(Protocol):
    def __init__(self, callback):
        self.connectionCallback = callback # Player Connection will use this callback to let Arena handle all data and connections
        self.id = -1 # ID is necessary for Arena to know who is sending it incoming data

    def setID(self, newID):
        self.id = newID

    # Autmatically called when the player first connects
    def connectionMade(self):
        print "player connected"
        self.connectionCallback("player joined", self)

    def connectionLost(self):
        self.connectionCallback("connection lost", self)

    # Automatically called when the player sends data over the conneciton
    def dataReceived(self, data):
        print "data from player " + str(self.id)
        self.connectionCallback("new data", data)

    # Writes a message to the player
    # TODO pass id of player the message is about
    def sendData(self, message):
        self.transport.write(message)


# Factory for the connection with the Arena
#   This will create an instance of the PlayerConnection class that will be used during communication 
class PlayerConnectionFactory(ClientFactory):
    def __init__(self, callback):
        self.connectionCallback = callback

    def startedConnecting(self, connector):
        print "A new player is connecting..."

    def buildProtocol(self, address):
        # Arena is passed so that player connections can be kept in the arena's list of players
        return PlayerConnection(self.connectionCallback)


class Arena():
    def __init__(self):
        # List of players used for updating all players on the other players
        self.players = {}

        # Listens for incoming connections from players joining the game
        reactor.listenTCP(PLAYER_PORT, PlayerConnectionFactory(self.connectionHandler))
        print "Waiting for connections..."
        reactor.run() # Waits forever for connections

    # When a player connects or sends data, this callback will parse and handle the event/data
    def connectionHandler(self, message, data):
        if message == "player joined":
            # Create a unique ID for the player and set it accordingly
            id = len(self.players) + 1
            data.setID(id)
            # Added to the list of players for future communication
            self.players[id] = data
            # Let players know a new bike joined
            self.broadcastMessage(message, id)
        elif message == "new data":
            pass
        elif message == "connection lost":
            self.broadcastMessage(message, id)
            del self.players[id] # Deletes this player from the dictionary of players

    # Calls the sendData method for every player except the one the message originated from
    def broadcastMessage(self, message, id):
        for player in self.players:
            if player != id:
                self.players[player].sendData(message)



if __name__ == "__main__":
    arena = Arena() # By instantiating the Arena object, it starts listening for connections
