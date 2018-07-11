import socket
import sys

def Main():
	host = '192.168.15.141'
	port = 5000

	s = socket.socket()
	s.bind((host, port))

	s.listen(1)
	print("listening...")
	c, addr = s.accept()

	print("Connection from: " + str(addr))

	while True:
		try:
		    data = c.recv(1024).decode()
		except:
		    sys.exit ("Data could not be recieved 'data = c.recv(1024).decode()'")
		if not data:
		    print("no data")
		    break
		print("from connected user: " + str(data))
		try:
		    c.send(data.encode())
		except:
		    sys.exit("Data could not be sent 'c.send(data.encode())'")
	c.close()


if __name__ == '__main__':
	Main()
