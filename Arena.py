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

class PlayerConnection(Protocol):
	def __init__(self):
		pass

# The connection with the remote player, one per player
#	This will create an instance of the PlayerConnection class that will be used during communication 
class PlayerConnectionFactory(ClientFactory):
	def startedConnecting(self, connector):
		print "A new player is connecting..."

	def buildProtocol(self, address):
		return PlayerConnection()


if __name__ == "__main__":
	# To connect to a client to establish the connection that will be used during game play
	reactor.connectTCP("student00.cse.nd.edu", PLAYER_PORT, PlayerConnectionFactory())
	reactor.run()