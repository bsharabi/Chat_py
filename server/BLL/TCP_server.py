import sys
sys.path.append("./Server")
from socket import *
import select
import json
from api.IClient import IClient
from api.IServer import *
from DAL.DataBase import mongodb
from datetime import datetime
from api.IRequest import *
from api.IResponse import *
class Request(IRequest):
    def __init__(self, header: dict = {}, body: dict = {}, req: str = "", fileName: str = "", user: str = "", password: str = "", origin: str = "", toClient: str = "", *args, **kwargs) -> None:
        super().__init__(header,body,req,fileName,user,password,origin,toClient,*args,**kwargs)
        
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
        print(form)
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
        super().__init__(header,body,res,origin,*args,**kwargs)

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

class client(IClient):

    def __init__(self, name: str, connection=None) -> None:
        super().__init__(name,connection)

    def __eq__(self, connection):
        return connection == self.connection

    def __repr__(self) -> str:
        return "{" + f"\"name\":\"{self.name}\",\"online\":\"{self.isConnect}\""+"}"

class TCPServer(Iserver):

    def __init__(self, db: mongodb):
        super().__init__()
        self.db = db
        self.clientNumber = 0
        self.host = "localhost"
        self.serverTCP = socket(AF_INET, SOCK_STREAM)
        self.serverUDP = socket(AF_INET, SOCK_DGRAM)
        # self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.serverTCP.setblocking(0)
        self.serverUDP.setblocking(0)
        self.connectTCP = False
        self.connectUDP = False
        self.optionsReq: dict[str, function] = {}
        self.clients: dict[str, client] = {}
        self.load_options()

    def load_options(self):
        self.optionsReq["registar"] = self.register
        self.optionsReq["login"] = self.login
        self.optionsReq["sendMsg"] = self.send_msg
        self.optionsReq["sendMsgALL"] = self.send_msg_to_all

    def connect_to_TCP(self):
        try:
            self.serverTCP.bind((self.host, self.port))
            self.port = self.serverTCP.getsockname()[1]
            self.serverTCP.listen()
            self.serverTCP.listen()

            self.connectTCP = True
            print("server is connect on TCP")
            return True
        except:
            print("Failed to connect to server on TCP")
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

    def connect_to_UDP(self):
        try:
            self.serverUDP.bind((self.host, self.port))
            self.port = self.serverUDP.getsockname()[1]
            self.serverUDP.listen()
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

    def client_registration(self, *args, **kwargs) -> Response:
        succ, msg = self.db.user_exits(*args, **kwargs)
        if (succ, msg) == (False, "D-exist"):
            if self.db.create_user(*args, **kwargs):
                return Response(res="available")
            else:
                return Response(res="error")
        return Response(res=msg)

    def client_login_req(self, connection, *args, **kwargs) -> tuple[bool, Response]:
        name = kwargs["UserName"]
        if name in self.clients:
            return False, Response(res="Client connected", body={"args": [], "data": {"listOnline": []}})
        res = self.db.auth_user(*args, **kwargs)
        print(res)
        if res == (True, "match"):
            self.clients[name] = client(name, connection)
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
                self.write_file(log=meg)
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
            res = Response(res="udpateFriend", body=body)
            print(res)
            self.brodcast(res)

    def client_byConnection(self, connection) -> client:
        for name, client in self.clients.items():
            if client == connection:
                return client
        return None

    def brodcast(self, res: Response) -> None:
        try:
            for client in self.clients.values():
                client.connection.send(res.__str__().encode())
        except Exception as e:
            print("Exception ", e)

    def connectDB(self) -> bool:
        try:
            return self.db.connect_db()
        except:
            return False

    def Connection_byName(self, name) -> client:
        try:
            return self.clients[name].connection
        except:
            print("D-exist")
        return None

    def send_message_by_name(self, req: Request) -> bool:
        client_name = req.get_toClient()
        connection = self.Connection_byName(client_name)
        if connection:
            res = Response(res="msg", body=req.body)
            return self.send_response(connection, res)
        else:
            print("Connection does not exist")
            return False

    def send_response(self, connection, res: Response):
        try:
            connection.send(res.__str__().encode())
            print("Send success")
            return True
        except Exception as e:
            print("Send faild ", e)
            return False

    def readTCP(self, connection, inputs: list, exceptional: list):
        if connection is self.serverTCP:
            self.server_req(connection, inputs)
        else:
            self.client_req(connection, exceptional)

    def server_req(self, connection, inputs: list):
        now = datetime.now()
        try:
            client, client_address = connection.accept()
            client.setblocking(0)
            inputs.append(client)
            self.clientNumber += 1
            self.write_file(log=str(
                now)+f" Request connect from  {client_address} -> client{self.clientNumber}")
        except:
            pass

    def client_req(self, connection, exceptional):
        try:
            request_string = connection.recv(4096).decode()
        except:
            pass
        try:
            if request_string:
                request_dict = json.loads(request_string)
                request_object = Request(**request_dict)
                req = request_object.get_req()
                ans = self.optionsReq[req](request_object, connection)

            else:
                exceptional.append(connection)
        except Exception as e:
            print(e)

    def readUDP(self, connection):
        pass

    def register(self, req: Request, connection) -> bool:
        name = req.get_user()
        password = req.get_password()
        response: Response = self.client_registration(
            UserName=name, UserPassword=password)
        self.write_file(
            log=f"Request registar from  {name} -> {response.get_res()}")
        self.send_response(connection, response)

    def login(self, req: Request, connection) -> bool:
        name = req.get_user()
        password = req.get_password()
        succ, response = self.client_login_req(
            connection, UserName=name, UserPassword=password)
        listOnline = response.get_data()["listOnline"]
        self.write_file(
            log=f"Request login from  {name} -> {response.get_res()}")
        self.send_response(connection, response)
        if succ:
            body = {
                "args": [],
                "data": {"listOnline": listOnline}
            }
            res = Response(res="udpateFriend", body=body)
            self.brodcast(res)
            return True
        else:
            return False

    def send_msg(self, req: Request, connection) -> bool:
        self.send_message_by_name(req)

    def send_msg_to_all(self, req: Request, connection) -> bool:
        res = Response(res="brodcastMsg", body=req.body)
        self.brodcast(res)

    def __call__(self):

        inputs = [self.serverTCP, self.serverUDP]
        outputs = []
        self.connectDB()
        while self.connectTCP:
            readable, writeable, exceptional = select.select(
                inputs, outputs, inputs, 0.1)
            for s in readable:
                s: socket
                if s.type == self.serverTCP.type:
                    # threading.Thread(target=self.readTCP, args=[
                    #                  s, inputs, exceptional]).start()
                    self.readTCP(s, inputs, exceptional)
                elif s.type == self.serverUDP.type:
                    self.readUDP(s)
            try:
                self.update_connections(inputs, outputs, exceptional)
            except:
                pass

    def __del__(self):
        self.close_connection_TCP()
        print("Server destroyed, Goodbye!")

#TODO writeable
