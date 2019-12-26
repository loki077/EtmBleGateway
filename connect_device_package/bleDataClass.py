"""********************************************************************************************
Project Name    : bleDataClass.py
Developer       : Lokesh Ramina
Platform        : Python 3.7 on Rpi4, Debian
Date            : 22-12-2019
Purpose         : To scan Ble Sensor Data and push to second script
Note			: Please go through the readme.txt file to understand the code and concept
********************************************************************************************"""

'''***************************Library Import***************************'''
import time
from datetime import datetime

dictData1 ={}
dictData1["Flags"] = "4"
dictData1["Complete Local Name"] = "FURZY101ABAA"
dictData1["Manufacturer"] ="feff00710400ed0271008927"
dictData1["ADDRESS"] ="00:81:f9:5f:35:47"
dictData1["RSSI"] = "-88"

dictData2 ={}
dictData2["Flags"] = "4"
dictData2["Complete Local Name"] = "FURZY101ABAA"
dictData2["Manufacturer"] ="feff01710400ed0271008927"
dictData2["ADDRESS"] ="00:81:f9:5f:35:47"
dictData2["RSSI"] = "-88"

dictData3 ={}
dictData3["Flags"] = "4"
dictData3["Complete Local Name"] = "FURZY101ABAB"
dictData3["Manufacturer"] ="feff00710400ed0271008927"
dictData3["ADDRESS"] ="00:81:f9:5f:35:47"
dictData3["RSSI"] = "-88"

dictData4 ={}
dictData4["Flags"] = "4"
dictData4["Complete Local Name"] = "FURZY101ABAB"
dictData4["Manufacturer"] ="feff01710400ed0271008927"
dictData4["ADDRESS"] ="00:81:f9:5f:35:47"
dictData4["RSSI"] = "-88"

