import socket
import sys
import time
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print ('connecting to %s port %s' % server_address)
sock.connect(server_address)
counter = 0
packetSize = 115

time.sleep(10)
while True:
	try:		
		# print(".", end = "")
		data = sock.recv(packetSize)
		if(len(data) > 0):
			print ('received "%s"' % data)
			data = ""
			counter += 1
			print("counter :", counter)

	except KeyboardInterrupt:
		print('closing socket')
		sock.close()

	except Exception as e:
		pass

	finally:
		pass