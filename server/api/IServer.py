
from os import path
import json
import os
from datetime import datetime
from api.IRequest import IRequest


class Iserver:

    def __init__(self) -> None:
        self.port = 3000
        self.mc=1
        self.host = "localhost"
        self.File = "./server/data/log.json"
        self.directory = "data"
        self.parent_dir = "./"
        self.path = path.join("./server", "data")
        if not path.isdir("./server/data"):
            os.mkdir(self.path)
        if not os.path.isfile(self.File):
            with open(self.File, 'w') as f:
                json.dump([], f,
                          indent=4,
                          separators=(',', ': '))

    def write_file(self, *args, **kwargs):
        listObj = []
        try:
            with open(self.File) as file:
                listObj:list = json.load(file)
            listObj.append(kwargs)
            with open(self.File, 'w') as json_file:
                json.dump(listObj, json_file,
                          indent=4,
                          separators=(',', ': '))
        except:
            pass
        self.mc+=1

    def read_file_log(self, f=0, to=19) -> list[str]:
        listObj = []
        try:
            with open(self.File) as file:
                listObj = json.load(file)
                listObj = listObj[::-1]
                length = len(listObj)
            if length > to:
                return listObj[length-19:length], length-19, length
            return listObj[f:to], f, to
        except:
            return [], f, to

    def connect_to_TCP(self):
        pass

    def close_connection_TCP(self):
        pass

    def registar(self,req:IRequest,connection):
        pass
    
    def login(self,req:IRequest,connection):
        pass
    
    def send_msg(self:IRequest,req,connection):
        pass
        
    def send_msg_to_all(self:IRequest,req,connection):
        pass