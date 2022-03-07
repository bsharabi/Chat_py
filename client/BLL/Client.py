from fileinput import filename
import sys
sys.path.append("./Client")
from threading import Lock
from socket import *
import json
from select import *
import select
from .Validation import *
import os
from datetime import datetime
from os import path
from threading import Thread
from api.IClient import Iclient
from api.IFriends import IFriend
from api.IRequest import IRequest
from api.IResponse import IResponse
from .controllerUDP import Client_Start
LOCK = Lock()

class Request(IRequest):
    def __init__(self, header: dict = {}, body: dict = {}, req: str = "", fileName: str = "", user: str = "", password: str = "", origin: str = "", toClient: str = "", *args, **kwargs) -> None:
        super().__init__(header, body, req, fileName, user,
                         password, origin, toClient, *args, **kwargs)

    def get_req(self):
        return self.header.get("req")

    def get_data(self):
        return self.body.get("data")

    def get_origin(self):
        return self.origin

    def get_date(self):
        return self.header.get("date")

    def get_user(self):
        form: dict = self.body.get("form")
        return form.get("user")

    def get_password(self):
        form: dict = self.body.get("form")
        return form.get("password")

    def get_toClient(self):
        return self.body.get("to")

    def __str__(self):
        return json.dumps({"header": self.header, "body": self.body, "origin": self.origin})

class Response(IResponse):

    def __init__(self, header: dict = {}, body: dict = {}, res: str = "", origin: str = "", *args, **kwargs) -> None:
        self.header = header if header else {
            "res": res, "date": str(datetime.now())}
        self.body = body if body else {"args": args, "data": kwargs}
        self.origin = origin

    def get_res(self):
        return self.header.get("res")

    def get_data(self):
        return self.body.get("data")

    def get_origin(self):
        return self.origin

    def get_date(self):
        return self.header.get("date")

    def get_body(self):
        return self.body

    def __str__(self):
        return json.dumps({"header": self.header, "body": self.body, "origin": self.origin})

class Friend(IFriend):

    def __init__(self, name: str, isConnect: bool, path_folder: str) -> None:
        super().__init__(name, isConnect, path_folder)

    def write(self, *args, **kwargs):
        filename = self.msg_file if args[0] == "msg"else self.log_file

        listObj = []
        try:
            with open(filename) as file:
                listObj = json.load(file)
            listObj.append(kwargs)
            with open(filename, 'w') as json_file:
                json.dump(listObj, json_file,
                          indent=4,
                          separators=(',', ': '))
        except:
            pass

    def read(self, filename: str, f=0, to=10)->tuple[list,int,int]:
        file_Name = self.msg_file if filename == "msg"else self.log_file
        listObj = []
        try:
            with open(file_Name) as file:
                listObj = json.load(file)
                listObj = listObj[::-1]
                length = len(listObj)
            return listObj[:14], f, to
            # if length < to:
            #     return listObj[length-10:length], length-10, length
            # return listObj[f:to], f, to
        except:
            return [], f, to

    def __repr__(self):
        return f"{self.name} {self.isConnect}"

