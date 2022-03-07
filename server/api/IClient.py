from socket import socket


class IClient:

    def __init__(self, name: str, connection: socket = None) -> None:
        '''
        return None
        '''
        # name of client
        self.name = name
        # save client connection to the server
        self.connection = connection
        # field of client, True if client connect to the server false if not
        self.isConnect = True

    def __eq__(self, connection: socket):
        pass

    def __repr__(self) -> str:
        '''
        return the client's deteils in server 
        '''
        pass
