import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))) #Copied from the Games code from

import serverController as sc
import playerCount as pc
from time import sleep

#count = pc.PlayerCount("Counter Strike: Source")
#count = pc.PlayerCount("Portal")

#playersPerServer = 500

def adjustServers(game, playersPerServer):
    count = pc.PlayerCount(game)
    active, suspended = sc.checkServers()
    servercount = count // playersPerServer
    if servercount == 0: servercount = 1
    print("Calculated servercount", servercount)
    n = servercount - active
    if servercount == active:
        return f"Servers are meeting demand"
    elif servercount < active:
        sc.suspendServers(n)
        return f"Reduced active servers by {n}"
    elif servercount > active:
        sc.resumeServers(n)
        return f"Increased active servers by {n}"
    
def checkPLayerCount(game):
    count = pc.PlayerCount(game)
    if count == None:
        return f"No game found"
    return count

def checkServers():
    active, suspended = sc.checkServers()
    print(active, "active servers")
    print(suspended, "suspended servers")

def runAutoAdjust(count, playersPerServer):
    run = True
    while run:
        adjustServers(count, playersPerServer)
        sleep(300)

def main():
    print("**********************************************************")
    print("MAIN MENU")
    print("Press 1 to run auto adjust")
    print("Press 2 to check a games player count")
    print("Press 3 to check servers")
    print("Press 9 to exit")
    print("**********************************************************\n")
    selection = input("input a number: ")

    if selection == "1":
        game = input("Select game: ")
        playersPerServer = int(input("select how many players per server: "))
        runAutoAdjust(game, playersPerServer)

    elif selection == "2":
        game = input("Select game: ")
        count = checkPLayerCount(game)
        print(f"{count} players are playing {game}")

    elif selection == "3":
        checkServers()

    elif selection == "9":
        quit()
    else:
        print("Invalid input")
        main()
if __name__ == "__main__":
    main()