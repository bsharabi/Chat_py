from socket import *
import json
from types import SimpleNamespace
import db 
# import sys
# import os
import threading
from select import *
import select
import json
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))
from SocketHandler import *
from SocketHandler import Client
from GUI_Controller import GUI_Panel

class client:

    def __init__(self, name: str, password: str, connect=None) -> None:
        self.name = name
        self.password = password
        self.connection = connect
        self.isConnect = False
        pass

    def send_msg(self,connection,data):     
        meessage= ""
        connection.send(data.encode())
        pass    
    
    def __repr__(self) -> str:
        return "{" + f"\"name\":\"{self.name}\",\"online\":\"{self.isConnect}\""+"}"

class TCPServer():

    def __init__(self):
        self.host = "localhost"
        self.server = socket(AF_INET, SOCK_STREAM)
        
        # self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server.setblocking(0)
        self.server.bind((self.host, 3000))
        self.port = self.server.getsockname()[1]
        self.gui = GUI_Panel(self.port)
        
        self.add_log = self.gui.GuiController.add_log
        self.clients: dict[str, client] = {}

    def client_registration(self, name: str, password: str):
        # if not db.user_exits(name):
        if name not in self.clients:
            new_client = client(name, password)
            self.clients[name] = new_client
            return True
        return False

    def client_login_req(self, connection, name: str, password: str):
        if name in self.clients:
            if self.clients[name].password == password:
                self.clients[name].connection = connection
                self.clients[name].isConnect = True
                return True
        return False
    
    def client_online(self) -> list:
        return [c for c in self.clients.values()]

    def who_online(self, inputs, outputs, exceptional):
        for connection in exceptional:
            client = self.client_byConnection(connection)
            print(client)
            print(f"Lost connection with {client.name}")
            self.add_log(f"Lost connection with {client.name}")
            if connection in inputs:
                inputs.pop(inputs.index(connection))
            if connection in outputs:
                outputs.pop(outputs.index(connection))
            connection.close()

    def client_byConnection(self, connection) -> client:
        for name, client in self.clients.items():
            if client.connection == connection:
                client.isConnect = False
                return client
            
    def Connection_byName(self, name) -> client:
        for name, client in self.clients.items():
            if client.name == name:
                return client
        return None

    def __call__(self):
        self.server.listen()
        print("server is connect")
        inputs = [self.server]
        outputs = []
        clientNumber = 0
        add_log: function = self.gui.GuiController.add_log
        while self.gui():
            readable, writeable, exceptional = select.select(
                inputs, outputs, inputs, 0.1)
            for s in readable:
                if s is self.server:
                    # listen on server
                    connection, client_address = s.accept()
                    connection.setblocking(0)
                    inputs.append(connection)
                    # print(f"Request connect from {client_address} -> client{clientNumber}")
                    clientNumber += 1
                    self.add_log(
                        f"Request connect from  {client_address} -> client{clientNumber}")
                    # print(f"Adding client{clientNumber}")
                    # self.clients.add(f"client{clientNumber}",(connection, client_address))
                    # handel=Socket_handler(self.clients["clientNumber"])
                    # threading.Thread(target=handel).start()
                else:
                    # client connection
                    message = s.recv(4096).decode()
                    if message:
                        print(f"Got message \"{message}\"\n")
                        jsonObj = json.loads(message, object_hook=lambda d: SimpleNamespace(**d))
                        print(jsonObj)
                        if jsonObj.req == "registar":
                            succ = self.client_registration(jsonObj.data.name,jsonObj.data.password)
                            if succ:
                                response = "available".encode()
                                pass
                            else:
                                response = "taken".encode()
                            self.add_log(
                                f"Request registar from  {client_address} -> {response}")
                            s.send(response)
                        elif jsonObj.req == "login":
                            succ = self.client_login_req(s, jsonObj.data.name,jsonObj.data.password)
                            if succ:
                                response = "success".encode()
                                pass
                            else:
                                response = "failure".encode()
                            self.add_log(
                                f"Request login from  {client_address} -> {response}")
                            s.send(response)
                        elif jsonObj.req == "listOnline":
                            list_client = str(self.client_online())
                            print(list_client)
                            add_log(
                                f"Request listOnline from  {client_address} -> list_client")
                            s.send(list_client.encode())
                        elif jsonObj.req == "msg":
                            print("Hello")
                            to_client=self.Connection_byName(jsonObj.data.name)
                            print(to_client)
                            if to_client != None:
                                from_client=self.client_byConnection(s)
                                data=jsonObj.data
                                to_client.connection.send("is None".encode())
                                # from_client.send_msg(to_client,data)
                            else:
                                pass                      
                    else:
                        exceptional.append(s)               
            self.who_online( inputs, outputs, exceptional)

if __name__ == "__main__":
    s = TCPServer()
    s()
