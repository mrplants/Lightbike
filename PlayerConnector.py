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
import _BikeEvent

PLAYER_PORT = 9000
ARENA_IP_ADDRESS = "student00.cse.nd.edu"

# Messages
READY = "ready"
NEW_PLAYER = "player joined"
CONN_LOST = "connection lost"
START_GAME = "start"
CONNECTED = "connected"

# The actual connection with the Arena that will send and receive data
class PlayerConnection(Protocol):
    def __init__(self, callback):
        self.connectionCallback = callback

    # To Arena
    def connectionMade(self):
        print 'Connected to Arena'
        self.connectionCallback(self, CONNECTED)

    # From Arena
    def dataReceived(self, data):
        # Check for each type of event arena broadcasts
        if data == CONN_LOST:
            print "a player lost connection"
            event = BikeEvent(_BikeEvent.CRASH, 0, 0)
            self.board.newEvent(event)

        elif data == NEW_PLAYER:
            print "a player joined"
            self.connectionCallback(self, NEW_PLAYER)

        elif data == START_GAME:
            print "start the game"
            self.connectionCallback(self, START_GAME)

        else:
            # Pass the BikeEvent from some other player to this player's board
            self.board.newEvent(data)

    # To Arena to update it about things happening to this player
    #   Will be sending BikeEvents or the READY message
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
        self.arenaConnection = None

        #self.initiateConnection()
        
    # Starts a TCP connection with the port specified as the one for player/arena communication
    def initiateConnection(self):
        # To connect to the Arena to establish the player's connection
        reactor.connectTCP(ARENA_IP_ADDRESS, PLAYER_PORT, PlayerConnectionFactory(self.connectionCallback))
        reactor.run()

    # Gives the PlayerConnector a reference to the connection for further communication
    def connectionCallback(self, connection, data):
        if data['message'] == NEW_PLAYER:
            # Since a new player just connected, they must be added to the board
            self.board.addBike(data['id'], data['color'])
        elif data == START_GAME:
            self.board.startGame()
        elif data == CONNECTED:
            self.arenaConnection = connection
        
    # Receives a BikeEvent and passes it to the Arena (so arena can tell other players)
    # TODO pickle?
    def newEvent(self, event):
        if self.arenaConnection:
            self.arenaConnection.sendData(event)
        else:
            #print "Error: player not yet connected to arena"
            pass

    # Called  when the player indicates that they are ready to play
    def ready(self):
        self.arenaConnection.sendData(READY)

if __name__ == "__main__":
    # For testing
    connector = PlayerConnector(None)
    connector.initiateConnection()
    
