from socket import *
import threading
from client_GUI import GUI_Panel

class client:
    client_number = 0
    def __init__(self, id: int = client_number, name: str = f"user{client_number}", room: str = "all", connect: socket = None, port: int = 3000, host: str = "localhost") -> None:
        self.id = id
        self.name = name
        self.room = room
        self.connect = connect
        self.port = port
        self.host = host
        self.server_TCP = socket(AF_INET, SOCK_STREAM)
        self.server_UDP = socket(AF_INET, SOCK_STREAM)
        self.gui=GUI_Panel()
        client.client_number += 1


    def __del__(self):
        print("I'm being automatically destroyed. Goodbye!")
        return 0

    def inc_client_number(self) -> int:
        client.client_number += 1
        return client.client_number
        
    def __call__(self):
        print(f"Client is connected {self.id}")
        self.gui(self.server_TCP)
        print("after gui __call__ from client ")

    def __str__(self) -> str:
        return f"id {self.id}\nname {self.name}\nroom {self.room}\n"


if __name__ == "__main__":
    c1 = client(id=1)
    c1()

