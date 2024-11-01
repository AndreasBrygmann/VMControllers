from novaClient import NovaClient

nova = NovaClient()

def checkServers():
    active = 0
    suspended = 0
    for i in range(9):
        server = nova.servers.find(name = f"server{i}")
        status = server.status
        if status == "ACTIVE":
            active += 1
        elif status == "SUSPENDED":
            suspended += 1
    '''
    if active + suspended < 9:
        print(f"{9 - (active + suspended)} servers have an unknown status")
    return active, suspended
    '''
    return active, suspended

def findServer(statusCheck):    
    for i in range(9):
        server = nova.servers.find(name = f"server{i}")
        status = server.status
        if status == statusCheck:
            return server
          
    return f"List depleted"

def suspendServers(n):    
    for i in range(9):
        if n == 0:
            return
        server = nova.servers.find(name = f"server{i}")
        status = server.status
        if status == "ACTIVE":
            server.suspend()
            n += 1

def resumeServers(n):    
    for i in range(9):
        if n == 0:
            return
        server = nova.servers.find(name = f"server{i}")
        status = server.status
        if status == "SUSPENDED":
            server.resume()
            n -= 1

def suspendServer():
    server = findServer("ACTIVE")
    if server == "List depleted":
        return f"All servers are suspended"
    server.suspend()

def resumeServer():
    server = findServer("SUSPENDED")
    if server == "List depleted":
        return f"All servers are active"
    server.resume()
