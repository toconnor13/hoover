from twisted.internet import protocol, reactor
import os

class Echo(protocol.Protocol):
	def dataReceived(self, data):
		f = open('attendance.csv', 'a')
		f.write(data)
		os.system("echo Data received `date \"+%d-%m %I-%M\"` >> datalog.txt")
		if os.stat('attendance.csv').st_size > 40000:
			os.system("echo File rolled over `date \"+%d-%m %I-%M\"` >> datalog.txt")
			os.system("mysqlimport --ignore-lines=0 --fields-terminated-by=, --columns='timestamp,rssi,id,sensor_id' --local -u root -p'the power to do what is right' cattalax ./attendance.csv >> datalog.txt")
			os.remove('attendance.csv')

class EchoFactory(protocol.Factory):
	def buildProtocol(self, addr):
		return Echo()


reactor.listenTCP(4481, EchoFactory())
reactor.run()
