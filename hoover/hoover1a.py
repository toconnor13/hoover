from twisted.internet import protocol, reactor
import os

class Echo(protocol.Protocol):
	def dataReceived(self, data):
		f = open('/root/walkby_log1a.csv', 'a')
		f.write(data)

class EchoFactory(protocol.Factory):
	def buildProtocol(self, addr):
		return Echo()


reactor.listenTCP(4483, EchoFactory(), interface='10.24.18.26')
reactor.run()
