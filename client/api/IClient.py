from os import path
import os
from .IFriends import IFriend

class Iclient:

    def __init__(self) -> None:
        self.id = id
        self.mc = 0
        self.connected: bool = False
        self.name = "user"
        self.port = None
        self.host = None
        self.friends: dict[str, IFriend] = {}
        self.directory = "./client/data"
        self.path = path.join("./client", "data")
        if not path.isdir("./client/data"):
            os.mkdir(self.path)

    def connect_to_TCP(self):
        pass

    def data_directory(self):
        pass

    def close_connection_TCP(self):
        pass

    def login():
        pass

    def register():
        pass

    def request(self, *args, **kwargs):
        pass

    def response(self):
        pass