import socket
import time
import sys
import subprocess
import re

def diskUsage():

    output = subprocess.run("df --total |grep total", shell=True, stdout=subprocess.PIPE,)
    index = 0
    data = str

    while True:
        data = str(output.stdout).split(" ")

        if re.match('^[-+]?[0-9]\d{0,2}(\.\d{1,2})?%?$', str(data[index])):
            break
        else:
            index+=1
    
    return data[index]

def Main():
    host = '192.168.15.141'
    port = 5000
    s = socket.socket()
    while True:
        try:
            s.connect((host, port))
            break
        except:
            sys.exit ("connection error: (s.connect((host,port))")


    # database operations
    temper  = diskUsage()
    while True:

        try:
            s.send(temper.encode())
        except:
            sys.exit("Data send error 's.send(temper)'")


        try:
            data = s.recv(1024).decode()
        except:
            print ("No response data (data = s.recv(1024))")


        print ('Received from server: ' + str(data))
        time.sleep(1)

    s.close()

if __name__ == '__main__':
    Main()

    #servis nedir? Bir programi servisten ayiran nedir?
    #UDP daha iyi olur mu? Yoksa onun yerine gonderilen
    #ve gelen veriyi veri tabanina mi kaydetmek iyi?
