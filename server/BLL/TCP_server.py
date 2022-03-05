import sys
sys.path.append("./Server")
import select
from socket import *
from os.path import isfile, join
from os import listdir
import json
from api.IClient import IClient
from api.IServer import *
from DAL.DataBase import mongodb
from datetime import datetime
from api.IRequest import *
from api.IResponse import *
import threading


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

    def get_file_name(self):
        return self.body.get("file")

    def __str__(self):
        return json.dumps({"header": self.header, "body": self.body, "origin": self.origin})


class Response(IResponse):

    def __init__(self, header: dict = {}, body: dict = {}, res: str = "", origin: str = "", *args, **kwargs) -> None:
        super().__init__(header, body, res, origin, *args, **kwargs)

    def get_res(self):
        return self.header.get("res")

    def get_data(self):
        return self.body.get("data")

    def get_origin(self):
        return self.origin

    def get_date(self):
        return self.header.get("date")

    def __str__(self):
        return json.dumps({"header": self.header, "body": self.body, "origin": self.origin})


class Client(IClient):

    def __init__(self, name: str, connection=None) -> None:
        super().__init__(name, connection)

    def __eq__(self, connection):
        return connection == self.connection

    def __repr__(self) -> str:
        return "{" + f"\"name\":\"{self.name}\",\"online\":\"{self.isConnect}\""+"}"


