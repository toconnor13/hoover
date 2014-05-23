from twisted.internet import protocol, reactor
import os
import commands

class Echo(protocol.Protocol):
	def dataReceived(self, data):
		f = open('/root/attendance.csv', 'a')
		f.write(data)
		os.system("echo Data received `date \"+%d-%m %I-%M\"` >> /root/datalog.txt")
		if os.stat('/root/attendance.csv').st_size > 40000:
			os.system("echo File rolled over `date \"+%d-%m %I-%M\"` >> /root/datalog.txt")
			output = commands.getoutput("mysqlimport --ignore-lines=0 --fields-terminated-by=, --columns='timestamp,rssi,id,sensor_id' --local -u root -p'the power to do what is right' cattalax /root/attendance.csv >> /root/datalog.txt")
#			if 'cattalax.attendance: Records' in output:
			if not output:
				os.remove('/root/attendance.csv')
				os.system("echo Success:"+output+" >> /root/datalog.txt")

class EchoFactory(protocol.Factory):
	def buildProtocol(self, addr):
		return Echo()

reactor.listenTCP(4481, EchoFactory(), interface='10.24.18.26')
reactor.run()
