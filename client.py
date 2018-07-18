import socket
import time
import sys
import subprocess
import re
import configparser
import json
import os                                   # yine bad smell için sor hem subp hem os

open('partitions.ini', 'w').close()
os.system("date >> partitions.ini")
os.system("df -h |grep /dev/sd >> partitions.ini")

def diskUsage():
    file = open("partitions.ini", "r")

    data = file.read().split()
    index = 0
    a = 0
    devindex = 0
    useindex = 0
    hold = [[0] * 2 for _ in range(10)]

    while True:
        try:
            if data[index]:
                index += 1
            else:
                index -= 1
                break
        except:
            index -= 1
            break

    while a != index:

        if re.match('/dev/sd', data[a]):
            hold[devindex][useindex] = data[a]
            useindex += 1

            a += 1
        elif re.match('\d{0,3}\%', data[a]):
            hold[devindex][useindex] = data[a]
            useindex -= 1
            devindex += 1
            a += 1
        else:

            a += 1
    return(hold)


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

    devcount = -1
    devindex = 0
    useindex = 0
    while True:
        if diskUsage()[devcount+1][0]==0:
            break
        else:
            devcount+=1
    print(devcount)
# database operations

    while True:
        if devindex > devcount:
            devindex = 0

        data = {
            "disk": diskUsage()[devindex][0],
            "usage": diskUsage()[devindex][1]
        }
        devindex += 1

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