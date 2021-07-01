from crc32forcer import access
from runtimeSrc import changeSrc, replace
import ReadWrite
import DataAnalyzer
from colorama import Fore
from infoCollector import getData
import os, sys
import time
import libsSecurity
from createPack import genrate
from createShell import shell

clear = lambda: os.system("clear")

def upack():
    with open("gameInfo.txt", 'r') as f:
        d = f.read()
        f.close()
    all = d.split()
    pkg = all[0]
    data = all[1]
    return pkg,data


def main():
    getData()
    pkg, data = upack()
    while(ReadWrite.get_pid(pkg) == ""):
        clear()
        print("[x] Game offline")
        
    print("[x]Game ONLINE")
    shell(pkg)
    genrate(pkg)
    ReadWrite.writer(pkg, "200", "0")
    ReadWrite.writer(pkg, "150", "0")
    num = float(9.21970312**-41)
    ReadWrite.writer(pkg, str(num), "0")
    time.sleep(2)
    while True:
        clear()
        print("1. Reach Lobby")
        print("2. Exit")
        ans = input(">>>> ")
        ans = int(ans)
        if ans == 1:
            changeSrc(pkg)
            #libsSecurity.changeLib(data)
            print("Done. Done use it again")
            time.sleep(3)
        elif ans == 2:
            replace(pkg)
            #libsSecurity.default(data)
            time.sleep(3)
            sys.exit(0)
            break
        else:
            print("Enter given data")
            time.sleep(2)
    

main()

    


