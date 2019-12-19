from bluepy.btle import Scanner, DefaultDelegate

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
while True:
	try:
		print("*************************Rescan**************************")
		devices = scanner.scan(20.0)
		print("")
		for dev in devices:
			if(str(dev.addr) in fuzzyList):
				print("************************NEW DEVICE************************")
				print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
				for (adtype, desc, value) in dev.getScanData():
					print ("  %s = %s" % (desc, value))
	except Exception as e:
		print("Exception")
	