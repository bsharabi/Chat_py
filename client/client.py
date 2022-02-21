from socket import *
import threading
from types import SimpleNamespace
from GUI import GUI_Panel
import json
from select import *
import select
from Validation import *

class Iclient:
    
    def __init__(self) -> None:
        pass
    
    def connect_to_server(self):
        pass
    
    def login(self):
        pass
    
    # @valid_token
    def request(self):
        pass
    
    def response(self):
        pass   

class request:
    def __init__(self) -> None:
        self.req = None
        self.data = None

    def __str__(self):
        return "{\"req\":\"{}\",\"data\":{\"name\":\"barak\",\"password\":12345}}"

class Message:

    def __init__(self, send: int, msg: dict, sending_time: str, sending_date: str) -> None:
        '''
        send and succ = 1
        send and fail = 0
        send to server = -1
        '''
        self.send = send
        self.msg = msg
        self.sending_time = sending_time
        self.sending_date = sending_date
        pass

class Friend:

    def __init__(self, name: str, isConnect: bool) -> None:
        self.name = name
        self.isConnect = isConnect

class Client():

    def __init__(self, id: int=1, name: str = f"user", port: int = 3000, host: str = "localhost") -> None:
        self.id = id
        self.connected:bool=False
        self.name = name
        self.port = port
        self.host = host
        self.friend_msg: dict[str, list[Message]] = {}
        self._socket_TCP = socket(AF_INET, SOCK_STREAM)
        self._socket_UDP = socket(AF_INET, SOCK_STREAM)

    def connect_to_server(self) -> bool:
        try:
            self._socket_TCP.connect((self.host, self.port))
            print("The connection was successful")
            self.connected=True
            return True
        except:
            print("The connection failed")
            return False
    
    # @isConnected
    def Registration(self,name:str,password:str):
        req = "{\"req\":\"registar\",\"data\":{\"name\":" + \
            f"\"{name}\",\"password\":" + f"\"{password}\" "+"}}"
        try:
            self._socket_TCP.send(req.encode())
            print(f"Sent message \"{req}\"\n")
        except:
            pass
        try:
            response = self._socket_TCP.recv(1024).decode()
            print(f"Got response\"{response}\"\n")
            if response == "available":
                return True
        except:
            pass
        return False

    
    @valid_login
    def login_to_server(self, name: str, password: str):
        req = "{\"req\":\"login\",\"data\":{\"name\":" + \
            f"\"{name}\",\"password\":"+f"\"{password}\" "+"}}"
        self.name = name
        try:
            self._socket_TCP.send(req.encode())
            print(f"Sent message \"{req}\"\n")
        except:
            pass
        try:
            response = self._socket_TCP.recv(1024).decode()
            print(f"Got response\"{response}\"\n")
            if response == "success":
                return True
        except:
            pass
        return False
    
    # @isConnected
    def list_of_client_online(self) -> str:
        req = "{\"req\":\"listOnline\",\"data\":{"+"}}"
        try:
            self._socket_TCP.send(req.encode())
            print(f"Sent request \"{req}\"\n")
        except:
            print("Dose not send")
        try:
            response = self._socket_TCP.recv(1024).decode('utf-8')
            print(f"Got response\"{response}\"\n")
            return response
        except:
            print("No reply was received")
        return "faild"
    
    # @isConnected
    def send_msg_to_client(self, to: str, msg: str):
        req = {
            "req": "msg",
            "data": {
                "name": f"{to}",
                "msg": f"{msg}"
            },
            "from": f"{self.name}"
        }
        try:
            self._socket_TCP.send(str(json.dumps(req)).encode())
            print(f"Sent message \"{req}\"\n")
        except:
            pass
        try:
            response = self._socket_TCP.recv(1024).decode()
            print(f"Got response\"{response}\"\n")
            if response == "success":
                return True
        except:
            pass
        return False

    def get_msg_from_client(self):

        inputs = [self._socket_TCP, ]
        outputs = []
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs, 0.1)

        for s in readable:
            if s is self._socket_TCP:
                # message from server
                messages = s.recv(4096).decode()
                print(f"Got response\"{messages}\"\n")

                # if messages:
                #     for message in messages.split("\n"):
                #         splitMessage = message.split(":")
                #         if splitMessage[0] == "message":
                #             # controller.messageList.add(
                #             #     splitMessage[1], splitMessage[2])
                #             pass

    def __del__(self):
        self._socket_TCP.close()
        print("I'm being automatically destroyed. Goodbye!")
        return 0

    def __call__(self):
        while True:
            pass
        pass

    def __str__(self) -> str:
        return f"id {self.id}\nname {self.name}\nroom {self.room}\nport {self.port}\nhost {self.host}"


# if __name__ == "__main__":
#     c1 = Client(id=1)
#     c1()

   