class AdvtFormat():
	# ********* Slicing Index & Parameters ********* 
	#Manufacturer Descriptor (FURZY)
	# feff00710400ed0271008927
	# feff01710400ed0271008927
	#Battery Voltage
	batVoltStartPt 	= 6
	batVoltEndPt 	= 7
	
	#Opto Sensor Reading
	optoStartPt 	= 8
	optoEndPt 		= 11

	#Temp Sensor Reading HDC2010/BME280
	tempStartPt 	= 12
	tempEndPt	 	= 15

	#Humidity Sensor Reading HDC2010/BME280
	humiStartPt 	= 16
	humiEndPt	 	= 19

	#Operating Hours
	oHourStartPt	= 20
	oHourEndPt		= 23

	#Pressure sensor
	pressureStartPt	= 20
	pressureEndPt	= 23

	#Relative Humidity Params BME280
	relHumiPercentPerStep = 0.5 #100% RH = Dec. 200 (ADC step) -> 0xc800 

	#Temp Params BME280
	zeroDegCStep = 500 #ADC Step
	degCPerStep = 0.1 

	#Voltage calculation
	maxVoltIn = 3.3 
	batVoltRes = 8 #bits
	voltsPerStep = maxVoltIn/((2**batVoltRes)-1)

	#Air Pressure Params BME280
	pressurePerStep = 10 #Pascals (Pa)
		
	#Variables of system
	deviceName = 0
	deviceAdd = 0
	rssiVal = 0
	flags = 0

	rxTime = ""
	rxDate = ""
	messageData0 = ""
	messageData1 = ""
	status = 0

	def __init__(self, tempDeviceName, tempDeviceAdd, tempFlags):
		self.deviceName = tempDeviceName
		self.deviceAdd = tempDeviceAdd
		self.flags = tempFlags

	def get_data(self):
		finalString = ""
		if self.status == 1:
			finalString = self.general_data()
			print(finalString)
			self.status = 0
		return finalString

	def general_data(self):
		return "flags," + self.flags  +",deviceName," + self.deviceName +",deviceAdd," + self.deviceAdd +",rssi," + self.rssiVal + ",date," + self.rxDate + ",time,"+self.rxTime + self.get_bat_volt() + self.get_opto_reading() + self.get_temp_BME280() + self.get_temp_HDC2010() + self.get_humi_BME280() + self.get_humi_HDC2010() + self.get_air_pressure() + self.get_operating_hour()

	# feff00710400ed0271008927
	# feff01710400ed0271008927
	def feed_data(self, tempManufacturing, tempRssiVal):
		self.rxDate = str(datetime.date(datetime.now()))
		self.rxTime = str(datetime.time(datetime.now()))
		self.rssiVal = tempRssiVal
		if(int(tempManufacturing[5],16) == 0):
			if tempManufacturing != self.messageData0:
				self.messageData0 = tempManufacturing
				self.status = 1
				print("New 0")

		elif (int(tempManufacturing[5],16) == 1):
			if tempManufacturing != self.messageData1:
				self.messageData1 = tempManufacturing
				self.status = 1
				print("New 1")

	def get_data_status(self):
		return self.status

	'''Extract & Calculate Battery Voltage'''
	def get_bat_volt(self):
		print(self.messageData0[self.batVoltStartPt:self.batVoltEndPt+1])
		batVoltHex = int(self.messageData0[self.batVoltStartPt:self.batVoltEndPt+1], 16)
		print(batVoltHex)
		batVolt = round(batVoltHex * self.voltsPerStep, 2)
		return ",batteryVoltage," + str(batVolt)

	'''Extract & Calculate Opto Sensor Reading'''	
	def get_opto_reading(self):
		optoHex = self.messageData0[self.optoStartPt:self.optoEndPt+1]
		optoHexChangeEndian = []

		for count in range(1,len(optoHex),2):
			optoHexChangeEndian.insert(0,optoHex[count-1:count+1]) #Little Endian -> Big Endian Byte Order
		
		optoHexBigEndian = ''.join(optoHexChangeEndian)
		optoRaw = int(optoHexBigEndian,16) #Presently raw reading, not converted to any sci/eng units
		return ",optoVal," + str(optoRaw)

	'''Extract & Calculate Temperature BME280 Sensor'''
	def get_temp_BME280(self):
		tempHex = self.messageData1[self.tempStartPt:self.tempEndPt+1]
		tempHexChangeEndian = []

		for count in range(1,len(tempHex),2):
			tempHexChangeEndian.insert(0,tempHex[count-1:count+1]) #Little Endian -> Big Endian Byte Order

		tempHexBigEndian = ''.join(tempHexChangeEndian)
		tempStep = int(tempHexBigEndian,16)
		tempDegC = round((tempStep-self.zeroDegCStep)*self.degCPerStep,2)
		return ",tempBmeVal," + str(tempDegC)

	'''Extract & Calculate Temperature HDC2010 Sensor'''
	def get_temp_HDC2010(self):
		tempHex = self.messageData0[self.tempStartPt:self.tempEndPt+1]
		tempHexChangeEndian = []

		for count in range(1,len(tempHex),2):
			tempHexChangeEndian.insert(0,tempHex[count-1:count+1]) #Little Endian -> Big Endian Byte Order

		tempHexBigEndian = ''.join(tempHexChangeEndian)
		tempStep = int(tempHexBigEndian,16)
		tempDegC = tempStep
		return ",tempHdcVal," + str(tempDegC)

	'''Extract & Calculate Relative Humidity BME280 Sensor'''
	def get_humi_BME280(self):
		relHumiHex = self.messageData1[self.humiStartPt:self.humiEndPt+1]
		relHumiChangeEndian = [] 

		for count in range(1,len(relHumiHex),2):
			relHumiChangeEndian.insert(0,relHumiHex[count-1:count+1]) #Little Endian -> Big Endian Byte Order

		relHumiHexBigEndian = ''.join(relHumiChangeEndian)
		relHumiStep = int(relHumiHexBigEndian,16)
		relHumiPercent = relHumiStep * self.relHumiPercentPerStep
		return ",humiBmeVal," + str(relHumiPercent)

	'''Extract & Calculate Relative Humidity HDC2010 Sensor'''
	def get_humi_HDC2010(self):
		relHumiHex = self.messageData0[self.humiStartPt:self.humiEndPt+1]
		relHumiChangeEndian = [] 

		for count in range(1,len(relHumiHex),2):
			relHumiChangeEndian.insert(0,relHumiHex[count-1:count+1]) #Little Endian -> Big Endian Byte Order

		relHumiHexBigEndian = ''.join(relHumiChangeEndian)
		relHumiStep = int(relHumiHexBigEndian,16)
		relHumiPercent = relHumiStep * self.relHumiPercentPerStep
		return ",humiHdcVal," + str(relHumiPercent)

	'''Extract & Calculate Air Pressure BME280 Sensor'''
	def get_air_pressure(self):
		pressureHex = self.messageData1[self.pressureStartPt:self.pressureEndPt+1]
		pressureChangeEndian = []

		for count in range(1,len(pressureHex),2):
			pressureChangeEndian.insert(0, pressureHex[count-1:count+1]) #Little Endian -> Big Endian Byte Order

		pressureHexBigEndian = ''.join(pressureChangeEndian)
		pressureStep = int(pressureHexBigEndian,16)
		pressurekPa = (pressureStep * self.pressurePerStep)/1000
		return ",airPressure," + str(pressurekPa)

	'''Calculate operating hour'''
	def get_operating_hour(self):
		opHour = int(self.messageData0[self.oHourStartPt:self.oHourEndPt+1])
		rawOPHour = opHour * 2
		return ",operatingHour," + str(rawOPHour)

class DataHandler():
	dataBase = []
	deviceIdList = []

	def feed_data(self, tempData):
		if tempData["Complete Local Name"] in self.deviceIdList:
			index = self.deviceIdList.index(tempData["Complete Local Name"])
			self.dataBase[index].feed_data(tempData["Manufacturer"],tempData["RSSI"])
			print("Id exist")

		else:
			self.dataBase.append(AdvtFormat(tempData["Complete Local Name"], tempData["ADDRESS"], tempData["Flags"]))
			self.dataBase[-1].feed_data(tempData["Manufacturer"],tempData["RSSI"])
			self.deviceIdList.append(tempData["Complete Local Name"])
			print("New Id ")

	def get_data_len(self):
		tempCounter = 0
		for advData in self.dataBase:
			if advData.get_data_status() == 1:
				tempCounter += 1
		return tempCounter

	def get_data(self):
		for x in self.dataBase:
			if x.get_data_status() == 1:
				return x.get_data()
		return ""


# bleDataHandlerObj = DataHandler()

# while True:
# 	bleDataHandlerObj.feed_data(dictData1)
# 	time.sleep(2)
# 	bleDataHandlerObj.feed_data(dictData2)
# 	time.sleep(2)
# 	bleDataHandlerObj.feed_data(dictData3)
# 	time.sleep(2)
# 	bleDataHandlerObj.feed_data(dictData4)
# 	time.sleep(2)
# 	while True:
# 		dataToSend = bleDataHandlerObj.get_data()
# 		if(dataToSend != ""):
# 			print(dataToSend)
# 		else:
# 			break
