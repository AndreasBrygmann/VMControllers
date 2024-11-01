import serverController as sc
import playerCount as pc
from time import sleep as time

#count = pc.PlayerCount("Counter Strike: Source")
count = pc.PlayerCount("Portal")

active, suspended = sc.checkServers()
print("Active servers on start", active)
print("Playercount on start", count)

playersPerServer = 500

def adjustServers():
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


run = True
while run:
    adjustServers()
    time.sleep(300)