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
		devices = scanner.scan(0.5)
		print("")
		for dev in devices:
			if(str(dev.addr) in fuzzyList):
				print("************************NEW DEVICE************************")
				print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
				for (adtype, desc, value) in dev.getScanData():
					print ("  %s = %s" % (desc, value))
				print ("Raw Data : ", dev.getScanData())
	except Exception as e:
		print("Exception")

# #!/usr/bin/python
# from __future__ import print_function

# from time import gmtime, strftime, sleep
# from bluepy.btle import Scanner, DefaultDelegate, BTLEException
# import sys


# class ScanDelegate(DefaultDelegate):

# 	def handleDiscovery(self, dev, isNewDev, isNewData):
# 		print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), dev.addr, dev.getScanData())
# 		sys.stdout.flush()

# scanner = Scanner().withDelegate(ScanDelegate())

# # listen for ADV_IND packages for 10s, then exit
# scanner.scan(10.0, passive=True)

	