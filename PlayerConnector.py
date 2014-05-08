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

PLAYER_PORT = 9010
ARENA_IP_ADDRESS = "66.254.237.93"

# The actual connection with the Arena that will send and receive data
class PlayerConnection(Protocol):
    def __init__(self):
        pass

    def connectionMade(self):
        print 'Connected to Arena'

    def dataReceived(self, data):
        print data


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
        board.addBike(self.id, (255, 0, 0))
        
    # Starts a TCP connection with the port specified as the one for player/arena communication
    def initiateConnection(self):
        # To connect to the Arena to establish the player's connection
        reactor.connectTCP(ARENA_IP_ADDRESS, PLAYER_PORT, PlayerConnectionFactory())
        reactor.run()
        
    def newEvent(self, event):
        pass

if __name__ == "__main__":
    connector = PlayerConnector()
    connector.initiateConnection()
    
