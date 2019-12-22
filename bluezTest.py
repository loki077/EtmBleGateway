#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PyBluez ble example beacon_scan.py"""

from bluetooth.ble import BeaconService


class Beacon(object):

    def __init__(self, data, address):
        self._uuid = data[0]
        self._major = data[1]
        self._minor = data[2]
        self._power = data[3]
        self._rssi = data[4]
        self._address = address

    def __str__(self):
        ret = "Beacon: address:{ADDR} uuid:{UUID} major:{MAJOR} " \
              "minor:{MINOR} txpower:{POWER} rssi:{RSSI}" \
              .format(ADDR=self._address, UUID=self._uuid, MAJOR=self._major,
                      MINOR=self._minor, POWER=self._power, RSSI=self._rssi)
        return ret


service = BeaconService()
devices = service.scan(2)

for address, data in list(devices.items()):
    b = Beacon(data, address)
    print(b)

print("Done.")


# # bluetooth low energy scan
# from bluetooth.ble import DiscoveryService

# service = DiscoveryService()
# devices = service.discover(2)

# print("Yeah")
# for address, name in devices.items():
#     print("name: {}, address: {}".format(name, address))

# import bluetooth
# import select

# class MyDiscoverer(bluetooth.DeviceDiscoverer):
    
#     def pre_inquiry(self):
#         self.done = False
    
#     def device_discovered(self, address, device_class, name):
#         print("%s - %s" % (address, name))

#     def inquiry_complete(self):
#         self.done = True

# d = MyDiscoverer()
# d.find_devices(lookup_names = True)

# readfiles = [ d, ]

# print("start")
# while True:
#     rfds = select.select( readfiles, [], [] )[0]

#     if d in rfds:
#         d.process_event()

#     if d.done: break