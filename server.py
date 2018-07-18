import socket
import sys
import json
import configparser

def getConfig():
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    host = config['DEFAULT']['Ip Address']
    port = config['DEFAULT']['Port']
    configData = [host,port]
    return configData


host = getConfig()[0]
port = getConfig()[1]

while True:
	s = socket.socket()
	s.bind((host, int(port)))

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

