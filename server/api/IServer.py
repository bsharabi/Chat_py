
from os import path
import json
import os
from socket import socket
from api.IRequest import IRequest
import sys
from api.IResponse import *

class Iserver:

    def __init__(self) -> None:
        # option ti load port and host from terminal 
        # args[1] is host
        #args[2] is port 
        try:
            self.port:int = int(sys.argv[2])
            self.host:str = sys.argv[1]
        except Exception as e:
            self.host = "localhost"
            self.port = 3000
     
        #The current version of this server
        self.mc=1
        # directory of log file 
        self.File = "./server/data/log.json"
        # data directory 
        self.directory = "data"
        # parent directory (root)
        self.parent_dir = "./server"
        # create path to data
        self.path = path.join("./server", "data")
        # check if the data dir is exist, if not create one 
        if not path.isdir("./server/data"):
            os.mkdir(self.path)
        if not os.path.isfile(self.File):
            with open(self.File, 'w') as f:
                json.dump([], f,
                          indent=4,
                          separators=(',', ': '))
        # observe
        self.observs:list[function]=[]
        
    def get_mc(self)->int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this srever.
        """   
        pass
    
    def write_file_log(self, *args, **kwargs)->None:
        """
        Saves the logs server in JSON format to a file
        @param  dict: {"log":log msg}
        example: write_file(log="connect to the server")
        """
        pass

    def read_file_log(self) -> list[str]:
        """
        load the logs server from JSON format file to the UI
        """
        pass

    def connect_to_TCP(self)->bool:
        """
        connect to server on TCP protocol 
        @return: True if connect successful False o.w.
        """
        pass

    def close_connection_TCP(self)->bool:
        """
        close connection server on TCP protocol 
        @return: True if close successful False o.w.
        """
        pass
    
    def connect_to_UDP(self)->bool:
        """
        connect to server on UDP protocol 
        @return: True if connect successful False o.w.
        """
        pass

    def close_connection_UDP(self)->bool:
        """
        close connection server on UDP protocol 
        @return: True if close successful False o.w.
        """
        pass

    def registar(self,req:IRequest,connection:socket)->bool:
        '''
        Receives a registration request from the client and his connection to the server
        @param req(IRequest): 
        @param connection: 
        @return: Returns True if the registry was successful False o.w.
        example:
        request = Request(header={"req": register}, user=user,password=password, origin=origin, *args, **kwargs)                
        '''
        pass
    
    def login(self,req:IRequest,connection:socket)->bool:
        '''
        Receives a login request from the client and his connection to the server
        @param req(IRequest): 
        @param connection: 
        @return: Returns True if the login was successful False o.w.
        if True the server send to all the client list online who online to the server 
        example:
        request = Request(header={"req": login}, user=user,password=password, origin=origin, *args, **kwargs)                
        '''
        pass
    
    def send_msg(self:IRequest,req,connection:socket)->bool:
        '''
        Receives a senMsg request from the client and his connection to the server
        @param req(IRequest): 
        @param connection: 
        @return: Returns True if the sendMsg was successful False o.w.
        example:
        request = Request(header={"req": sendMsg}, user=user,toClient=Name of the receiving client, origin=origin, *args, **kwargs)                
        '''
        pass
        
    def send_msg_to_all(self:IRequest,req,connection:socket)->bool:      
        '''
        Receives a senMsgALL request from the client and his connection to the server
        @param req(IRequest): 
        @param connection: 
        @return: Returns True if the senMsgALL was successful False o.w.
        example:
        request = Request(header={"req": senMsgALL}, user=user,toClient=Friend Group, origin=origin, *args, **kwargs)                
        '''
        pass
    
    def get_files_list(self, req: IRequest, connection:socket) -> bool:
        '''
        Receives a getFilesList request from the client and his connection to the server
        @param req(IRequest): 
        @param connection: 
        @return: Returns a list of all file names on the server or empty list
        example:
        request = Request(header={"req": getFilesList}, *args, **kwargs)                
        '''
        pass
    
    def get_file(self, req: IRequest, connection:socket) -> bool:
        '''
        Receives a getFile request from the client and his connection to the server
        @param req(IRequest): 
        @param connection: 
        @return: Returns a True if file exist and start UDP server and send response to the client 
                    False if have a problem with a file
        example:
        flag = 1 file exist and res:downloadFile
        flag = 0 file does not exist and res: D-downloadFile
        flag = -1 file error and res: err_downloadFile
        response = Response(res="downloadFile",flag=1,file_name=fileName,packet_count="" )
        request = Request(header={"req": getfile},filename=file_name *args, **kwargs)                
        '''
        
        pass