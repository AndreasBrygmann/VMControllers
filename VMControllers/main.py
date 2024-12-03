import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))) #Sets a fixed install path

import serverController as sc
import playerCount as pc
from time import sleep
from fastapi import FastAPI
#from fastapi.templating import Jinja2Templates
app = FastAPI()
#templates = Jinja2Templates(directory="templates/")
import uvicorn
from fastapi.responses import HTMLResponse

#count = pc.PlayerCount("Counter Strike: Source")
#count = pc.PlayerCount("Portal")

active, suspended = sc.checkServers()
game = "Videogame"

def adjustServers(game, playersPerServer, strategy):
    count = pc.PlayerCount(game)
    servercount = (count // playersPerServer) + strategy
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


""" def displayActiveVMs(request: Request):
    activeString = 'active_vm_count' \
          '{appid="10",title="Counter Strike",type="game",releasedate="2000-11-01 00:00:00",freetoplay="0",developer="Valve",publisher="Valve",category="top_1000"} ' \
            + str(active)
    suspendedString = 'suspended_vm_count' \
          '{appid="10",title="Counter Strike",type="game",releasedate="2000-11-01 00:00:00",freetoplay="0",developer="Valve",publisher="Valve",category="top_1000"} ' \
            + str(suspended)
    
    return templates.TemplateResponse('metrics.html', context={'active': activeString, 'suspended': suspendedString}) """

@app.get("/metrics", response_class=HTMLResponse)
def displayActiveVMs():
    activeVMString = 'server_count{title="Active Virtual Machines", totalvms="9"} ' + str(active)
    template = f"<html><head><title>Is this Showing?</title></head><body><p>{activeVMString}</p></body></html>"
    
    return HTMLResponse(content=activeVMString, status_code=200)

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
        uvicorn.run("main:app", port=8000, log_level="info")

    elif selection == "9":
        quit()
    else:
        print("Invalid input")
        main()

if __name__ == "__main__":
    main()
