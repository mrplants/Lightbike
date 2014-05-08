# PlayerConnector.py

# Programming Paradigms
# Maribeth Rauh and Sean Fitzgerald
# 5/7/2014

# This class handles the player's connection and information transfer to and from the Arena backend
#       It initiaties a connection with Arena
#       Updates the Arena about its turns and when it dies
#       Recieves information from the Arena about the other player's turns and deaths

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from _BikeEvent import BikeEvent

PLAYER_PORT = 9000
ARENA_IP_ADDRESS = "student00.cse.nd.edu"

# The actual connection with the Arena that will send and receive data
class PlayerConnection(Protocol):
    def __init__(self, callback):
        self.connectionCallback = callback

    # To Arena
    def connectionMade(self):
        print 'Connected to Arena'

    # From Arena
    def dataReceived(self, data):
        # Check for non-event messages
        # Pass the BikeEvent from some other player to this player's board
        self.board.newEvent(data)

    # To Arena to update it about things happening to this player
    #   Will be sending BikeEvents
    def sendData(self, message):
        self.transport.write(message)


# Factory for the connection with the Arena
#   This will create an instance of the PlayerConnection class that will be used during communication 
class PlayerConnectionFactory(ClientFactory):
    def startedConnecting(self, connector):
        print "Joining the arena..."

    def buildProtocol(self, address):
        return PlayerConnection()


# High level class that contains the factory and protocol that will set up and then be the connection with the arena
class PlayerConnector():
    def __init__(self, board):
        self.id = "connector"
        self.board = board
        self.board.addBike(self.id, (255, 0, 0)) # Do this when a player connects
        self.arenaConnection = None

        self.initiateConnection()
        
    # Starts a TCP connection with the port specified as the one for player/arena communication
    def initiateConnection(self):
        # To connect to the Arena to establish the player's connection
        reactor.connectTCP(ARENA_IP_ADDRESS, PLAYER_PORT, PlayerConnectionFactory(self.connectionCallback))
        reactor.run()

    # Gives the PlayerConnector a reference to the connection for further communication
    def connectionCallback(self, connection):
        self.arenaConnection = connection
        
    # Receives a BikeEvent and passes it to the Arena (so arena can tell other players)
    # TODO pickle?
    def newEvent(self, event):
        if self.arenaConnection:
            self.arenaConnection.sendData(event)
        else:
            print "Error: player not yet connected to arena"

if __name__ == "__main__":
    # For testing
    connector = PlayerConnector(None)
    connector.initiateConnection()
    