class Client(Iclient):

    def __init__(self, id: int = 1, name: str = f"user", port: int = 3000, host: str = "localhost") -> None:
        super().__init__()
        self.id = id
        self.connectedTCP: bool = False
        self.connectedUDP: bool = False
        self.name = name
        self.port = port
        self.host = host
        self.path = ""
        self.friends_list = []
        self.friends: dict[str, IFriend] = {}
        self._socket_TCP = socket(AF_INET, SOCK_STREAM)
        self._socket_UDP = socket(AF_INET, SOCK_DGRAM)
        self.options: dict[str, function] = {}
        self.download_file_count_pack=0

        self.load_options()

    def load_options(self)->None:
        '''
        The function builds a dictionary of functions for easier use
        @return None
        '''
        self.options["udpateFriend"] = self.udpateFriend
        self.options["brodcastMsg"] = self.brodcast
        self.options["msg"] = self.get_msg
        self.options["fileList"] = self.set_file_list
        self.options["downloadFile"] = self.download_file
        self.options["D-downloadFile"] = self.d_download_file
        self.options["Server Ex"] = self.err_download_file

    def connect_to_TCP(self) -> bool:
        """
        connect to client on TCP protocol 
        @return: True if connect successful False o.w.
        """
        try:
            self._socket_TCP.connect((self.host, self.port))
            print("The connection was successful (TCP)")
            self.connectedTCP = True
            return True
        except:
            print("The connection failed (TCP)")
            return False

    def connect_to_UDP(self)-> bool:
        """
        connect to client on UDP protocol 
        @return: True if connect successful False o.w.
        """
        try:
            print("The connection was successful (UDP)")
            self.connectedUDP = True
            return True
        except:
            print("The connection failed (UDP)")
            return False

    def close_connection_TCP(self):
        """
        close connection client on TCP protocol 
        @return: True if close successful False o.w.
        """
        try:
            self._socket_TCP.close()
            print("The close connection was successful (TCP)")
            self.connectedTCP = False
            return True
        except:
            print("The close connection failed (TCP)")
            return False

    def close_connection_UDP(self):
        """
        close connection client on UDP protocol 
        @return: True if close successful False o.w.
        """
        try:
            self._socket_UDP.close()
            print("The close connection was successful (UDP)")
            self.connectedUDP = False
            return True
        except:
            print("The close connection failed (UDP)")
            return False

    def create_data_directory(self) -> bool:
        _path=path.join(os.getcwd(),"Client/data")
        if not path.isdir(_path):
            os.mkdir(_path)
        self.path = path.join(_path,self.name)
        if not path.isdir(self.path):
            os.mkdir(self.path)
            return True

    def create_data_directory_friends(self, data: dict)->None:
        with LOCK:
            friends_list: list[str] = data.get("listOnline")
            friends_list.remove(self.name)
            friends_list.append("Friends Group")
            friend_group_online = False
            if len(self.friends_list) == 0:
                self.friends_list: list[str] = os.listdir(path=self.path)

            for name in self.friends_list:
                path_folder = path.join(self.path, name)
                if name in friends_list:
                    friends_list.remove(name)
                    self.friends[name] = Friend(name, True, path_folder)
                    if name != "Friends Group":
                        friend_group_online = True
                    continue
                self.friends[name] = Friend(name, False, path_folder)

            for friend in friends_list:
                path_folder = path.join(self.path, friend)
                if not os.path.isdir(path_folder):
                    os.mkdir(path_folder)
                self.friends[friend] = Friend(friend, True, path_folder)
                friend_group_online = True

            self.friends["Friends Group"].isConnect = friend_group_online

            self.friends = {k: v for k, v in sorted(
                self.friends.items(), key=lambda item: not item[1].isConnect)}

    def login(self, req: str = "", password: str = "", user:str="",origin: str = "", *args, **kwargs) -> tuple[bool, str]:
        user=self.name if user=="" else user
        request = Request(header={"req": req}, user=user,
                          password=password, origin=origin, *args, **kwargs)
        try:
            self._socket_TCP.send(request.__str__().encode())
            print(f"Sent message \"{request}\"\n")
        except Exception as e:
            print(f"fail send \"{request}\"\n")
            print("Error msg :", e)
            return False, "error connect"
        try:
            response_string = self._socket_TCP.recv(4096).decode()
            response_dict = json.loads(response_string)
            response_object = Response(**response_dict)
            print(f"Got response\"{response_object}\"\n")
            if response_object.get_res() == "Success":
                self.create_data_directory()
                self.create_data_directory_friends(response_object.get_data())
                return True, response_object.get_res()
        except Exception as e:
            print("No response from server ", e)
            return False, "IoException"
        return False, response_object.get_res()

    def register(self, req: str = "", password: str = "",user:str="", origin: str = "", *args, **kwargs) -> tuple[bool, str]:
        user=self.name if user=="" else user

        request = Request(header={"req": req}, user=user, password=password,
                          origin=origin, *args, **kwargs)
        try:
            self._socket_TCP.send(request.__str__().encode())
            print(f"Sent message \"{request}\"\n")
        except:
            print(f"fail send \"{request}\"\n")
            return False, "error"
        try:
            response_string = self._socket_TCP.recv(1024).decode()
            response_dict = json.loads(response_string)
            response_object = Response(**response_dict)
            print(f"Got response\"{response_object}\"\n")
            if response_object.get_res() == "available":
                return True, "Success"
        except:
            print("No response from server")
            return False, "IoException"
        return False, response_object.get_res()

    def readTCP(self, connection:socket)->None:
        '''
        The function receives a TCP connection and reads it
        '''
        if connection is self._socket_TCP:
            self.server_response(connection)

    def readUDP(self, connection: socket)->None:
        '''
        The function receives a UDP connection and reads it
        '''
        data, address = connection.recvfrom(4096)
        print(data, address)

    def server_response(self, connection:socket) -> None:
        '''
        The function reads the message from the server
        and converts the message to the reply object and then routes it
        '''
        try:
            response_string = connection.recv(4096).decode()
            if response_string:
                print(f"Got response\"{response_string}\"\n")
                response_dict = json.loads(response_string)
                response_object = Response(**response_dict)
                res = response_object.get_res()
                self.options[res](response_object)

        except Exception as e:
            print(e)

    def udpateFriend(self, res: IResponse) -> None:
        self.create_data_directory_friends(res.get_data())
        self.mc += 1

    def brodcast(self, res: IResponse) -> None:
        body = res.get_body()
        data: dict = res.get_data()
        nameFriend = res.get_body().get("to")
        msg = data.get("msg")
        dateT = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.friends.get(nameFriend).write(
            "msg", msg=msg, fromClient=nameFriend, toClient=self.name, date=dateT)
        self.mc += 1

    def set_file_list(self, res: IResponse) -> None:
        '''
        The function saves the downloadable files from the server in the variable
        '''
        try:
            self.file_list = res.get_data()["filesList"]
        except Exception as e:
            print(e)

    def get_msg(self, res: IResponse) -> None:
        body = res.get_body()
        data: dict = res.get_data()
        msg = data.get("msg")
        form: dict = body.get("form")
        nameFriend = form.get("user")
        dateT = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.friends.get(nameFriend).write(
            "msg", msg=msg, fromClient=nameFriend, toClient=self.name, date=dateT)
        self.mc += 1
    
    def d_download_file(self,res:IResponse)->None:
        pass
    
    def err_download_file(self,res:IResponse)->None:
        pass
    
    def download_file(self, res: IResponse)->bool:
        try:
            downloadFlag = res.get_data()["flag"]
            
            if downloadFlag == 1:
                file_name=res.get_data()["file_name"]
                count_p=res.get_data()["packet_count"]
                self.download_file_count_pack=int(count_p)
                self.download_start=True
                Client_Start(file_name,self)
            
        except Exception as e:
            print(e)        

    def request(self, req: str = "", fileName: str = "",  password: str = "", origin: str = "", toClient: str = "", *args, **kwargs)->None:
        request = Request(req=req, fileName=fileName, user=self.name, password=password,
                          origin=origin, toClient=toClient, *args, **kwargs)
        try:
            self._socket_TCP.send(request.__str__().encode())
            print(f"Sent message \"{request}\"\n")
        except:
            print(f"fail send \"{request}\"\n")
            return False, "error"

    def response(self)->None:
        inputs = [self._socket_TCP, self._socket_UDP]
        outputs = []
        while self.connectedTCP:
            try:
                readable, writable, exceptional = select.select(
                    inputs, outputs, inputs, 0.1)
                for s in readable:
                    s: socket
                    if s.type == self._socket_TCP.type:
                        self.readTCP(s)
                    elif s.type == self._socket_UDP.type:
                        self.readUDP(s)
            except Exception as e:
                print(e)

    def __del__(self):
        self.connectedTCP = False
        self.connectedUDP = False
        self.close_connection_UDP()
        self.close_connection_TCP()
        print("Client destroyed, Goodbye!")

    def __str__(self) -> str:
        '''
        A function performed when the object is erased from memory
        '''
        return f"id {self.id}\nname {self.name}\nport {self.port}\nhost {self.host}"
