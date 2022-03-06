from os import path
import os
from .IFriends import IFriend
import threading
class Iclient:

    def __init__(self) -> None:
        self.id = id
        self.connected: bool = False
        self.name = "user"
        self.mc=0
        self.port = None
        self.host = None
        self.friends: dict[str, IFriend] = {}
        self.directory = "./Client/data"
        self.path = path.join("./Client", "data")
        if not path.isdir("./Client/data"):
            os.mkdir(self.path)
        self.file_list:list[str]=[]
        self.download_file_count_pack=0
        self.download_start=False



    def connect_to_TCP(self):
        pass

    def data_directory(self):
        pass

    def close_connection_TCP(self):
        pass

    def login(self):
        pass

    def register(self):
        pass

    def request(self, req: str = "", fileName: str = "",  password: str = "", origin: str = "", toClient: str = "", *args, **kwargs):
        pass

    def response(self):
        pass