from twisted.internet import protocol, reactor
import os

class Echo(protocol.Protocol):
	def dataReceived(self, data):
		f = open('/root/walkby_log.csv', 'a')
		addr_log=[]
		os.system("echo Data received `date \"+%d-%m %I-%M\"` >> /root/datalog2.txt")
		data2 = data.split('\n')
		for line in data2:
			details = line.split(',')
			if len(details)>3:
				if 'BSSID' in details[2]:
					os.system("echo Broadcast message received >> /root/datalog2.txt")
					continue
				os.system("echo "+line+" | nc 10.24.18.26 4481")
				if int(details[1])>-70 and details[2] not in addr_log:
					os.system("echo " + details[0] + ","+details[2] + " | nc 10.24.18.26 4483")
					f.write(details[0]+","+details[2] + "\n")
					addr_log.append(details[2])
			
class EchoFactory(protocol.Factory):
	def buildProtocol(self, addr):
		return Echo()


reactor.listenTCP(4482, EchoFactory(), interface='10.24.18.26')
reactor.run()
