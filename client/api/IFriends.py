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
    
    def write(self, *args, **kwargs)->None:
        '''
        The function adds to the message or log file of that client
        @return None
        '''
        pass
    
    def read(self, filename: str, f=0, to=10)->tuple[list,int,int]:
        '''
        The function reads from the message or logs file of that client
        @return None
        '''
        pass
    