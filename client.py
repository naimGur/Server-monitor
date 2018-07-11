import socket
import time
from random import randint

def Main():
    host = '192.168.15.141'
    port = 5000

    s = socket.socket()
    while True:
        try:
            s.connect((host, port))
            break
        except:
            print "connection error: (s.connect((host,port))"


    # database operation
    temper  = '10'
    while True:
        #try:
        s.send(temper)
        #    break
        #except:
        #    print "Data send error (s.send(temper))"
        #try:
        data = s.recv(1024)
        #    break
        #except:
        #    print "No response data (data = s.recv(1024))"

        print 'Received from server: ' + str(data)
        time.sleep(1)
    s.close()

if __name__ == '__main__':
    Main()

    #servis nedir? Bir programi servisten ayiran nedir?
    #UDP daha iyi olur mu? Yoksa onun yerine gonderilen
    #ve gelen veriyi veri tabanina mi kaydetmek iyi?
