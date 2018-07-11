import socket

def Main():
    host = '192.168.15.141'
    port = 5000

    s = socket.socket()
    s.bind((host,port))

    s.listen(1)
    c, addr = s.accept()

    print "Connection from: " + str(addr)

    while True:

        data = c.recv(1024)

        if not data:
           	print "no data"
		break
#	if data>18:
#		c.send("WARNING")
        print "from connected user: " + str(data)

	print  str(data)
	#database operation
	c.send(data)
    c.close()



if __name__ == '__main__':

    Main()
