from twisted.internet import protocol, reactor
import os

class Echo(protocol.Protocol):
	def dataReceived(self, data):
		f = open('walkby_log.csv', 'a')
		addr_log=[]
		os.system("echo Data received `date \"+%d-%m %I-%M\"` >> datalog2.txt")
		data2 = data.split('\n')
		for line in data2:
			details = line.split(',')
			if details[2]=='BSSID:ff:ff:ff:ff:ff:ff':
				oc.system("echo Broadcast message received >> datalog2.txt")
				continue
			if len(details)>3:
				os.system("echo "+line+" | nc 10.24.18.1 4481")
				if int(details[1])>-70 and details[2] not in addr_log:
					os.system("echo " + details[0] + ","+details[2] + " | nc 10.24.18.1 4483")
					f.write(details[0]+","+details[2] + "\n")
					addr_log.append(details[2])
			
class EchoFactory(protocol.Factory):
	def buildProtocol(self, addr):
		return Echo()


reactor.listenTCP(4482, EchoFactory())
reactor.run()
