import socket
import sys
import json
import configparser
import os
import time

def getConfig(filename):
    config = configparser.ConfigParser()
    config.sections()
    config.read(filename)
    host = config['DEFAULT']['Ip Address']
    port = config['DEFAULT']['Port']
    configData = [host, port]
    return configData

def getmodify(client_ip):
    """
    Linux uzerinden dosyanin timestamp'ine bakar.
    Ancak timestamp degerinde microseconds gorundugu icin, bunlari temizler.
    Eger dosya bulunamazsa veya baska bir hata ile karsilasilirsa, NONE degerini dondurur.
    """
    filepath = 'config_{0}.ini'.format(client_ip)
    try:
        modify = str(os.popen('stat {0} | grep Modify'.format(filepath)).read())
        modified = str(modify.split()[2].split(":")[0] +":"+ modify.split()[2].split(":")[1])
        joinedmodify = str(modify.split()[1] +" "+ modified + " " + modify.split()[3])
    except:
        joinedmodify = 'NONE'
    return joinedmodify


def read_client_config(client_ip):
    """
    Client config dosyalarini okur ve icerigini dondurur.
    Dosya yok ise, NONE dondurur.
    """
    lines = 'NONE'.encode()

    filepath = 'config_{0}.ini'.format(client_ip)
    print("Reading config file: {0}".format(filepath))
    try:
        f = open(filepath, 'rb')
        lines = f.read(1024)
        f.close()
    except FileNotFoundError:
        print("The file {0} was not found on the disk".format(filepath))
    except Exception as e:
        print("Error while reading file {0}. Error: {1}".format(filepath, str(e)))
    return lines



if __name__ == '__main__':


    config_file = 'config_server.ini'

    try:
        host = '0.0.0.0'
        port = getConfig(config_file)[1]

    except Exception as e:
        print("Config okunurken hata oluştu: {0}".format(str(e)))
        raise SystemExit

    s = socket.socket()
    s.bind((host, int(port)))

    s.listen()
    print("listening...")

    while True:


        try:
            c, addr = s.accept()
            print("Connection from: " + str(addr[0]))
            data = c.recv(1024).decode()

            if data:
                print("Message from client: {0}".format(str(data)))
                joinedmodify = getmodify(addr[0]).encode()

                if str(data) == "MODIFIED":
                    client_config_lines = read_client_config(addr[0])
                    c.send(client_config_lines)
                else:
                    try:
                        c.send(joinedmodify)
                    except Exception as e:
                        print("Error while sending data: {0}".format(str(e)))

        except Exception as e:
            print("Error when reading from socket: {0}".format(str(e)))
            raise SystemExit        
    c.close()