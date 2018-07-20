import socket
import time
import sys
import subprocess
import re
import configparser
import json
import os


def diskUsage():
    p = os.popen('df -h | grep /dev/sd')
    p_lines = p.read().split('\n')
    disks = {}
    for i in p_lines:
        if len(i) > 0:
            disks[i.split()[0]] = i.split()[4]
    return disks

def getConfig():
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    host = config['DEFAULT']['Ip Address']
    port = config['DEFAULT']['Port']
    renew_time = config['DEFAULT']['Renew_Period']
    configData = [host,port,renew_time]
    return configData
# bad smell icin sor


def getmodify():
    modify = str(os.popen('stat config.ini | grep Modify').read())
    modified = str(modify.split()[2].split(":")[0] +":"+ modify.split()[2].split(":")[1])
    joinedmodify = str(modify.split()[1] +" "+ modified + " " + modify.split()[3])
    return joinedmodify

def send_message(message, host, port):
    s = socket.socket()
    s.connect((host, int(port)))
    s.send(message.encode())

    data = ''

    data = s.recv(1024).decode()
    s.close()
    return data


def Main():



    try:
        host = getConfig()[0]
        port = getConfig()[1]

    except configparser.MissingSectionHeaderError:
        print("Configde Sectionlardan biri yok.")
        raise SystemExit
    except Exception as e:
        print("Config okunurken hata!")
        print(str(e))
        raise SystemExit


    # s = socket.socket()

    # try:
    #     s.connect((host, int(port)))
    # except:
    #     sys.exit("connection error: (s.connect((host,port))")



# database operations

    while True:

        # s = socket.socket()
        # try:
        #     s.connect((host, int(port)))
        #     connection_status = 1
        # except:
        #     print("Error while connecting")
        #     connection_status = 0
        #     time.sleep(5)

        connection_status = 1
        if connection_status:

            renew_time = getConfig()[2]
            joinedmodify = getmodify()

            disk_usage = diskUsage()

            jsondata = json.dumps(disk_usage)

            try:
                data = send_message(jsondata, '94.103.47.87', 5000)
                # s.send(jsondata.encode())
            except:
                sys.exit("Data send error 's.send(jsondata)'")

            # try:
            #     data = s.recv(1024).decode()
            # except:
            #     print("No response data (data = s.recv(1024))")

            print('kendi hesaplamasi   : ' + joinedmodify)
            print("+++++++++++++++++   : " + str(data)+ "\n\n")
            if str(data) != str(joinedmodify):
                print("Sending MODIFIED")
                # s.send("MODIFIED".encode())
                modified_data = send_message('MODIFIED', '94.103.47.87', 5000)
                print("MODIFIED sent")
            if str(modified_data).split()[0] == "[DEFAULT]":
                print("default aliniyor\n---------")
                print(modified_data)
                with open("config.ini","wb") as f:
                    f.write(modified_data.encode())
                    print("done new thing")
                f.close()

            time.sleep(float(renew_time))

    s.close()


if __name__ == '__main__':
    Main()

#servis nedir? Bir programi servisten ayiran nedir?