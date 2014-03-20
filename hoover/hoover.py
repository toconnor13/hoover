from twisted.internet import protocol, reactor
import os

f = open('attendance.csv', 'a')
class Echo(protocol.Protocol):
	def dataReceived(self, data):
		f.write(data)
		print "Some data received"
		if os.stat('attendance.csv') > 2000:
			os.system("mysqlimport --ignore-lines=0 --fields-terminated-by=, --columns='timestamp,rssi,id,sensor_id' --local -u root -p'the power to do what is right' cattalax ./attendance.csv")
			print "File rolled over."
			os.remove('attendance.csv')
			f = open('attendance.csv', 'a')

class EchoFactory(protocol.Factory):
	def buildProtocol(self, addr):
		return Echo()


reactor.listenTCP(4481, EchoFactory())
reactor.run()
