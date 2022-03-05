
from os import path
import json
import os
from api.IRequest import IRequest
import sys
from api.IResponse import *

class Iserver:

    def __init__(self) -> None:
        try:
            self.port:int = int(sys.argv[2])
            self.host:str = sys.argv[1]
        except Exception as e:
            self.host = "localhost"
            self.port = 3000

        self.mc=1
        self.File = "./server/data/log.json"
        self.directory = "data"
        self.parent_dir = "./server"
        self.path = path.join("./server", "data")
        if not path.isdir("./server/data"):
            os.mkdir(self.path)
        if not os.path.isfile(self.File):
            with open(self.File, 'w') as f:
                json.dump([], f,
                          indent=4,
                          separators=(',', ': '))
        self.observs:list[function]=[]
        
    def write_file(self, *args, **kwargs)->None:
        pass

    def read_file_log(self, limitFrom=0, limitTo=19) -> list[str]:
        pass

    def connect_to_TCP(self)->None:
        pass

    def close_connection_TCP(self)->None:
        pass

    def registar(self,req:IRequest,connection)->bool:
        pass
    
    def login(self,req:IRequest,connection)->bool:
        pass
    
    def send_msg(self:IRequest,req,connection)->bool:
        pass
        
    def send_msg_to_all(self:IRequest,req,connection)->bool:
        pass