# Arena.py

# Programming Paradigms
# Maribeth Rauh and Sean Fitzgerald
# 5/7/2014

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue


# Tell bikes what color they are

# Track connections and count them
# Accept incoming connections from bikes
# Listen to when bikes turn and die

# Tell other bikes when these things happen

PLAYER_PORT = 9000

# Messages
READY = "ready"
NEW_PLAYER = "player joined"
CONN_LOST = "connection lost"
BIKE_EVENT = "bike event"
START_GAME = "start"

# The actual connection with the player that will send and receive data
class PlayerConnection(Protocol):
    def __init__(self, callback):
        self.connectionCallback = callback # Player Connection will use this callback to let Arena handle all data and connections
        self.id = -1 # ID is necessary for Arena to know who is sending it incoming data
        self.ready = False

    def setID(self, newID):
        self.id = newID

    def pickColor(self):
        return (255, 0, 0)

    # Autmatically called when the player first connects
    def connectionMade(self):
        print "player connected"
        data = {}
        data['id'] = self.id
        data['message'] = NEW_PLAYER
        data['color'] = self.pickColor()
        self.connectionCallback(message, self, data)

    def connectionLost(self):
        self.connectionCallback(CONN_LOST, self, None)

    # Automatically called when the player sends data over the conneciton
    def dataReceived(self, data):
        print "data from player " + str(self.id)
        if data == READY:
            self.ready = True
            self.connectionCallback(READY, self, None)
        else:
            self.connectionCallback(BIKE_EVENT, self, data)

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
    def connectionHandler(self, message, player, data):
        if message == NEW_PLAYER:
            # Create a unique ID for the player and set it accordingly
            ID = len(self.players) + 1
            player.setID(ID)
            # Added to the list of players for future communication
            self.players[ID] = player
            # Alerts all other players that a new bike joined
            self.broadcastMessage(data, ID)

        elif message == READY:
            startGame = True
            for player in self.players:
                if not self.players[player].ready:
                    startGame = False

            if startGame:
                self.broadcastMessage(START_GAME, player.id)

        elif message == BIKE_EVENT:
            # Passes the BikeEvent received to all other players
            self.broadcastMessage(data, player.id)

        elif message == CONN_LOST:
            # Alerts other players that one has lost its connection
            self.broadcastMessage(message, ID)
            # Deletes this player from the dictionary of players
            del self.players[ID]

        else:
            print "Error: unrecognized message"

    # Calls the sendData method for every player except the one the message originated from
    def broadcastMessage(self, message, ID):
        data = {}
        data['message'] = message
        data['id'] = ID
        for player in self.players:
            if player != ID:

                self.players[player].sendData(data)



if __name__ == "__main__":
    arena = Arena() # By instantiating the Arena object, it starts listening for connections
