# EtmBleGateway
This is a python code develop to listen adv. of beacons and push it on server. Developed on Rpi with cellular module.


# Setup
Using Bluetooth LE with Python

1 Installing bluepy

Using gatttool is very laborious for doing any useful work, so it's a good idea to use a programming language. The bluepy package is one way to use Bluetooth LE commands from Python - it can be installed from https://pypi.python.org/pypi using the pip command. If you don't already have pip, on the Pi or other Debian systems it is easily installed with:

    sudo apt-get install python-pip
Before installing bluepy you will also need some support libraries:

    sudo apt-get install libglib2.0-dev
Then you can run:

    sudo pip install bluepy
If successful, it will show a message such as this:

        Installing blescan script to /usr/local/bin
         Installing sensortag script to /usr/local/bin
     Successfully installed bluepy
     Cleaning up...

2 Test bluepy

bluepy command-line programs
The blescan program performs a similar function to "hcitool lescan" but produces more information. You will need root privileges (using e.g. sudo) to run it. Typical output looks like this:

     pi@raspberrypi:~ $ sudo blescan 
     Scanning for devices...
         Device (new): b0:b4:48:ed:44:c3 (public), -68 dBm 
        Flags: <05>
        Incomplete 16b Services: <80aa>
        Complete Local Name: 'CC2650 SensorTag'
        Tx Power: <00>
        0x12: <08002003>
        Manufacturer: <0d00030000>
        
You can alter its behaviour with various command-line options; blescan -h gives help text.

# bluepy
Below is the class specification of blupy:
http://ianharvey.github.io/bluepy-doc/index.html

Git Hub Link :
https://github.com/IanHarvey/bluepy

# Hardware Requirement
1 Rpi 4 (Ble 5)
2 sixfab mPCI-E Base Shield 
3 EC25-AU
4 ETM Ble publisher beacon

# Future Scope
This gateway code over RPi will be able to Scan our particular beacon push the data to the server. 
Internet access will be through Cellular module using SixFab base board - with Quectle module / Lan / Wifi.
Configure Devices over the air.
