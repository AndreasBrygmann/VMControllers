import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))) #Sets a fixed install path

import serverController as sc
import playerCount as pc
from time import sleep
from fastapi import FastAPI
app = FastAPI()
import uvicorn
from fastapi.responses import PlainTextResponse

game = None

def getServerCount():
    active, suspended = sc.checkServers()
    return active, suspended


def adjustServers(game, playersPerServer, strategy):
    active, suspended = getServerCount()
    count = pc.PlayerCount(game)
    servercount = count // playersPerServer
    if servercount < 1: servercount = 1
    servercount += strategy
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
    active, suspended = getServerCount()
    print(active, "active servers")
    print(suspended, "suspended servers")

def runAutoAdjust(count, playersPerServer, strategy):
    run = True
    while run:
        adjustServers(count, playersPerServer, strategy)
        sleep(300)

@app.get("/")
def read_root():
    return {"Hello": "World "}

@app.get("/metrics", response_class=PlainTextResponse)
def displayActiveVMs():
    active, suspended = getServerCount()
    activeVMString = '# TYPE server_count gauge\n# HELP server_count "Number of active servers or VMs"\nserver_count{title="Active Virtual Machines", totalvms="9"} ' + str(active) + '\n'
    #template = f"<html><head><title>Is this Showing?</title></head><body><p>{activeVMString}</p></body></html>"
    
    return PlainTextResponse(content=activeVMString, status_code=200)

def main():
    print("**********************************************************")
    print("MAIN MENU")
    print("Press 1 to run auto adjust")
    print("Press 2 to check a games player count")
    print("Press 3 to check servers")
    print("Press 8 for metrics")
    print("Press 9 to exit")
    print("**********************************************************\n")
    selection = input("input a number: ")

    if selection == "1":
        game = input("Select game: ")
        playersPerServer = int(input("select how many players per server: "))
        print('Select scaling strategy:\nPress "0" For Cost saving\nPress "1" For Balanced scaling\nPress "2" For Aggressive scaling')
        strategy = int(input("Enter 0, 1 or 2..."))
        runAutoAdjust(game, playersPerServer, strategy)

    elif selection == "2":
        game = input("Select game: ")
        count = checkPLayerCount(game)
        print(f"{count} players are playing {game}")

    elif selection == "3":
        checkServers()

    elif selection == "8":
        port = int(input("Select a port: "))
        uvicorn.run("main:app", port=port, log_level="info")

    elif selection == "9":
        quit()
    else:
        print("Invalid input")
        main()

if __name__ == "__main__":
    main()
