import socket
import time
import sys
import subprocess
import re
import configparser
import json
import os                                   # yine bad smell için sor hem subp hem os

def diskUsage():
    """This method gets the Disk Usage"""
    os.system("date >> partitions.ini")
    os.system("df -h |grep /dev/sd >> partitions.ini")
    #output = subprocess.run("df -h |grep dev/sd", shell=True, stdout=subprocess.PIPE,)
    file = open("partitions.ini", "r")
    index = 0
    data = str
    bufferreader = file.read()
    while True:
        data = bufferreader.split(" ")
        #data = str(output.stdout).split(" ")
        if re.match('/dev/sd',data[index]):
            print(data[index])
        if re.match('\d{0,3}\%', str(data[index])):
            break
        else:
            index+=1

    return data[index]


def getConfig():
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    host = config['DEFAULT']['Ip Address']
    port = config['DEFAULT']['Port']
    renew_time = config['DEFAULT']['Renew Period']
    configData = [host,port,renew_time]
    return configData
# bad smell icin sor


def Main():

    host = getConfig()[0]
    port = getConfig()[1]
    renew_time = getConfig()[2]


    s = socket.socket()

    try:
        s.connect((host, int(port)))
    except:
        sys.exit ("connection error: (s.connect((host,port))")


    # database operations

    while True:
        data = {
            "disk": "disk usage",
            "value": diskUsage()
        }

        jsondata = json.dumps(data)

        with open("data_file", "w") as write_file:
            json.dump(data, write_file)


        try:
            s.send(jsondata.encode())
        except:
            sys.exit("Data send error 's.send(jsondata)'")


        try:
            data = s.recv(1024).decode()
        except:
            print("No response data (data = s.recv(1024))")


        print('Received from server: ' + str(data))
        time.sleep(float(renew_time))

    s.close()

if __name__ == '__main__':
    Main()

    #servis nedir? Bir programi servisten ayiran nedir?
    #UDP daha iyi olur mu? Yoksa onun yerine gonderilen
    #ve gelen veriyi veri tabanina mi kaydetmek iyi?
