from os import path
import os
from .IFriends import IFriend
import threading
from IResponse import IResponse


class Iclient:

    def __init__(self) -> None:
        self.id = id
        self.connected: bool = False
        self.name = "user"
        self.mc = 0
        self.port = None
        self.host = None
        self.friends: dict[str, IFriend] = {}
        self.directory = "./Client/data"
        self.path = path.join("./Client", "data")
        if not path.isdir("./Client/data"):
            os.mkdir(self.path)
        self.file_list: list[str] = []
        self.download_file_count_pack = 0
        self.download_start = False

    def connect_to_TCP(self) -> bool:
        """
        connect to client on TCP protocol 
        @return: True if connect successful False o.w.
        """
        pass

    def close_connection_TCP(self) -> bool:
        """
        close connection client on TCP protocol 
        @return: True if close successful False o.w.
        """
        pass

    def connect_to_UDP(self) -> bool:
        """
        connect to client on UDP protocol 
        @return: True if connect successful False o.w.
        """
        pass

    def close_connection_UDP(self) -> bool:
        """
        close connection client on UDP protocol 
        @return: True if close successful False o.w.
        """
        pass

    def create_data_directory(self) -> bool:
        '''
        The function creates a folder in which it stores all the messages from the customers
        @return True if the data directory created False o.w.
        '''
        pass

    def create_data_directory_friends(self) -> None:
        '''
        The function creates an information folder for each new customer in which it stores the specific information about the customer.
        Messages, date and logs
        @return: None
        '''

    def login(self) -> tuple[bool, str]:
        '''
        sending a login request to the server 
        @return: Returns True,Succ if the login was successful False,Failur o.w.
        example:
        request = Request(header={"req": login}, user=user,password=password, origin=origin, *args, **kwargs)                
        '''
        pass

    def register(self) -> tuple[bool, str]:
        '''
        sending a registration request to the server
        @return: Returns True,avilable if the registry was successful False,some msg o.w.
        example:
        request = Request(header={"req": register}, user=user,password=password, origin=origin, *args, **kwargs)                
        '''

    def udpateFriend(self, res: IResponse) -> None:
        '''
        The function receives a response object from the server and updates the connected clients
        @param res:
        example body = {
                "args": [],
                "data": {"listOnline": listOnline}
            }
            ressponse = Response(res="udpateFriend", body=body)
            @return: None
        '''
        pass

    def download_file(self, res: IResponse) -> bool:
        '''
        The function receives a response object from the server and updates the client
        whether it is possible to download the requested file and also whether 
        it is possible to connect to the file server
        @param res: 
        @return True if file exist and can start download file from the server False o.w.
        example :response = Response(res="downloadFile",flag=1,file_name=fileName,packet_count="" )
        '''
        pass

    def brodcast(self, res: IResponse) -> None:
        '''
        The function sends messages to all connected clients without the connection of the sending client 
        @param res: The response format for other client
        @param connection: connection of the sending client 
        @return None
        tuohti
        @return: True if succ False o.w.
        '''
        pass

    def get_msg(self, res: IResponse) -> None:
        '''
        The function receives a response object from the
        server with a message from another client and updates the client's message file
        @param res:IResponse Object
        example res = Response(res="msg", body=req.body)
        '''
        pass

    def request(self, req: str = "", fileName: str = "",  password: str = "", origin: str = "", toClient: str = "", *args, **kwargs) -> None:
        '''
        Function responsible for creating a new request for server and send
        @param req : IRequest Object
        @param fileName : if the request of type getFile
        .
        .
        .
        @return None
        example:
        request = Request(req=req, fileName=fileName, user=self.name, password=password,
                          origin=origin, toClient=toClient, *args, **kwargs)
        '''
        
        pass

    def response(self) -> None:
        '''
        The function listens for answers from the server and routes each request to the relevant function
        @return None 
        '''
        pass
