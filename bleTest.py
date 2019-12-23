from bluepy.btle import Scanner, DefaultDelegate
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to %s port %s' % server_address)
sock.bind(server_address)

class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)

	def handleDiscovery(self, dev, isNewDev, isNewData):
		if isNewDev:
			print(".", end = '')
			# print("Discovered device", dev.addr, end = '')
		elif isNewData:
			print("/", end = '')
			# print("Received new data from", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
fuzzyList = []
fuzzyList.append("00:81:f9:5f:45:ac")
fuzzyList.append("00:81:f9:5f:35:47")
fuzzyList.append("00:81:f9:5f:35:7D")

# Listen for incoming connections
sock.listen(1)

print ('waiting for a connection')
connection, client_address = sock.accept()
counter = 0
while True:
	try:	
		print("*************************Rescan**************************")
		devices = scanner.scan(0.1)
		print("")
		for dev in devices:
			if(str(dev.addr) in fuzzyList):
				print("************************NEW DEVICE************************")
				print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
				dataToSend = "~"
				for (adtype, desc, value) in dev.getScanData():
					print (" %s = %s" % (desc, value))
					dataToSend += str("%s;%s;" % (desc, value))
				dataToSend += "ADDRESS;"
				dataToSend += str(dev.addr)
				dataToSend += ";"
				dataToSend += "RSSI;"
				dataToSend += str(dev.rssi)
				
				# print ("Raw Data : ", dev.getScanData())
				if(dataToSend):
					print ("Raw Data : ", dataToSend)
					print(len(dataToSend))
					dataToSend = str.encode(dataToSend)
					connection.send(dataToSend)
					counter += 1
					print("counter :", counter)

	except KeyboardInterrupt:
		print('closing socket')
		sock.close()

	except Exception as e:
		print("Exception")
		# sock.close()