class TCPServer(Iserver):

    def __init__(self, db: mongodb):
        super().__init__()
        self.db = db
        self.clientNumber = 0
        self.serverTCP = socket(AF_INET, SOCK_STREAM)
        self.serverUDP = socket(family=AF_INET, type=SOCK_DGRAM)
        self.serverTCP.setblocking(0)
        self.serverUDP.setblocking(0)
        self.connectTCP = False
        self.connectUDP = False
        self.optionsReq: dict[str, function] = {}
        self.clients: dict[str, Client] = {}
        self.ThreadList: list[threading.Thread] = []
        self.load_options()

    def load_options(self):
        self.optionsReq["registar"] = self.register
        self.optionsReq["login"] = self.login
        self.optionsReq["sendMsg"] = self.send_msg
        self.optionsReq["sendMsgALL"] = self.send_msg_to_all
        self.optionsReq["getFilesList"] = self.get_files_list
        self.optionsReq["getConnectToUDP"] = self.request_to_connectUDP
        self.optionsReq["getFile"] = self.get_file

   # --------------------- private functionv--------------------
    def connect_to_TCP(self) -> bool:
        try:
            self.serverTCP.bind((self.host, self.port))
            self.port = self.serverTCP.getsockname()[1]
            self.serverTCP.listen()
            self.connect_to_UDP()
            self.connectTCP = True
            print("server is connect on TCP")
            return True
        except Exception as e:
            print("Failed to connect to server on TCP")
            print(e)
            return False

    def close_connection_TCP(self) -> bool:
        try:
            self.serverTCP.close()
            print("The disconnection was successful TCP")
            self.connectTCP = False
            self.close_connection_UDP()
            self.db.close_connection()
            return True
        except:
            print("Disconnection failed TCP")
            return False

    def connect_to_UDP(self) -> bool:
        try:
            self.serverUDP.bind((self.host, self.port))
            self.port = self.serverUDP.getsockname()[1]
            self.connectUDP = True
            print("server is connect on UDP")
            return True
        except:
            print("Failed to connect to server on UDP")
            return False

    def close_connection_UDP(self) -> bool:
        try:
            self.serverUDP.close()
            print("The disconnection was successful UDP")
            self.connectUDP = False
            self.db.close_connection()
            return True
        except:
            print("Disconnection failed UDP")
            return False

    def write_file_log(self, *args, **kwargs) -> None:
        listObj = []
        try:
            with open(self.File) as file:
                listObj: list = json.load(file)
            listObj.append(kwargs)
            with open(self.File, 'w') as json_file:
                json.dump(listObj, json_file,
                          indent=4,
                          separators=(',', ': '))
        except:
            pass
        for func in self.observs:
            func()

    def read_file_log(self) -> list[str]:
        listObj = []
        try:
            with open(self.File) as file:
                listObj = json.load(file)
                length = len(listObj)
            return listObj[::-1], length
        except:
            return [], 0

    def client_registration(self, *args, **kwargs) -> IResponse:
        succ, msg = self.db.user_exits(*args, **kwargs)
        if (succ, msg) == (False, "D-exist"):
            if self.db.create_user(*args, **kwargs):
                return Response(res="available")
            else:
                return Response(res="error")
        return Response(res=msg)

    def client_login_req(self, connection, *args, **kwargs) -> tuple[bool, IResponse]:
        name = kwargs["UserName"]
        if name in self.clients:
            return False, Response(res="Client connected", body={"args": [], "data": {"listOnline": []}})
        res = self.db.auth_user(*args, **kwargs)
        if res == (True, "match"):
            self.clients[name] = Client(name, connection)
            listOnline: list = self.client_online()
            return True, Response(res="Success", body={"args": [], "data": {"listOnline": listOnline}})
        return False, Response(res="Failure", body={"args": [], "data": {"listOnline": []}})

    def client_online(self) -> list:
        try:
            return [c for c in self.clients.keys()]
        except:
            return []

    def update_connections(self, inputs, outputs, exceptional) -> None:
        er = "Anonymous client"
        change = False
        for connection in exceptional:
            change = True
            self.clientNumber -= 1
            client = self.client_byConnection(connection)
            if client:
                meg = f"Lost connection with {client.name if client!=None else er}"
                self.write_file_log(log=meg)
                client.isConnect = False
                del self.clients[client.name]
                connection.close()
            if connection in inputs:
                inputs.pop(inputs.index(connection))
            if connection in outputs:
                outputs.pop(outputs.index(connection))
        if change:
            listOnline: list[str] = self.client_online()
            body = {
                "args": [],
                "data": {"listOnline": listOnline}
            }
            ressponse = Response(res="udpateFriend", body=body)
            print(listOnline)
            self.brodcast(ressponse)

    def client_byConnection(self, connection) -> IClient:
        for name, client in self.clients.items():
            if client == connection:
                return client
        return None

    def brodcast(self, res: IResponse, connection=None) -> None:
        try:
            for client in self.clients.values():
                if client.connection != connection:
                    client.connection.send(res.__str__().encode())
        except Exception as e:
            print("Exception ", e)

    def connectDB(self) -> bool:
        try:
            return self.db.connect_db()
        except:
            return False

    def Connection_byName(self, name) -> IClient:
        try:
            return self.clients[name].connection
        except:
            print("D-exist")
        return None

    def send_message_by_name(self, req: IRequest) -> bool:
        client_name = req.get_toClient()
        connection = self.Connection_byName(client_name)
        if connection:
            res = Response(res="msg", body=req.body)
            return self.send_response(connection, res)
        else:
            print("Connection does not exist")
            return False

    def send_response(self, connection, res: IResponse) -> bool:
        try:
            connection.send(res.__str__().encode())
            print(f"Send success")
            return True
        except Exception as e:
            print("Send faild ", e)
            return False

    def readTCP(self, connection, inputs: list, exceptional: list) -> None:

        if connection is self.serverTCP:
            self.server_req(connection, inputs)
        else:
            self.client_req(connection, exceptional)

    def server_req(self, connection, inputs: list) -> None:
        now = datetime.now()
        try:
            client, client_address = connection.accept()
            client.setblocking(0)
            inputs.append(client)
            self.clientNumber += 1
            self.write_file_log(log=str(
                now)+f" Request connect from  {client_address} -> client{self.clientNumber}")
        except:
            pass

    def client_req(self, connection, exceptional) -> None:
        try:
            request_string = connection.recv(4096).decode()
        except Exception as e:
            exceptional.append(connection)
            print(e)
        try:
            if request_string:
                request_dict = json.loads(request_string)
                request_object = Request(**request_dict)
                req = request_object.get_req()
                ans = self.optionsReq[req](request_object, connection)

            else:
                exceptional.append(connection)
        except Exception as e:
            exceptional.append(connection)
            print(e)

    def readUDP(self, connection) -> None:
        pass

    # ------------------- public function --------------------
    def register(self, req: IRequest, connection) -> bool:
        name = req.get_user()
        password = req.get_password()
        response: Response = self.client_registration(
            UserName=name, UserPassword=password)
        self.write_file_log(
            log=f"Request registar from  {name} -> {response.get_res()}")
        self.send_response(connection, response)

    def login(self, req: IRequest, connection) -> bool:
        name = req.get_user()
        password = req.get_password()
        succ, response = self.client_login_req(
            connection, UserName=name, UserPassword=password)
        listOnline = response.get_data()["listOnline"]
        self.write_file_log(
            log=f"Request login from  {name} -> {response.get_res()}")
        self.send_response(connection, response)
        if succ:
            body = {
                "args": [],
                "data": {"listOnline": listOnline}
            }
            res = Response(res="udpateFriend", body=body)
            self.brodcast(res,connection)
            return True
        else:
            return False

    def send_msg(self, req: IRequest, connection) -> bool:
        self.send_message_by_name(req)

    def send_msg_to_all(self, req: IRequest, connection) -> bool:
        res = Response(res="brodcastMsg", body=req.body)
        self.brodcast(res, connection)

    def get_files_list(self, req: IRequest, connection) -> bool:
        mypath = "./server/files"
        try:
            onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
            response = Response(res="fileList", body={
                                "args": [], "data": {"filesList": onlyfiles}})
            self.send_response(connection, response)
        except Exception as e:
            print(e)

    def get_file(self, req: IRequest, connection) -> bool:
        mypath = "./server/files"
        try:
            fileName = req.get_file_name()
            file_exist = os.path.isfile(path.join(mypath, fileName))
            if file_exist:
                response = Response(res="exist")
                self.send_response(connection, response)
                return True
            else:
                response = Response(res="D-exist")
                self.send_response(connection, response)
                return False

        except Exception as e:
            print(e)
        return False

    def request_to_connectUDP(self, req: IRequest, connection):
        return self.connect_to_UDP()

    def __call__(self) -> None:
        inputs = [self.serverTCP, self.serverUDP, ]
        outputs = []
        self.connectDB()
        while self.connectTCP:
            try:
                readable, writeable, exceptional = select.select(
                    inputs, outputs, inputs, 0.1)
            except Exception as e:
                print(e)
                continue
            for s in readable:
                s: socket
                if s.type == self.serverTCP.type:
                    th = threading.Thread(target=self.readTCP, args=[
                                          s, inputs, exceptional])
                    th.setName(f"Client {self.clientNumber}")
                    self.ThreadList.append(th)
                    th.start()

                elif s.type == self.serverUDP.type:
                    self.readUDP(s)
            try:
                self.update_connections(inputs, outputs, exceptional)
            except Exception as e:
                print(e)

            self.ThreadList = [th for th in self.ThreadList if th.is_alive()]

    def __del__(self) -> None:
        self.close_connection_TCP()
        print("Server destroyed, Goodbye!")

# TODO writeable
