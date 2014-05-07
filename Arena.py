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

PLAYER_PORT = 9010

# The actual connection with the player that will send and receive data
class PlayerConnection(Protocol):
	def __init__(self):
		pass


# Factory for the connection with the Arena
#	This will create an instance of the PlayerConnection class that will be used during communication 
class PlayerConnectionFactory(ClientFactory):
	def startedConnecting(self, connector):
		print "A new player is connecting..."

	def buildProtocol(self, address):
		return PlayerConnection()
		

class Arena():
	def __init__(self):
		# Listens for incoming connections from players joining the game
		reactor.listenTCP(PLAYER_PORT, PlayerConnectionFactory())
		reactor.run() # Waits forever for connections


if __name__ == "__main__":
	arena = Arena() # By instantiating the Arena object, it starts listening for connections