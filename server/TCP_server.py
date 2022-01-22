from socket import *
# import sys
# import os
import threading
from select import *
import select
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))
from SocketHandler import *
from SocketHandler import Client
from GUI_Controller import GUI_Panel

class clients:
    
    def __init__(self):
        self.dict:dict[str,Client] = dict()

    def add(self, name:str, connection:tuple):
        print("add new client")
        self.dict[name] = Client(name, connection)

    def nameAvailable(self, name:str):
        print("from nameAvailable ",name not in self.dict)
        return  name not in self.dict

    def getByConnection(self, connection)->Client:

        for client in self.dict.values():

            if client._connection == connection:
                return client        
        return None

class TCPServer():

    def __init__(self):
        self.host = "localhost"
        self.server = socket(AF_INET, SOCK_STREAM)
        # self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server.setblocking(0)
        self.server.bind((self.host, 3000))
        self.port = self.server.getsockname()[1]
        self.gui = GUI_Panel(self.port)
        self.clients = clients()

    def __call__(self):
        self.server.listen()
        print("server is connect")
        inputs = [self.server]
        outputs = []
        clientNumber = 0
        while self.gui():
            readable, writeable, exceptional = select.select(
                inputs, outputs, inputs, 0.1)
            for s in readable:
                if s is self.server:
                    # listen on server
                    connection, client_address = s.accept()
                    connection.setblocking(0)
                    inputs.append(connection)
                    self.clients.add(f"client{clientNumber}",(connection, client_address)) 
                    clientNumber += 1
                    # handel=Socket_handler(self.clients["clientNumber"])  
                    # threading.Thread(target=handel).start()
                else:
                    #client connection
                    message = s.recv(4096).decode()
            
                    if message:
                        print(f"Got message \"{message}\"\n")
                        if message.split(":")[0] == "name":
                            if self.clients.nameAvailable(message.split(":")[1]):
                                client = self.clients.getByConnection(s)
                                client.name = message.split(":")[1]
                                response = "available".encode()
                            else:
                                response = "taken".encode()
                            s.send(response)
if __name__ == "__main__":
    s = TCPServer()
    s()
