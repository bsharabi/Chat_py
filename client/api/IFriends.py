from os import path
import os 
import json

class IFriend:
    
    def __init__(self, name: str, isConnect: bool, path_folder: str) -> None:
        self.name = name
        self.isConnect = isConnect
        self.data_folder = path_folder
        self.msg_file = path.join(path_folder, "msg.json")
        self.log_file = path.join(path_folder, "log.json")
        if not os.path.isfile(self.msg_file):
            with open(self.msg_file, 'w') as f:
                json.dump([], f,
                          indent=4,
                          separators=(',', ': '))

        if not os.path.isfile(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f,
                          indent=4,
                          separators=(',', ': '))
    
    def write(self):
        pass
    
    def read(self):
        pass
    
    def __repr__(self) -> str:
        pass